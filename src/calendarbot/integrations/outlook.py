"""Microsoft Outlook Calendar API integration via Microsoft Graph."""

import logging
from datetime import datetime, timedelta
from urllib.parse import urlencode

import httpx

from calendarbot.config import get_settings

logger = logging.getLogger(__name__)

MICROSOFT_AUTH_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
MICROSOFT_TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
GRAPH_API_URL = "https://graph.microsoft.com/v1.0"


class OutlookCalendarClient:
    """Client for Microsoft Graph Calendar API."""

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
        """Make authenticated request to Microsoft Graph API."""
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
                logger.error(f"Microsoft Graph API error: {response.status_code} - {response.text}")
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
                MICROSOFT_TOKEN_URL,
                data={
                    "client_id": self.settings.outlook_client_id,
                    "client_secret": self.settings.outlook_client_secret,
                    "refresh_token": self.refresh_token,
                    "grant_type": "refresh_token",
                    "scope": " ".join(OutlookOAuthFlow.SCOPES_FULL),
                },
            )

            if response.status_code != 200:
                logger.error(f"Outlook token refresh failed: {response.text}")
                return None

            data = response.json()
            expires_at = datetime.utcnow() + timedelta(seconds=data.get("expires_in", 3600))

            return {
                "access_token": data["access_token"],
                "refresh_token": data.get("refresh_token", self.refresh_token),
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
        reminders: list[int] | None = None,
        generate_teams_link: bool = False,
        custom_link: str | None = None,
    ) -> dict:
        """Create a calendar event.

        Args:
            summary: Event title
            start_time: Event start time
            end_time: Event end time
            attendees: List of attendee email addresses
            description: Event description
            timezone: Timezone string
            reminders: List of reminder times in minutes before the event
            generate_teams_link: If True, auto-generate a Microsoft Teams meeting link
            custom_link: Custom meeting link to add to description
        """
        event_body: dict = {
            "subject": summary,
            "start": {
                "dateTime": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "timeZone": timezone,
            },
            "end": {
                "dateTime": end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "timeZone": timezone,
            },
        }

        # Handle description with optional custom link
        if custom_link:
            link_text = f"Meeting Link: {custom_link}"
            if description:
                event_body["body"] = {
                    "contentType": "text",
                    "content": f"{description}\n\n{link_text}",
                }
            else:
                event_body["body"] = {"contentType": "text", "content": link_text}
        elif description:
            event_body["body"] = {"contentType": "text", "content": description}

        if attendees:
            event_body["attendees"] = [
                {"emailAddress": {"address": email}, "type": "required"} for email in attendees
            ]
            logger.info(f"Creating Outlook event with attendees: {attendees}")

        # Handle reminders
        if reminders is not None and reminders:
            # Microsoft Graph uses a single reminder, use the first one
            event_body["reminderMinutesBeforeStart"] = reminders[0]
            event_body["isReminderOn"] = True
        else:
            event_body["isReminderOn"] = False

        # Add Microsoft Teams meeting if requested
        if generate_teams_link:
            event_body["isOnlineMeeting"] = True
            event_body["onlineMeetingProvider"] = "teamsForBusiness"

        url = f"{GRAPH_API_URL}/me/calendar/events"
        result = await self._request("POST", url, json=event_body)

        if "error" in result:
            logger.error(f"Outlook Calendar API error: {result}")
        else:
            event_id = result.get("id", "unknown")
            created_attendees = [
                a.get("emailAddress", {}).get("address") for a in result.get("attendees", [])
            ]
            logger.info(
                f"Outlook event created: id={event_id}, attendees_in_response={created_attendees}"
            )

        return result

    async def get_event(self, event_id: str) -> dict:
        """Get a single event."""
        url = f"{GRAPH_API_URL}/me/calendar/events/{event_id}"
        return await self._request("GET", url)

    async def delete_event(self, event_id: str) -> dict:
        """Delete a calendar event."""
        url = f"{GRAPH_API_URL}/me/calendar/events/{event_id}"
        return await self._request("DELETE", url)

    async def update_event(
        self,
        event_id: str,
        summary: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        timezone: str = "UTC",
        attendees: list[str] | None = None,
        description: str | None = None,
        custom_link: str | None = None,
        generate_teams_link: bool = False,
    ) -> dict:
        """Update an existing calendar event.

        Only provided fields will be updated (partial update via PATCH).
        """
        # First get the existing event to check current state
        existing = await self.get_event(event_id)
        if "error" in existing:
            return existing

        event_body: dict = {}

        if summary is not None:
            event_body["subject"] = summary

        if start_time is not None:
            event_body["start"] = {
                "dateTime": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "timeZone": timezone,
            }

        if end_time is not None:
            event_body["end"] = {
                "dateTime": end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "timeZone": timezone,
            }

        if attendees is not None:
            event_body["attendees"] = [
                {"emailAddress": {"address": email}, "type": "required"} for email in attendees
            ]

        # Handle description/custom link
        if custom_link is not None:
            link_text = f"Meeting Link: {custom_link}"
            if description:
                event_body["body"] = {
                    "contentType": "text",
                    "content": f"{description}\n\n{link_text}",
                }
            else:
                event_body["body"] = {"contentType": "text", "content": link_text}
        elif description is not None:
            event_body["body"] = {"contentType": "text", "content": description}

        # Handle Teams meeting link generation
        if generate_teams_link and not existing.get("isOnlineMeeting"):
            event_body["isOnlineMeeting"] = True
            event_body["onlineMeetingProvider"] = "teamsForBusiness"

        if not event_body:
            # Nothing to update
            return existing

        url = f"{GRAPH_API_URL}/me/calendar/events/{event_id}"
        result = await self._request("PATCH", url, json=event_body)

        if "error" in result:
            logger.error(f"Outlook Calendar update error: {result}")
        else:
            logger.info(f"Outlook event updated: id={event_id}")

        return result

    async def list_events(
        self,
        time_min: datetime | None = None,
        time_max: datetime | None = None,
        max_results: int = 10,
    ) -> dict:
        """List calendar events."""
        params = {
            "$top": max_results,
            "$orderby": "start/dateTime",
        }

        # Build filter for time range
        filters = []
        if time_min:
            filters.append(f"start/dateTime ge '{time_min.isoformat()}Z'")
        if time_max:
            filters.append(f"end/dateTime le '{time_max.isoformat()}Z'")

        if filters:
            params["$filter"] = " and ".join(filters)

        url = f"{GRAPH_API_URL}/me/calendar/events"
        result = await self._request("GET", url, params=params)

        # Transform to a consistent format with items key
        if "error" not in result and "value" in result:
            result["items"] = result.pop("value")

        return result

    async def get_user_email(self) -> str | None:
        """Get the user's email from their Microsoft account."""
        url = f"{GRAPH_API_URL}/me"
        result = await self._request("GET", url)
        if "error" in result:
            logger.error(f"Failed to get Outlook user email: {result}")
            return None
        # Microsoft Graph returns mail or userPrincipalName
        email = result.get("mail") or result.get("userPrincipalName")
        if not email:
            logger.warning(f"User info response missing email field: {result}")
        return email


