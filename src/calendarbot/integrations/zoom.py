"""Zoom API integration."""

import base64
import logging
from datetime import datetime, timedelta

import httpx

from calendarbot.config import get_settings

logger = logging.getLogger(__name__)

ZOOM_AUTH_URL = "https://zoom.us/oauth/authorize"
ZOOM_TOKEN_URL = "https://zoom.us/oauth/token"
ZOOM_API_URL = "https://api.zoom.us/v2"


class ZoomClient:
    """Client for Zoom API."""

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
        """Make authenticated request to Zoom API."""
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
                logger.error(f"Zoom API error: {response.status_code} - {response.text}")
                return {"error": f"API error: {response.status_code}", "code": response.status_code}

            if response.status_code == 204:
                return {"success": True}

            return response.json()

    async def refresh_access_token(self) -> dict | None:
        """Refresh the access token using refresh token."""
        if not self.refresh_token:
            return None

        # Zoom uses Basic Auth for token refresh
        credentials = f"{self.settings.zoom_client_id}:{self.settings.zoom_client_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                ZOOM_TOKEN_URL,
                headers={
                    "Authorization": f"Basic {encoded}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.refresh_token,
                },
            )

            if response.status_code != 200:
                logger.error(f"Zoom token refresh failed: {response.text}")
                return None

            data = response.json()
            expires_at = datetime.utcnow() + timedelta(seconds=data.get("expires_in", 3600))

            return {
                "access_token": data["access_token"],
                "refresh_token": data.get("refresh_token", self.refresh_token),
                "expires_at": expires_at,
            }

    async def get_user_info(self) -> dict:
        """Get the current user's info."""
        url = f"{ZOOM_API_URL}/users/me"
        return await self._request("GET", url)

    async def create_meeting(
        self,
        topic: str,
        start_time: datetime,
        duration: int = 60,
        timezone: str = "UTC",
        agenda: str | None = None,
        password: str | None = None,
    ) -> dict:
        """Create a Zoom meeting.

        Args:
            topic: Meeting title
            start_time: Meeting start time
            duration: Duration in minutes
            timezone: Timezone string
            agenda: Optional meeting description
            password: Optional meeting password (auto-generated if not provided)

        Returns:
            dict with meeting details including join_url
        """
        meeting_body = {
            "topic": topic,
            "type": 2,  # Scheduled meeting
            "start_time": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "duration": duration,
            "timezone": timezone,
            "settings": {
                "join_before_host": True,
                "waiting_room": False,
                "mute_upon_entry": False,
                "auto_recording": "none",
            },
        }

        if agenda:
            meeting_body["agenda"] = agenda

        if password:
            meeting_body["password"] = password

        url = f"{ZOOM_API_URL}/users/me/meetings"
        result = await self._request("POST", url, json=meeting_body)

        if "error" not in result:
            logger.info(f"Created Zoom meeting: {result.get('id')} - {result.get('join_url')}")

        return result

    async def get_meeting(self, meeting_id: str) -> dict:
        """Get meeting details."""
        url = f"{ZOOM_API_URL}/meetings/{meeting_id}"
        return await self._request("GET", url)

    async def delete_meeting(self, meeting_id: str) -> dict:
        """Delete a meeting."""
        url = f"{ZOOM_API_URL}/meetings/{meeting_id}"
        return await self._request("DELETE", url)


class ZoomOAuthFlow:
    """Handle Zoom OAuth2 flow."""

    SCOPES = ["meeting:write", "user:read"]

    def __init__(self):
        self.settings = get_settings()

    def get_authorization_url(self, state: str) -> str:
        """Generate OAuth authorization URL."""
        params = {
            "client_id": self.settings.zoom_client_id,
            "redirect_uri": self.settings.zoom_redirect_uri,
            "response_type": "code",
            "state": state,
        }

        query = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{ZOOM_AUTH_URL}?{query}"

    async def exchange_code(self, code: str) -> dict | None:
        """Exchange authorization code for tokens."""
        # Zoom uses Basic Auth for token exchange
        credentials = f"{self.settings.zoom_client_id}:{self.settings.zoom_client_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                ZOOM_TOKEN_URL,
                headers={
                    "Authorization": f"Basic {encoded}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": self.settings.zoom_redirect_uri,
                },
            )

            if response.status_code != 200:
                logger.error(f"Zoom token exchange failed: {response.text}")
                return None

            data = response.json()
            expires_at = datetime.utcnow() + timedelta(seconds=data.get("expires_in", 3600))

            return {
                "access_token": data["access_token"],
                "refresh_token": data.get("refresh_token", ""),
                "expires_at": expires_at,
            }
