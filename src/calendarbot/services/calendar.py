"""Calendar service for managing meetings."""

import logging
from datetime import datetime
from typing import Any, cast

from sqlalchemy.ext.asyncio import AsyncSession

from calendarbot.db.models import User
from calendarbot.db.repository import MeetingRepository, OAuthTokenRepository
from calendarbot.integrations.google import GoogleCalendarClient
from calendarbot.integrations.outlook import OutlookCalendarClient
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

    async def _get_valid_client(
        self, user: User, force_provider: str | None = None
    ) -> tuple[GoogleCalendarClient | OutlookCalendarClient, str, str] | dict:
        """Get a calendar client with valid tokens, refreshing if needed.

        Respects user's default_calendar preference. Falls back to whichever is connected.

        Args:
            user: The user to get client for.
            force_provider: If set, force using this provider ('google' or 'outlook').

        Returns (client, calendar_id, provider) on success, or dict with error on failure.
        """
        google_token = await self.token_repo.get_token(user.id, "google")
        outlook_token = await self.token_repo.get_token(user.id, "outlook")

        # If forcing a specific provider
        if force_provider:
            if force_provider == "google" and google_token:
                return await self._get_google_client(user, google_token)
            elif force_provider == "outlook" and outlook_token:
                return await self._get_outlook_client(user, outlook_token)
            else:
                return {"error": f"{force_provider.title()} calendar not connected."}

        # Determine priority based on user preference
        preferred = user.default_calendar
        if preferred == "google" and google_token:
            return await self._get_google_client(user, google_token)
        elif preferred == "outlook" and outlook_token:
            return await self._get_outlook_client(user, outlook_token)

        # No preference or preferred not connected - fall back to first available
        if google_token:
            return await self._get_google_client(user, google_token)
        if outlook_token:
            return await self._get_outlook_client(user, outlook_token)

        return {
            "error": "No calendar connected. Use /connect or /connectoutlook to link your calendar."
        }

    async def _get_google_client(
        self, user: User, token
    ) -> tuple[GoogleCalendarClient, str, str] | dict:
        """Get a Google Calendar client with valid tokens."""
        access_token = self.encryption.decrypt(token.access_token_encrypted)
        refresh_token = self.encryption.decrypt(token.refresh_token_encrypted)

        # Always try to refresh if token is expired or close to expiry (5 min buffer)
        from datetime import timedelta

        if datetime.utcnow() >= (token.expires_at - timedelta(minutes=5)):
            logger.info(f"Google token expired or expiring soon for user {user.id}, refreshing...")
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
                logger.info(f"Google token refreshed successfully for user {user.id}")
            else:
                logger.error(f"Google token refresh failed for user {user.id}")
                return {
                    "error": "Failed to refresh Google token. Please /disconnect and /connect again."
                }

        return (
            GoogleCalendarClient(
                access_token=access_token,
                refresh_token=refresh_token,
            ),
            token.calendar_id or "primary",
            "google",
        )

    async def _get_outlook_client(
        self, user: User, token
    ) -> tuple[OutlookCalendarClient, str, str] | dict:
        """Get an Outlook Calendar client with valid tokens."""
        access_token = self.encryption.decrypt(token.access_token_encrypted)
        refresh_token = self.encryption.decrypt(token.refresh_token_encrypted)

        # Always try to refresh if token is expired or close to expiry (5 min buffer)
        from datetime import timedelta

        if datetime.utcnow() >= (token.expires_at - timedelta(minutes=5)):
            logger.info(f"Outlook token expired or expiring soon for user {user.id}, refreshing...")
            client = OutlookCalendarClient(
                access_token=access_token,
                refresh_token=refresh_token,
            )
            new_tokens = await client.refresh_access_token()
            if new_tokens:
                await self.token_repo.save_token(
                    user_id=user.id,
                    provider="outlook",
                    access_token_encrypted=self.encryption.encrypt(new_tokens["access_token"]),
                    refresh_token_encrypted=self.encryption.encrypt(
                        new_tokens.get("refresh_token") or refresh_token
                    ),
                    expires_at=new_tokens["expires_at"],
                )
                access_token = new_tokens["access_token"]
                logger.info(f"Outlook token refreshed successfully for user {user.id}")
            else:
                logger.error(f"Outlook token refresh failed for user {user.id}")
                return {
                    "error": "Failed to refresh Outlook token. Please /disconnectoutlook and /connectoutlook again."
                }

        return (
            OutlookCalendarClient(
                access_token=access_token,
                refresh_token=refresh_token,
            ),
            token.calendar_id or "primary",
            "outlook",
        )

    async def _handle_api_error(
        self, result: dict, user: User, retry_func, provider: str = "google"
    ) -> dict:
        """Handle API errors, refreshing token and retrying on 401."""
        if result.get("code") == 401:
            logger.info(
                f"Got 401 for user {user.id} (provider={provider}), forcing token refresh..."
            )
            # Force token refresh by setting expiry to past
            token = await self.token_repo.get_token(user.id, provider)
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
        generate_teams_link: bool = False,
        custom_link: str | None = None,
    ) -> dict:
        """Create a meeting on user's calendar.

        Args:
            user: The user creating the meeting.
            meeting_data: Parsed meeting data.
            generate_meet_link: If True, auto-generate a Google Meet link (Google only).
            generate_zoom_link: If True, create a Zoom meeting and add the link.
            generate_teams_link: If True, auto-generate a Microsoft Teams link (Outlook only).
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
        client, calendar_id, provider = client_result

        # Keep times in user's local timezone for calendar API
        start_local = meeting_data.start_datetime
        end_local = meeting_data.end_datetime

        # Determine reminders to use
        reminders = self._resolve_reminders(user, meeting_data)

        # Create event based on provider
        if provider == "google":
            google_client = cast(GoogleCalendarClient, client)

            async def do_create():
                return await google_client.create_event(
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

        else:  # outlook
            outlook_client = cast(OutlookCalendarClient, client)

            async def do_create():
                return await outlook_client.create_event(
                    summary=meeting_data.title,
                    start_time=start_local,
                    end_time=end_local,
                    attendees=meeting_data.attendees,
                    timezone=user.timezone,
                    reminders=reminders,
                    generate_teams_link=generate_teams_link,
                    custom_link=custom_link,
                )

        result = await do_create()

        # Retry on 401
        if result.get("code") == 401:
            result = await self._handle_api_error(result, user, do_create, provider)

        if "error" in result:
            return result

        # Extract Meet link from conference data if present (Google)
        meet_link = None
        if provider == "google" and "conferenceData" in result:
            for entry_point in result["conferenceData"].get("entryPoints", []):
                if entry_point.get("entryPointType") == "video":
                    meet_link = entry_point.get("uri")
                    break

        # Extract Teams link if present (Outlook)
        teams_link = None
        if provider == "outlook" and result.get("isOnlineMeeting"):
            online_meeting = result.get("onlineMeeting", {})
            teams_link = online_meeting.get("joinUrl")

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
            provider=provider,
            title=meeting_data.title,
            start_time=start_utc_naive,
            end_time=end_utc_naive,
            attendees=meeting_data.attendees,
            reminders=reminders if reminders else None,
        )

        return {
            "success": True,
            "event_id": result["id"],
            "link": result.get("htmlLink") or result.get("webLink", ""),
            "title": meeting_data.title,
            "start": meeting_data.start_datetime,
            "end": meeting_data.end_datetime,
            "attendees": meeting_data.attendees,
            "reminders": reminders,
            "meet_link": meet_link,
            "teams_link": teams_link,
            "zoom_link": zoom_link,
            "custom_link": custom_link if not zoom_link else None,
            "provider": provider,
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

    async def is_privacy_mode(self, user: User, provider: str | None = None) -> bool:
        """Check if user is connected in privacy mode (no calendar read access).

        Args:
            user: The user to check
            provider: Optional provider to check. If None, checks Google then Outlook.
        """
        if provider:
            token = await self.token_repo.get_token(user.id, provider)
            return token is not None and token.privacy_mode

        # Check Google first, then Outlook
        google_token = await self.token_repo.get_token(user.id, "google")
        if google_token:
            return google_token.privacy_mode

        outlook_token = await self.token_repo.get_token(user.id, "outlook")
        if outlook_token:
            return outlook_token.privacy_mode

        return False

    async def get_calendar_provider(self, user: User) -> str | None:
        """Get which calendar provider the user has connected (respects preference).

        Returns 'google', 'outlook', or None.
        """
        google = await self.token_repo.get_token(user.id, "google")
        outlook = await self.token_repo.get_token(user.id, "outlook")

        # Respect user preference
        if user.default_calendar == "google" and google:
            return "google"
        if user.default_calendar == "outlook" and outlook:
            return "outlook"

        # Fallback
        if google:
            return "google"
        if outlook:
            return "outlook"
        return None

    async def get_connected_providers(self, user: User) -> list[str]:
        """Get list of all connected calendar providers.

        Returns list like ['google', 'outlook'] or ['google'] or [].
        """
        providers = []
        if await self.token_repo.get_token(user.id, "google"):
            providers.append("google")
        if await self.token_repo.get_token(user.id, "outlook"):
            providers.append("outlook")
        return providers

    async def switch_meeting_calendar(
        self,
        user: User,
        event_id: str,
        from_provider: str,
        to_provider: str,
        meeting_data: dict,
    ) -> dict:
        """Move a meeting from one calendar to another.

        Deletes from source calendar, creates in destination calendar.

        Args:
            user: The user.
            event_id: The event ID in the source calendar.
            from_provider: Source calendar ('google' or 'outlook').
            to_provider: Destination calendar ('google' or 'outlook').
            meeting_data: Dict with title, start_time, end_time, attendees, etc.

        Returns dict with new event details or error.
        """
        # Get destination client
        dest_result = await self._get_valid_client(user, force_provider=to_provider)
        if isinstance(dest_result, dict):
            return dest_result  # Error

        dest_client, dest_calendar_id, _ = dest_result

        # Create in destination first (so we don't lose the meeting if delete fails)
        start_time = meeting_data.get("start_time")
        end_time = meeting_data.get("end_time")
        title = meeting_data.get("title", "(No title)")
        attendees = meeting_data.get("attendees", [])

        if to_provider == "google":
            google_client = cast(GoogleCalendarClient, dest_client)
            create_result = await google_client.create_event(
                summary=title,
                start_time=start_time,
                end_time=end_time,
                attendees=attendees,
                timezone=user.timezone,
                calendar_id=dest_calendar_id,
            )
        else:  # outlook
            outlook_client = cast(OutlookCalendarClient, dest_client)
            create_result = await outlook_client.create_event(
                summary=title,
                start_time=start_time,
                end_time=end_time,
                attendees=attendees,
                timezone=user.timezone,
            )

        if "error" in create_result:
            return {"error": f"Failed to create in {to_provider}: {create_result.get('error')}"}

        new_event_id = create_result.get("id")

        # Delete from source
        source_result = await self._get_valid_client(user, force_provider=from_provider)
        if not isinstance(source_result, dict):
            source_client, source_calendar_id, _ = source_result
            if from_provider == "google":
                google_client = cast(GoogleCalendarClient, source_client)
                await google_client.delete_event(event_id=event_id, calendar_id=source_calendar_id)
            else:  # outlook
                outlook_client = cast(OutlookCalendarClient, source_client)
                await outlook_client.delete_event(event_id=event_id)

            # Update local cache
            await self.meeting_repo.delete_by_external_id(user.id, event_id, from_provider)

        # Cache new meeting
        start_utc = TimezoneHelper.to_utc(start_time, user.timezone)
        end_utc = TimezoneHelper.to_utc(end_time, user.timezone)
        await self.meeting_repo.save_meeting(
            user_id=user.id,
            external_id=new_event_id,
            provider=to_provider,
            title=title,
            start_time=start_utc.replace(tzinfo=None),
            end_time=end_utc.replace(tzinfo=None),
            attendees=attendees,
        )

        # Extract meeting link
        meet_link = None
        teams_link = None
        if to_provider == "google" and "conferenceData" in create_result:
            for ep in create_result["conferenceData"].get("entryPoints", []):
                if ep.get("entryPointType") == "video":
                    meet_link = ep.get("uri")
                    break
        elif to_provider == "outlook" and create_result.get("isOnlineMeeting"):
            teams_link = create_result.get("onlineMeeting", {}).get("joinUrl")

        return {
            "success": True,
            "event_id": new_event_id,
            "provider": to_provider,
            "title": title,
            "link": create_result.get("htmlLink") or create_result.get("webLink", ""),
            "meet_link": meet_link,
            "teams_link": teams_link,
        }

    async def get_upcoming_meetings(
        self, user: User, limit: int = 10
    ) -> tuple[list[dict], bool, str | None]:
        """Get upcoming meetings.

        In privacy mode: returns only bot-created meetings from local DB.
        In full access mode: returns meetings from calendar API.

        Returns:
            Tuple of (meetings list, is_privacy_mode flag, error message or None)
        """
        # Check if user is in privacy mode
        privacy_mode = await self.is_privacy_mode(user)

        if privacy_mode:
            # Privacy mode: fetch from local database only
            return await self._get_local_meetings(user, limit), True, None

        # Full access mode: fetch from calendar API
        client_result = await self._get_valid_client(user)
        if isinstance(client_result, dict):
            # Return the error message so the caller can display it
            return [], False, client_result.get("error")
        client, calendar_id, provider = client_result

        if provider == "google":
            google_client = cast(GoogleCalendarClient, client)

            async def do_list():
                return await google_client.list_events(
                    calendar_id=calendar_id,
                    time_min=datetime.utcnow(),
                    max_results=limit,
                )

        else:  # outlook
            outlook_client = cast(OutlookCalendarClient, client)

            async def do_list():
                return await outlook_client.list_events(
                    time_min=datetime.utcnow(),
                    max_results=limit,
                )

        result = await do_list()

        # Retry on 401
        if result.get("code") == 401:
            result = await self._handle_api_error(result, user, do_list, provider)

        if "error" in result:
            logger.error(f"Failed to list events for user {user.id}: {result}")
            return [], False, result.get("error")

        events = result.get("items", [])
        meetings = []

        for event in events:
            if provider == "google":
                meeting = self._parse_google_event(event, user)
            else:  # outlook
                meeting = self._parse_outlook_event(event, user)

            if meeting:
                meetings.append(meeting)

        return meetings, False, None

    def _parse_google_event(self, event: dict, user: User) -> dict | None:
        """Parse a Google Calendar event into a meeting dict."""
        start_data = event.get("start", {})
        end_data = event.get("end", {})

        # Handle both dateTime (timed events) and date (all-day events)
        start_str = start_data.get("dateTime") or start_data.get("date")
        end_str = end_data.get("dateTime") or end_data.get("date")

        if not start_str or not end_str:
            return None

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

        return {
            "id": event.get("id"),
            "external_id": event.get("id"),
            "title": event.get("summary", "(No title)"),
            "start_time": start_time,
            "end_time": end_time,
            "attendees": attendees,
            "link": meet_link,
            "provider": "google",
        }

    def _parse_outlook_event(self, event: dict, user: User) -> dict | None:
        """Parse an Outlook Calendar event into a meeting dict."""
        start_data = event.get("start", {})
        end_data = event.get("end", {})

        start_str = start_data.get("dateTime")
        end_str = end_data.get("dateTime")

        if not start_str or not end_str:
            return None

        # Parse datetime - Outlook returns ISO format
        from dateutil import parser as dateutil_parser

        start_time = dateutil_parser.isoparse(start_str)
        end_time = dateutil_parser.isoparse(end_str)

        # Outlook doesn't include timezone in dateTime, use the timeZone field
        event_tz = start_data.get("timeZone", user.timezone)
        if not start_time.tzinfo:
            event_tz_obj = TimezoneHelper.get_timezone(event_tz)
            start_time = start_time.replace(tzinfo=event_tz_obj)
            end_time = end_time.replace(tzinfo=event_tz_obj)

        # Convert to user's timezone for display
        start_time = start_time.astimezone(TimezoneHelper.get_timezone(user.timezone))
        end_time = end_time.astimezone(TimezoneHelper.get_timezone(user.timezone))

        attendees = [
            a.get("emailAddress", {}).get("address", "") for a in event.get("attendees", [])
        ]

        # Extract Teams link if present
        meeting_link = None
        if event.get("isOnlineMeeting"):
            online_meeting = event.get("onlineMeeting", {})
            meeting_link = online_meeting.get("joinUrl")

        return {
            "id": event.get("id"),
            "external_id": event.get("id"),
            "title": event.get("subject", "(No title)"),
            "start_time": start_time,
            "end_time": end_time,
            "attendees": attendees,
            "link": meeting_link,
            "provider": "outlook",
        }

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
        generate_teams_link: bool = False,
    ) -> dict:
        """Update an existing meeting.

        Args:
            user: The user updating the meeting.
            event_id: Calendar event ID.
            title: New title (or None to keep existing).
            start_time: New start time in user's timezone (or None to keep).
            end_time: New end time in user's timezone (or None to keep).
            attendees: New attendee list (or None to keep).
            custom_link: Custom meeting link (or None to keep).
            generate_meet_link: If True, add Google Meet link (Google only).
            generate_teams_link: If True, add Teams link (Outlook only).

        Returns dict with updated meeting details or error.
        """
        client_result = await self._get_valid_client(user)
        if isinstance(client_result, dict):
            return client_result  # Error
        client, calendar_id, provider = client_result

        if provider == "google":
            google_client = cast(GoogleCalendarClient, client)

            async def do_update():
                return await google_client.update_event(
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

        else:  # outlook
            outlook_client = cast(OutlookCalendarClient, client)

            async def do_update():
                return await outlook_client.update_event(
                    event_id=event_id,
                    summary=title,
                    start_time=start_time,
                    end_time=end_time,
                    timezone=user.timezone,
                    attendees=attendees,
                    custom_link=custom_link,
                    generate_teams_link=generate_teams_link,
                )

        result = await do_update()

        # Retry on 401
        if result.get("code") == 401:
            result = await self._handle_api_error(result, user, do_update, provider)

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
                user.id, event_id, provider, **local_updates
            )

        # Extract Meet link from response if present (Google)
        meet_link = None
        if provider == "google" and "conferenceData" in result:
            for entry_point in result["conferenceData"].get("entryPoints", []):
                if entry_point.get("entryPointType") == "video":
                    meet_link = entry_point.get("uri")
                    break

        # Extract Teams link from response if present (Outlook)
        teams_link = None
        if provider == "outlook" and result.get("isOnlineMeeting"):
            online_meeting = result.get("onlineMeeting", {})
            teams_link = online_meeting.get("joinUrl")

        return {
            "success": True,
            "event_id": result.get("id"),
            "title": result.get("summary") or result.get("subject", "(No title)"),
            "meet_link": meet_link,
            "teams_link": teams_link,
            "provider": provider,
        }

    async def create_zoom_link(
        self,
        user: User,
        title: str,
        start_time: datetime,
        duration_minutes: int,
    ) -> dict:
        """Create a Zoom meeting link.

        Args:
            user: The user creating the Zoom meeting.
            title: Meeting title.
            start_time: Meeting start time.
            duration_minutes: Meeting duration in minutes.

        Returns dict with zoom_link on success, or error.
        """
        token = await self.token_repo.get_token(user.id, "zoom")
        if not token:
            return {"error": "Zoom not connected. Use /connect to link your Zoom account."}

        access_token = self.encryption.decrypt(token.access_token_encrypted)
        refresh_token = self.encryption.decrypt(token.refresh_token_encrypted)

        zoom_client = ZoomClient(access_token=access_token, refresh_token=refresh_token)

        result = await zoom_client.create_meeting(
            topic=title,
            start_time=start_time,
            duration=duration_minutes,
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
                        topic=title,
                        start_time=start_time,
                        duration=duration_minutes,
                        timezone=user.timezone,
                    )

            if "error" in result:
                logger.error(f"Failed to create Zoom meeting for user {user.id}: {result}")
                return {"error": "Failed to create Zoom meeting. Please try reconnecting Zoom."}

        return {"success": True, "zoom_link": result.get("join_url")}

    async def cancel_meeting(self, user: User, event_id: str) -> dict:
        """Cancel a meeting by calendar event ID."""
        client_result = await self._get_valid_client(user)
        if isinstance(client_result, dict):
            return client_result  # Error
        client, calendar_id, provider = client_result

        # Get event details first (for the title in response)
        if provider == "google":
            google_client = cast(GoogleCalendarClient, client)
            event = await google_client.get_event(event_id=event_id, calendar_id=calendar_id)
        else:  # outlook
            outlook_client = cast(OutlookCalendarClient, client)
            event = await outlook_client.get_event(event_id=event_id)

        if "error" in event:
            return {"error": "Meeting not found"}

        # Get title (different field names for Google vs Outlook)
        title = event.get("summary") or event.get("subject", "(No title)")

        # Delete from calendar
        if provider == "google":
            google_client = cast(GoogleCalendarClient, client)

            async def do_delete():
                return await google_client.delete_event(event_id=event_id, calendar_id=calendar_id)

        else:  # outlook
            outlook_client = cast(OutlookCalendarClient, client)

            async def do_delete():
                return await outlook_client.delete_event(event_id=event_id)

        result = await do_delete()

        # Retry on 401
        if result.get("code") == 401:
            result = await self._handle_api_error(result, user, do_delete, provider)

        if "error" in result:
            return result

        # Remove from local cache if exists
        await self.meeting_repo.delete_by_external_id(user.id, event_id, provider)

        return {"success": True, "title": title}