class OutlookOAuthFlow:
    """Handle Microsoft OAuth2 flow for Outlook Calendar."""

    # Full access: create events + read calendar
    SCOPES_FULL = [
        "Calendars.ReadWrite",
        "OnlineMeetings.ReadWrite",
        "User.Read",
        "offline_access",
    ]
    # Privacy mode: create events only (same scopes, but we'll track privacy mode separately)
    SCOPES_PRIVACY = [
        "Calendars.ReadWrite",
        "User.Read",
        "offline_access",
    ]

    def __init__(self):
        self.settings = get_settings()

    def get_authorization_url(self, state: str, privacy_mode: bool = False) -> str:
        """Generate OAuth authorization URL.

        Args:
            state: OAuth state parameter for security
            privacy_mode: If True, use limited scopes (create only, no read)
        """
        scopes = self.SCOPES_PRIVACY if privacy_mode else self.SCOPES_FULL
        params = {
            "client_id": self.settings.outlook_client_id,
            "redirect_uri": self.settings.outlook_redirect_uri,
            "response_type": "code",
            "scope": " ".join(scopes),
            "response_mode": "query",
            "prompt": "consent",
            "state": state,
        }

        query = urlencode(params)
        return f"{MICROSOFT_AUTH_URL}?{query}"

    async def exchange_code(self, code: str) -> dict | None:
        """Exchange authorization code for tokens."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                MICROSOFT_TOKEN_URL,
                data={
                    "client_id": self.settings.outlook_client_id,
                    "client_secret": self.settings.outlook_client_secret,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": self.settings.outlook_redirect_uri,
                    "scope": " ".join(self.SCOPES_FULL),
                },
            )

            if response.status_code != 200:
                logger.error(f"Outlook token exchange failed: {response.text}")
                return None

            data = response.json()
            expires_at = datetime.utcnow() + timedelta(seconds=data.get("expires_in", 3600))

            return {
                "access_token": data["access_token"],
                "refresh_token": data.get("refresh_token") or "",
                "expires_at": expires_at,
            }
