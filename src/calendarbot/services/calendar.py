"""Calendar service for managing meetings."""

import logging
from datetime import datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from calendarbot.db.models import User
from calendarbot.db.repository import MeetingRepository, OAuthTokenRepository
from calendarbot.integrations.google import GoogleCalendarClient
from calendarbot.integrations.zoom import ZoomClient
from calendarbot.services.parser import ParsedMeeting
from calendarbot.utils.encryption import TokenEncryption
from calendarbot.utils.timezone import TimezoneHelper

logger = logging.getLogger(__name__)


class CalendarService:
    """Business logic for calendar operations."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.meeting_repo = MeetingRepository(session)
        self.token_repo = OAuthTokenRepository(session)
        self.encryption = TokenEncryption()

    async def _get_valid_client(self, user: User) -> tuple[GoogleCalendarClient, str] | dict:
        """Get a Google Calendar client with valid tokens, refreshing if needed.

        Returns GoogleCalendarClient on success, or dict with error on failure.
        """
        token = await self.token_repo.get_token(user.id, "google")
        if not token:
            return {"error": "Google Calendar not connected. Use /connect to link your calendar."}

        access_token = self.encryption.decrypt(token.access_token_encrypted)
        refresh_token = self.encryption.decrypt(token.refresh_token_encrypted)

        # Always try to refresh if token is expired or close to expiry (5 min buffer)
        from datetime import timedelta

        if datetime.utcnow() >= (token.expires_at - timedelta(minutes=5)):
            logger.info(f"Token expired or expiring soon for user {user.id}, refreshing...")
            client = GoogleCalendarClient(
                access_token=access_token,
                refresh_token=refresh_token,
            )
            new_tokens = await client.refresh_access_token()
            if new_tokens:
                await self.token_repo.save_token(
                    user_id=user.id,
                    provider="google",
                    access_token_encrypted=self.encryption.encrypt(new_tokens["access_token"]),
                    refresh_token_encrypted=self.encryption.encrypt(
                        new_tokens.get("refresh_token") or refresh_token
                    ),
                    expires_at=new_tokens["expires_at"],
                )
                access_token = new_tokens["access_token"]
                logger.info(f"Token refreshed successfully for user {user.id}")
            else:
                logger.error(f"Token refresh failed for user {user.id}")
                return {
                    "error": "Failed to refresh Google token. Please /disconnect and /connect again."
                }

        return (
            GoogleCalendarClient(
                access_token=access_token,
                refresh_token=refresh_token,
            ),
            token.calendar_id or "primary",
        )

    async def _handle_api_error(self, result: dict, user: User, retry_func) -> dict:
        """Handle API errors, refreshing token and retrying on 401."""
        if result.get("code") == 401:
            logger.info(f"Got 401 for user {user.id}, forcing token refresh...")
            # Force token refresh by setting expiry to past
            token = await self.token_repo.get_token(user.id, "google")
            if token:
                from datetime import timedelta

                token.expires_at = datetime.utcnow() - timedelta(hours=1)
                await self.session.flush()

            # Retry with fresh token
            return await retry_func()
        return result

    async def _get_zoom_link(
        self,
        user: User,
        meeting_data: ParsedMeeting,
    ) -> str | None:
        """Create a Zoom meeting and return the join URL.

        Returns the Zoom join URL or None if failed.
        """
        token = await self.token_repo.get_token(user.id, "zoom")
        if not token:
            logger.warning(f"No Zoom token for user {user.id}")
            return None

        access_token = self.encryption.decrypt(token.access_token_encrypted)
        refresh_token = self.encryption.decrypt(token.refresh_token_encrypted)

        zoom_client = ZoomClient(access_token=access_token, refresh_token=refresh_token)

        # Calculate duration in minutes
        duration = int(
            (meeting_data.end_datetime - meeting_data.start_datetime).total_seconds() / 60
        )

        result = await zoom_client.create_meeting(
            topic=meeting_data.title,
            start_time=meeting_data.start_datetime,
            duration=duration,
            timezone=user.timezone,
        )

        if "error" in result:
            # Try token refresh on 401
            if result.get("code") == 401:
                logger.info(f"Zoom token expired for user {user.id}, refreshing...")
                new_tokens = await zoom_client.refresh_access_token()
                if new_tokens:
                    await self.token_repo.save_token(
                        user_id=user.id,
                        provider="zoom",
                        access_token_encrypted=self.encryption.encrypt(new_tokens["access_token"]),
                        refresh_token_encrypted=self.encryption.encrypt(
                            new_tokens.get("refresh_token") or refresh_token
                        ),
                        expires_at=new_tokens["expires_at"],
                    )
                    # Retry with new token
                    zoom_client = ZoomClient(
                        access_token=new_tokens["access_token"],
                        refresh_token=new_tokens.get("refresh_token") or refresh_token,
                    )
                    result = await zoom_client.create_meeting(
                        topic=meeting_data.title,
                        start_time=meeting_data.start_datetime,
                        duration=duration,
                        timezone=user.timezone,
                    )

            if "error" in result:
                logger.error(f"Failed to create Zoom meeting for user {user.id}: {result}")
                return None

        return result.get("join_url")

    async def create_meeting(
        self,
        user: User,
        meeting_data: ParsedMeeting,
        generate_meet_link: bool = False,
        generate_zoom_link: bool = False,
        custom_link: str | None = None,
    ) -> dict:
        """Create a meeting on user's calendar.

        Args:
            user: The user creating the meeting.
            meeting_data: Parsed meeting data.
            generate_meet_link: If True, auto-generate a Google Meet link.
            generate_zoom_link: If True, create a Zoom meeting and add the link.
            custom_link: Custom meeting link to add to the event.

        Returns dict with meeting details or error.
        """
        # Generate Zoom link first if requested (before creating calendar event)
        zoom_link = None
        if generate_zoom_link:
            zoom_link = await self._get_zoom_link(user, meeting_data)
            if zoom_link:
                # Use Zoom link as custom link in the calendar event
                custom_link = zoom_link

        client_result = await self._get_valid_client(user)
        if isinstance(client_result, dict):
            return client_result  # Error
        client, calendar_id = client_result

        # Keep times in user's local timezone for Google API
        start_local = meeting_data.start_datetime
        end_local = meeting_data.end_datetime

        # Determine reminders to use
        reminders = self._resolve_reminders(user, meeting_data)

        async def do_create():
            return await client.create_event(
                summary=meeting_data.title,
                start_time=start_local,
                end_time=end_local,
                attendees=meeting_data.attendees,
                timezone=user.timezone,
                calendar_id=calendar_id,
                reminders=reminders,
                generate_meet_link=generate_meet_link,
                custom_link=custom_link,
            )

        result = await do_create()

        # Retry on 401
        if result.get("code") == 401:
            result = await self._handle_api_error(result, user, do_create)

        if "error" in result:
            return result

        # Extract Meet link from conference data if present
        meet_link = None
        if "conferenceData" in result:
            for entry_point in result["conferenceData"].get("entryPoints", []):
                if entry_point.get("entryPointType") == "video":
                    meet_link = entry_point.get("uri")
                    break

        # Convert to UTC for local cache storage (naive datetime for PostgreSQL)
        start_utc = TimezoneHelper.to_utc(meeting_data.start_datetime, user.timezone)
        end_utc = TimezoneHelper.to_utc(meeting_data.end_datetime, user.timezone)
        # Strip timezone info for database (TIMESTAMP WITHOUT TIME ZONE)
        start_utc_naive = start_utc.replace(tzinfo=None)
        end_utc_naive = end_utc.replace(tzinfo=None)

        # Cache meeting locally with reminders for notification system
        await self.meeting_repo.save_meeting(
            user_id=user.id,
            external_id=result["id"],
            provider="google",
            title=meeting_data.title,
            start_time=start_utc_naive,
            end_time=end_utc_naive,
            attendees=meeting_data.attendees,
            reminders=reminders if reminders else None,
        )

        return {
            "success": True,
            "event_id": result["id"],
            "link": result.get("htmlLink", ""),
            "title": meeting_data.title,
            "start": meeting_data.start_datetime,
            "end": meeting_data.end_datetime,
            "attendees": meeting_data.attendees,
            "reminders": reminders,
            "meet_link": meet_link,
            "zoom_link": zoom_link,
            "custom_link": custom_link if not zoom_link else None,
        }

    def _resolve_reminders(self, user: User, meeting_data: ParsedMeeting) -> list[int] | None:
        """Resolve which reminders to use for the meeting.

        Returns:
            - list[int]: specific reminder minutes
            - []: empty list means no reminders
            - None: use calendar default (but we default to no reminders if not specified)
        """
        if meeting_data.reminders:
            # Specific reminders in the request
            return meeting_data.reminders
        elif meeting_data.use_default_reminder:
            # 'r' was specified, use user's default
            if user.default_reminder:
                return [int(x) for x in user.default_reminder.split(",")]
            else:
                return []  # User has no default, so no reminders
        else:
            # No 'r' in request - no reminders
            return []

    async def is_privacy_mode(self, user: User) -> bool:
        """Check if user is connected in privacy mode (no calendar read access)."""
        token = await self.token_repo.get_token(user.id, "google")
        return token is not None and token.privacy_mode

    async def get_upcoming_meetings(self, user: User, limit: int = 10) -> tuple[list[dict], bool]:
        """Get upcoming meetings.

        In privacy mode: returns only bot-created meetings from local DB.
        In full access mode: returns meetings from Google Calendar API.

        Returns:
            Tuple of (meetings list, is_privacy_mode flag)
        """
        # Check if user is in privacy mode
        privacy_mode = await self.is_privacy_mode(user)

        if privacy_mode:
            # Privacy mode: fetch from local database only
            return await self._get_local_meetings(user, limit), True

        # Full access mode: fetch from Google Calendar
        client_result = await self._get_valid_client(user)
        if isinstance(client_result, dict):
            return [], False  # No calendar connected or token error
        client, calendar_id = client_result

        async def do_list():
            return await client.list_events(
                calendar_id=calendar_id,
                time_min=datetime.utcnow(),
                max_results=limit,
            )

        result = await do_list()

        # Retry on 401
        if result.get("code") == 401:
            result = await self._handle_api_error(result, user, do_list)

        if "error" in result:
            logger.error(f"Failed to list events for user {user.id}: {result}")
            return [], False

        events = result.get("items", [])
        meetings = []

        for event in events:
            start_data = event.get("start", {})
            end_data = event.get("end", {})

            # Handle both dateTime (timed events) and date (all-day events)
            start_str = start_data.get("dateTime") or start_data.get("date")
            end_str = end_data.get("dateTime") or end_data.get("date")

            if not start_str or not end_str:
                continue

            # Parse datetime - Google returns ISO format with timezone
            from dateutil import parser as dateutil_parser

            start_time = dateutil_parser.isoparse(start_str)
            end_time = dateutil_parser.isoparse(end_str)

            # Convert to user's timezone for display
            if start_time.tzinfo:
                start_time = start_time.astimezone(TimezoneHelper.get_timezone(user.timezone))
                end_time = end_time.astimezone(TimezoneHelper.get_timezone(user.timezone))

            attendees = [a.get("email", "") for a in event.get("attendees", [])]

            # Extract meet link
            meet_link = event.get("hangoutLink")
            if not meet_link and "conferenceData" in event:
                for entry_point in event["conferenceData"].get("entryPoints", []):
                    if entry_point.get("entryPointType") == "video":
                        meet_link = entry_point.get("uri")
                        break

            meetings.append(
                {
                    "id": event.get("id"),
                    "external_id": event.get("id"),
                    "title": event.get("summary", "(No title)"),
                    "start_time": start_time,
                    "end_time": end_time,
                    "attendees": attendees,
                    "link": meet_link,
                }
            )

        return meetings, False

    async def _get_local_meetings(self, user: User, limit: int = 10) -> list[dict]:
        """Get upcoming meetings from local database cache (for privacy mode)."""
        meetings_db = await self.meeting_repo.get_upcoming(user.id, limit=limit)

        meetings = []
        for meeting in meetings_db:
            # Convert stored UTC times to user's timezone for display
            start_time = TimezoneHelper.from_utc(meeting.start_time, user.timezone)
            end_time = TimezoneHelper.from_utc(meeting.end_time, user.timezone)

            # Parse attendees from JSON
            attendees = []
            if meeting.attendees and isinstance(meeting.attendees, dict):
                attendees = meeting.attendees.get("emails", [])

            meetings.append(
                {
                    "id": meeting.external_id,
                    "external_id": meeting.external_id,
                    "title": meeting.title or "(No title)",
                    "start_time": start_time,
                    "end_time": end_time,
                    "attendees": attendees,
                    "link": None,  # Link not stored in local DB
                }
            )

        return meetings

    async def update_meeting(
        self,
        user: User,
        event_id: str,
        title: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        attendees: list[str] | None = None,
        custom_link: str | None = None,
        generate_meet_link: bool = False,
    ) -> dict:
        """Update an existing meeting.

        Args:
            user: The user updating the meeting.
            event_id: Google Calendar event ID.
            title: New title (or None to keep existing).
            start_time: New start time in user's timezone (or None to keep).
            end_time: New end time in user's timezone (or None to keep).
            attendees: New attendee list (or None to keep).
            custom_link: Custom meeting link (or None to keep).
            generate_meet_link: If True, add Google Meet link.

        Returns dict with updated meeting details or error.
        """
        client_result = await self._get_valid_client(user)
        if isinstance(client_result, dict):
            return client_result  # Error
        client, calendar_id = client_result

        async def do_update():
            return await client.update_event(
                event_id=event_id,
                calendar_id=calendar_id,
                summary=title,
                start_time=start_time,
                end_time=end_time,
                timezone=user.timezone,
                attendees=attendees,
                custom_link=custom_link,
                generate_meet_link=generate_meet_link,
            )

        result = await do_update()

        # Retry on 401
        if result.get("code") == 401:
            result = await self._handle_api_error(result, user, do_update)

        if "error" in result:
            return result

        # Update local cache if exists
        if title or start_time or end_time or attendees:
            # Convert times to UTC for local storage
            local_updates: dict[str, Any] = {}
            if title:
                local_updates["title"] = title
            if start_time:
                start_utc = TimezoneHelper.to_utc(start_time, user.timezone)
                local_updates["start_time"] = start_utc.replace(tzinfo=None)
            if end_time:
                end_utc = TimezoneHelper.to_utc(end_time, user.timezone)
                local_updates["end_time"] = end_utc.replace(tzinfo=None)
            if attendees is not None:
                local_updates["attendees"] = {"emails": attendees}

            await self.meeting_repo.update_by_external_id(
                user.id, event_id, "google", **local_updates
            )

        # Extract Meet link from response if present
        meet_link = None
        if "conferenceData" in result:
            for entry_point in result["conferenceData"].get("entryPoints", []):
                if entry_point.get("entryPointType") == "video":
                    meet_link = entry_point.get("uri")
                    break

        return {
            "success": True,
            "event_id": result.get("id"),
            "title": result.get("summary", "(No title)"),
            "meet_link": meet_link,
        }

    async def cancel_meeting(self, user: User, event_id: str) -> dict:
        """Cancel a meeting by Google event ID."""
        client_result = await self._get_valid_client(user)
        if isinstance(client_result, dict):
            return client_result  # Error
        client, calendar_id = client_result

        # Get event details first (for the title in response)
        event = await client.get_event(event_id=event_id, calendar_id=calendar_id)

        if "error" in event:
            return {"error": "Meeting not found"}

        title = event.get("summary", "(No title)")

        # Delete from Google Calendar
        async def do_delete():
            return await client.delete_event(event_id=event_id, calendar_id=calendar_id)

        result = await do_delete()

        # Retry on 401
        if result.get("code") == 401:
            result = await self._handle_api_error(result, user, do_delete)

        if "error" in result:
            return result

        # Remove from local cache if exists
        await self.meeting_repo.delete_by_external_id(user.id, event_id, "google")

        return {"success": True, "title": title}
