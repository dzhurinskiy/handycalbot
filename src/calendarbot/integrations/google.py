"""Google Calendar API integration."""

import logging
import uuid
from datetime import datetime, timedelta

import httpx

from calendarbot.config import get_settings

logger = logging.getLogger(__name__)

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_CALENDAR_API = "https://www.googleapis.com/calendar/v3"
GOOGLE_USERINFO_API = "https://www.googleapis.com/oauth2/v2/userinfo"


class GoogleCalendarClient:
    """Client for Google Calendar API."""

    def __init__(
        self,
        access_token: str,
        refresh_token: str | None = None,
    ):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.settings = get_settings()

    async def _request(
        self,
        method: str,
        url: str,
        **kwargs,
    ) -> dict:
        """Make authenticated request to Google API."""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                timeout=30.0,
                **kwargs,
            )

            if response.status_code == 401:
                return {"error": "Token expired", "code": 401}

            if response.status_code >= 400:
                logger.error(f"Google API error: {response.status_code} - {response.text}")
                return {"error": f"API error: {response.status_code}", "code": response.status_code}

            if response.status_code == 204:
                return {"success": True}

            return response.json()

    async def refresh_access_token(self) -> dict | None:
        """Refresh the access token using refresh token."""
        if not self.refresh_token:
            return None

        async with httpx.AsyncClient() as client:
            response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "client_id": self.settings.google_client_id,
                    "client_secret": self.settings.google_client_secret,
                    "refresh_token": self.refresh_token,
                    "grant_type": "refresh_token",
                },
            )

            if response.status_code != 200:
                logger.error(f"Token refresh failed: {response.text}")
                return None

            data = response.json()
            expires_at = datetime.utcnow() + timedelta(seconds=data.get("expires_in", 3600))

            return {
                "access_token": data["access_token"],
                "refresh_token": data.get("refresh_token"),  # May be None, caller handles fallback
                "expires_at": expires_at,
            }

    async def create_event(
        self,
        summary: str,
        start_time: datetime,
        end_time: datetime,
        attendees: list[str] | None = None,
        description: str | None = None,
        timezone: str = "UTC",
        calendar_id: str = "primary",
        reminders: list[int] | None = None,
        generate_meet_link: bool = False,
        custom_link: str | None = None,
    ) -> dict:
        """Create a calendar event.

        Args:
            reminders: List of reminder times in minutes before the event.
                       None means use calendar default, empty list means no reminders.
            generate_meet_link: If True, auto-generate a Google Meet link.
            custom_link: Custom meeting link to add to description.
        """
        event_body: dict = {
            "summary": summary,
            "start": {
                "dateTime": start_time.isoformat(),
                "timeZone": timezone,
            },
            "end": {
                "dateTime": end_time.isoformat(),
                "timeZone": timezone,
            },
        }

        # Handle description with optional custom link
        if custom_link:
            link_text = f"Meeting Link: {custom_link}"
            if description:
                event_body["description"] = f"{description}\n\n{link_text}"
            else:
                event_body["description"] = link_text
        elif description:
            event_body["description"] = description

        if attendees:
            event_body["attendees"] = [{"email": email} for email in attendees]
            event_body["sendUpdates"] = "all"  # Send invitations
            logger.info(f"Creating event with attendees: {attendees}")

        # Handle reminders
        if reminders is not None:
            if reminders:
                # Specific reminders requested
                event_body["reminders"] = {
                    "useDefault": False,
                    "overrides": [{"method": "popup", "minutes": m} for m in reminders],
                }
            else:
                # Empty list means no reminders
                event_body["reminders"] = {"useDefault": False, "overrides": []}
        # If reminders is None, don't set it - use calendar default

        # Add Google Meet conference data if requested
        if generate_meet_link:
            event_body["conferenceData"] = {
                "createRequest": {
                    "requestId": str(uuid.uuid4()),
                    "conferenceSolutionKey": {"type": "hangoutsMeet"},
                }
            }

        url = f"{GOOGLE_CALENDAR_API}/calendars/{calendar_id}/events"
        # Add conferenceDataVersion param if generating Meet link
        params = {"conferenceDataVersion": "1"} if generate_meet_link else None
        result = await self._request("POST", url, json=event_body, params=params)

        # Log the response to verify event creation
        if "error" in result:
            logger.error(f"Google Calendar API error: {result}")
        else:
            event_id = result.get("id", "unknown")
            created_attendees = [a.get("email") for a in result.get("attendees", [])]
            logger.info(f"Event created: id={event_id}, attendees_in_response={created_attendees}")

        return result

    async def get_event(self, event_id: str, calendar_id: str = "primary") -> dict:
        """Get a single event."""
        url = f"{GOOGLE_CALENDAR_API}/calendars/{calendar_id}/events/{event_id}"
        return await self._request("GET", url)

    async def delete_event(self, event_id: str, calendar_id: str = "primary") -> dict:
        """Delete a calendar event."""
        url = f"{GOOGLE_CALENDAR_API}/calendars/{calendar_id}/events/{event_id}"
        return await self._request("DELETE", url)

    async def list_events(
        self,
        calendar_id: str = "primary",
        time_min: datetime | None = None,
        time_max: datetime | None = None,
        max_results: int = 10,
    ) -> dict:
        """List calendar events."""
        params = {
            "maxResults": max_results,
            "singleEvents": "true",
            "orderBy": "startTime",
        }

        if time_min:
            params["timeMin"] = time_min.isoformat() + "Z"
        if time_max:
            params["timeMax"] = time_max.isoformat() + "Z"

        url = f"{GOOGLE_CALENDAR_API}/calendars/{calendar_id}/events"
        return await self._request("GET", url, params=params)

    async def list_calendars(self) -> dict:
        """List user's calendars."""
        url = f"{GOOGLE_CALENDAR_API}/users/me/calendarList"
        return await self._request("GET", url)

    async def get_user_email(self) -> str | None:
        """Get the user's email from their Google account."""
        result = await self._request("GET", GOOGLE_USERINFO_API)
        if "error" in result:
            logger.error(f"Failed to get user email: {result}")
            return None
        email = result.get("email")
        if not email:
            logger.warning(f"Userinfo response missing email field: {result}")
        return email


class GoogleOAuthFlow:
    """Handle Google OAuth2 flow."""

    SCOPES = [
        "https://www.googleapis.com/auth/calendar.events",
        "https://www.googleapis.com/auth/calendar.readonly",
        "https://www.googleapis.com/auth/userinfo.email",
    ]
    AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"

    def __init__(self):
        self.settings = get_settings()

    def get_authorization_url(self, state: str) -> str:
        """Generate OAuth authorization URL."""
        params = {
            "client_id": self.settings.google_client_id,
            "redirect_uri": self.settings.google_redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.SCOPES),
            "access_type": "offline",
            "prompt": "consent",
            "state": state,
        }

        query = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{self.AUTH_URL}?{query}"

    async def exchange_code(self, code: str) -> dict | None:
        """Exchange authorization code for tokens."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "client_id": self.settings.google_client_id,
                    "client_secret": self.settings.google_client_secret,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": self.settings.google_redirect_uri,
                },
            )

            if response.status_code != 200:
                logger.error(f"Token exchange failed: {response.text}")
                return None

            data = response.json()
            expires_at = datetime.utcnow() + timedelta(seconds=data.get("expires_in", 3600))

            return {
                "access_token": data["access_token"],
                "refresh_token": data.get("refresh_token") or "",
                "expires_at": expires_at,
            }
