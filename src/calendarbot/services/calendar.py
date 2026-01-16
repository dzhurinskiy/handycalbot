"""Calendar service for managing meetings."""

import logging
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from calendarbot.db.models import User
from calendarbot.db.repository import MeetingRepository, OAuthTokenRepository
from calendarbot.integrations.google import GoogleCalendarClient
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

    async def create_meeting(self, user: User, meeting_data: ParsedMeeting) -> dict:
        """Create a meeting on user's calendar.

        Returns dict with meeting details or error.
        """
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
            )

        result = await do_create()

        # Retry on 401
        if result.get("code") == 401:
            result = await self._handle_api_error(result, user, do_create)

        if "error" in result:
            return result

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

    async def get_upcoming_meetings(self, user: User, limit: int = 10) -> list[dict]:
        """Get upcoming meetings from Google Calendar."""
        client_result = await self._get_valid_client(user)
        if isinstance(client_result, dict):
            return []  # No calendar connected or token error
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
            return []

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

            meetings.append(
                {
                    "id": event.get("id"),
                    "external_id": event.get("id"),
                    "title": event.get("summary", "(No title)"),
                    "start_time": start_time,
                    "end_time": end_time,
                    "attendees": attendees,
                }
            )

        return meetings

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
