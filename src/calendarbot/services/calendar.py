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

        # Convert to UTC for API
        start_utc = TimezoneHelper.to_utc(meeting_data.start_datetime, user.timezone)
        end_utc = TimezoneHelper.to_utc(meeting_data.end_datetime, user.timezone)

        # Create event via Google Calendar API
        client = GoogleCalendarClient(access_token=access_token)
        result = await client.create_event(
            summary=meeting_data.title,
            start_time=start_utc,
            end_time=end_utc,
            attendees=meeting_data.attendees,
            timezone=user.timezone,
            calendar_id=token.calendar_id or "primary",
        )

        if "error" in result:
            return result

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
        """Get upcoming meetings for user."""
        meetings = await self.meeting_repo.get_upcoming(user.id, limit=limit)

        return [
            {
                "id": m.id,
                "external_id": m.external_id,
                "title": m.title,
                "start_time": TimezoneHelper.from_utc(m.start_time, user.timezone),
                "end_time": TimezoneHelper.from_utc(m.end_time, user.timezone),
                "attendees": m.attendees.get("emails", []) if m.attendees else [],
            }
            for m in meetings
        ]

    async def cancel_meeting(self, user: User, meeting_id: int) -> dict:
        """Cancel a meeting."""
        # Get token
        token = await self.token_repo.get_token(user.id, "google")
        if not token:
            return {"error": "Google Calendar not connected"}

        access_token = self.encryption.decrypt(token.access_token_encrypted)

        # Get meeting from local cache
        meetings = await self.meeting_repo.get_upcoming(user.id)
        meeting = next((m for m in meetings if m.id == meeting_id), None)

        if not meeting:
            return {"error": "Meeting not found"}

        # Delete from Google Calendar
        client = GoogleCalendarClient(access_token=access_token)
        result = await client.delete_event(
            event_id=meeting.external_id,
            calendar_id=token.calendar_id or "primary",
        )

        if "error" in result:
            return result

        # Remove from local cache
        await self.meeting_repo.delete_by_external_id(
            user.id, meeting.external_id, "google"
        )

        return {"success": True, "title": meeting.title}
