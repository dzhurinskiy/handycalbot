"""Calendar service for managing meetings."""

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from calendarbot.db.models import User
from calendarbot.db.repository import MeetingRepository, OAuthTokenRepository
from calendarbot.integrations.google import GoogleCalendarClient
from calendarbot.services.parser import ParsedMeeting
from calendarbot.utils.encryption import TokenEncryption
from calendarbot.utils.timezone import TimezoneHelper


class CalendarService:
    """Business logic for calendar operations."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.meeting_repo = MeetingRepository(session)
        self.token_repo = OAuthTokenRepository(session)
        self.encryption = TokenEncryption()

    async def create_meeting(
        self, user: User, meeting_data: ParsedMeeting
    ) -> dict:
        """Create a meeting on user's calendar.

        Returns dict with meeting details or error.
        """
        # Get user's Google token
        token = await self.token_repo.get_token(user.id, "google")
        if not token:
            return {"error": "Google Calendar not connected. Use /connect to link your calendar."}

        # Decrypt tokens
        access_token = self.encryption.decrypt(token.access_token_encrypted)
        refresh_token = self.encryption.decrypt(token.refresh_token_encrypted)

        # Check if token needs refresh
        if datetime.utcnow() >= token.expires_at:
            # Refresh the token
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
                        new_tokens.get("refresh_token", refresh_token)
                    ),
                    expires_at=new_tokens["expires_at"],
                )
                access_token = new_tokens["access_token"]

        # Keep times in user's local timezone for Google API
        # (Google handles timezone conversion when we specify the timeZone field)
        start_local = meeting_data.start_datetime
        end_local = meeting_data.end_datetime

        # Create event via Google Calendar API
        client = GoogleCalendarClient(access_token=access_token, refresh_token=refresh_token)
        result = await client.create_event(
            summary=meeting_data.title,
            start_time=start_local,
            end_time=end_local,
            attendees=meeting_data.attendees,
            timezone=user.timezone,
            calendar_id=token.calendar_id or "primary",
        )

        if "error" in result:
            return result

        # Convert to UTC for local cache storage
        start_utc = TimezoneHelper.to_utc(meeting_data.start_datetime, user.timezone)
        end_utc = TimezoneHelper.to_utc(meeting_data.end_datetime, user.timezone)

        # Cache meeting locally
        await self.meeting_repo.save_meeting(
            user_id=user.id,
            external_id=result["id"],
            provider="google",
            title=meeting_data.title,
            start_time=start_utc,
            end_time=end_utc,
            attendees=meeting_data.attendees,
        )

        return {
            "success": True,
            "event_id": result["id"],
            "link": result.get("htmlLink", ""),
            "title": meeting_data.title,
            "start": meeting_data.start_datetime,
            "end": meeting_data.end_datetime,
            "attendees": meeting_data.attendees,
        }

    async def get_upcoming_meetings(
        self, user: User, limit: int = 10
    ) -> list[dict]:
        """Get upcoming meetings from Google Calendar."""
        # Get user's Google token
        token = await self.token_repo.get_token(user.id, "google")
        if not token:
            return []

        # Decrypt tokens
        access_token = self.encryption.decrypt(token.access_token_encrypted)
        refresh_token = self.encryption.decrypt(token.refresh_token_encrypted)

        # Check if token needs refresh
        if datetime.utcnow() >= token.expires_at:
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
                        new_tokens.get("refresh_token", refresh_token)
                    ),
                    expires_at=new_tokens["expires_at"],
                )
                access_token = new_tokens["access_token"]

        # Fetch from Google Calendar API
        client = GoogleCalendarClient(access_token=access_token, refresh_token=refresh_token)
        result = await client.list_events(
            calendar_id=token.calendar_id or "primary",
            time_min=datetime.utcnow(),
            max_results=limit,
        )

        if "error" in result:
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

            meetings.append({
                "id": event.get("id"),
                "external_id": event.get("id"),
                "title": event.get("summary", "(No title)"),
                "start_time": start_time,
                "end_time": end_time,
                "attendees": attendees,
            })

        return meetings

    async def cancel_meeting(self, user: User, event_id: str) -> dict:
        """Cancel a meeting by Google event ID."""
        # Get token
        token = await self.token_repo.get_token(user.id, "google")
        if not token:
            return {"error": "Google Calendar not connected"}

        access_token = self.encryption.decrypt(token.access_token_encrypted)
        refresh_token = self.encryption.decrypt(token.refresh_token_encrypted)

        # Check if token needs refresh
        if datetime.utcnow() >= token.expires_at:
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
                        new_tokens.get("refresh_token", refresh_token)
                    ),
                    expires_at=new_tokens["expires_at"],
                )
                access_token = new_tokens["access_token"]

        # Get event details first (for the title in response)
        client = GoogleCalendarClient(access_token=access_token, refresh_token=refresh_token)
        event = await client.get_event(
            event_id=event_id,
            calendar_id=token.calendar_id or "primary",
        )

        if "error" in event:
            return {"error": "Meeting not found"}

        title = event.get("summary", "(No title)")

        # Delete from Google Calendar
        result = await client.delete_event(
            event_id=event_id,
            calendar_id=token.calendar_id or "primary",
        )

        if "error" in result:
            return result

        # Remove from local cache if exists
        await self.meeting_repo.delete_by_external_id(user.id, event_id, "google")

        return {"success": True, "title": title}
