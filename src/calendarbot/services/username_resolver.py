"""Username resolver service for @mention invites."""

import logging
from dataclasses import dataclass
from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession

from calendarbot.db.repository import (
    OAuthTokenRepository,
    UsernameLookupRepository,
    UserRepository,
)
from calendarbot.utils.encryption import TokenEncryption

logger = logging.getLogger(__name__)


class UsernameStatus(Enum):
    """Status of a resolved username."""

    REGISTERED = "registered"  # User is registered and allows invites
    PRIVACY_DISABLED = "privacy_disabled"  # User is registered but disabled invites
    NO_CALENDAR = "no_calendar"  # User is registered but hasn't connected calendar
    NOT_FOUND = "not_found"  # Username not found in our system


@dataclass
class ResolvedUser:
    """Result of resolving a username."""

    username: str
    status: UsernameStatus
    can_invite: bool
    # Note: NO email field - email is never exposed to protect privacy


@dataclass
class MeetingInviteResult:
    """Result of resolving usernames for a meeting invite."""

    # Usernames that were successfully resolved and invited (email sent)
    invited: list[str]
    # Usernames that are registered but have no calendar connected
    no_calendar: list[str]
    # Usernames that are registered but have privacy disabled
    privacy_disabled: list[str]
    # Usernames that are not registered at all
    not_found: list[str]
    # The actual emails to send invites to
    emails: list[str]


class UsernameResolverService:
    """Resolves @usernames to users while preserving privacy.

    Key privacy guarantees:
    - Emails are never exposed in resolution results
    - Only "registered" / "not_found" / "privacy_disabled" status shown
    - Rate limiting prevents username enumeration attacks
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.token_repo = OAuthTokenRepository(session)
        self.rate_limit_repo = UsernameLookupRepository(session)
        self.encryption = TokenEncryption()

    async def check_rate_limit(self, telegram_id: int, count: int = 1) -> bool:
        """Check if user is within rate limit.

        Returns True if within limit, False if rate limited.
        """
        return await self.rate_limit_repo.check_and_increment(telegram_id, count)

    async def get_remaining_lookups(self, telegram_id: int) -> int:
        """Get remaining lookups for a user in current window."""
        return await self.rate_limit_repo.get_remaining(telegram_id)

    async def resolve_usernames(
        self,
        usernames: list[str],
        requester_id: int,
    ) -> dict[str, ResolvedUser]:
        """Resolve usernames to ResolvedUser objects.

        Never exposes actual emails to the caller - only status.

        Args:
            usernames: List of usernames (without @ prefix)
            requester_id: Telegram ID of the user making the request

        Returns:
            Dict mapping username to ResolvedUser
        """
        if not usernames:
            return {}

        # Check rate limit
        if not await self.check_rate_limit(requester_id, len(usernames)):
            logger.warning(f"Rate limit exceeded for user {requester_id}")
            # Return all as "not_found" to prevent enumeration
            return {
                username: ResolvedUser(
                    username=username,
                    status=UsernameStatus.NOT_FOUND,
                    can_invite=False,
                )
                for username in usernames
            }

        # Fetch users by usernames
        users = await self.user_repo.get_users_by_usernames(usernames)

        # Build username -> user mapping (case-insensitive)
        user_map = {}
        for user in users:
            if user.telegram_username:
                user_map[user.telegram_username.lower()] = user

        # Build results
        results = {}
        for username in usernames:
            username_lower = username.lower()
            user = user_map.get(username_lower)  # type: ignore[assignment]

            if not user:
                results[username] = ResolvedUser(
                    username=username,
                    status=UsernameStatus.NOT_FOUND,
                    can_invite=False,
                )
            elif not user.allow_username_invites:
                results[username] = ResolvedUser(
                    username=username,
                    status=UsernameStatus.PRIVACY_DISABLED,
                    can_invite=False,
                )
            else:
                results[username] = ResolvedUser(
                    username=username,
                    status=UsernameStatus.REGISTERED,
                    can_invite=True,
                )

        return results

    async def get_emails_for_meeting(
        self,
        usernames: list[str],
        _requester_id: int,
    ) -> MeetingInviteResult:
        """Get actual emails for meeting creation (after user confirms).

        This is called during actual meeting creation, not preview.
        Returns detailed results showing which users:
        1. Were invited (email sent)
        2. Are registered but have no calendar
        3. Have privacy disabled
        4. Are not found (unregistered)

        Args:
            usernames: List of usernames (without @ prefix)
            requester_id: Telegram ID of the user making the request

        Returns:
            MeetingInviteResult with detailed breakdown
        """
        if not usernames:
            return MeetingInviteResult(
                invited=[], no_calendar=[], privacy_disabled=[], not_found=[], emails=[]
            )

        invited: list[str] = []
        no_calendar: list[str] = []
        privacy_disabled: list[str] = []
        not_found: list[str] = []
        emails: list[str] = []

        # Fetch users by usernames
        users = await self.user_repo.get_users_by_usernames(usernames)

        # Build username -> user mapping (case-insensitive)
        user_map = {}
        for user in users:
            if user.telegram_username:
                user_map[user.telegram_username.lower()] = user

        for username in usernames:
            username_lower = username.lower()
            user = user_map.get(username_lower)  # type: ignore[assignment]

            if not user:
                # User not found in our system
                not_found.append(username)
                continue

            if not user.allow_username_invites:
                # User has privacy disabled
                privacy_disabled.append(username)
                continue

            # Get user's email from OAuth token
            has_calendar, email = await self._get_user_email(user.id)
            if not has_calendar:
                # User hasn't connected calendar
                no_calendar.append(username)
            elif email:
                # Calendar connected and email retrieved
                emails.append(email)
                invited.append(username)
            else:
                # Calendar connected but couldn't fetch email (API error)
                # Still count as invited since they have calendar
                invited.append(username)
                logger.warning(
                    f"User {username} has calendar but couldn't fetch email - "
                    "they won't receive calendar invite"
                )

        return MeetingInviteResult(
            invited=invited,
            no_calendar=no_calendar,
            privacy_disabled=privacy_disabled,
            not_found=not_found,
            emails=emails,
        )

    async def _get_user_email(self, user_id: int) -> tuple[bool, str | None]:
        """Get user's email from their OAuth token.

        We use the email from the Google OAuth connection.

        Returns:
            Tuple of (has_calendar_connected, email_or_none)
            - (False, None) - No calendar connected
            - (True, email) - Calendar connected and email retrieved
            - (True, None) - Calendar connected but couldn't fetch email (API error)
        """
        from datetime import datetime, timedelta

        from calendarbot.integrations.google import GoogleCalendarClient

        token = await self.token_repo.get_token(user_id, "google")
        if not token:
            return (False, None)

        # Token exists, so calendar IS connected
        # Now try to get the email
        try:
            access_token = self.encryption.decrypt(token.access_token_encrypted)
            refresh_token = self.encryption.decrypt(token.refresh_token_encrypted)

            # Check if token is expired or close to expiry (5 min buffer)
            if datetime.utcnow() >= (token.expires_at - timedelta(minutes=5)):
                logger.info(f"Token expired for user {user_id} during email fetch, refreshing...")
                client = GoogleCalendarClient(
                    access_token=access_token,
                    refresh_token=refresh_token,
                )
                new_tokens = await client.refresh_access_token()
                if new_tokens:
                    # Save refreshed token
                    await self.token_repo.save_token(
                        user_id=user_id,
                        provider="google",
                        access_token_encrypted=self.encryption.encrypt(new_tokens["access_token"]),
                        refresh_token_encrypted=self.encryption.encrypt(
                            new_tokens.get("refresh_token") or refresh_token
                        ),
                        expires_at=new_tokens["expires_at"],
                    )
                    access_token = new_tokens["access_token"]
                    logger.info(f"Token refreshed successfully for user {user_id}")
                else:
                    logger.error(f"Token refresh failed for user {user_id}")
                    return (True, None)

            client = GoogleCalendarClient(
                access_token=access_token,
                refresh_token=refresh_token,
            )
            email = await client.get_user_email()
            return (True, email)
        except Exception as e:
            logger.error(f"Failed to get email for user {user_id}: {e}")
            # Calendar IS connected, but we couldn't fetch the email
            return (True, None)

    def get_status_icon(self, status: UsernameStatus) -> str:
        """Get display icon for a username status."""
        icons = {
            UsernameStatus.REGISTERED: "✓",
            UsernameStatus.NO_CALENDAR: "⚠️",
            UsernameStatus.PRIVACY_DISABLED: "🔒",
            UsernameStatus.NOT_FOUND: "❓",
        }
        return icons.get(status, "❓")

    async def get_username_statuses(
        self,
        usernames: list[str],
        requester_id: int,
    ) -> dict[str, str]:
        """Get status icons for usernames for display.

        Returns dict mapping username to status icon string.
        """
        resolved = await self.resolve_usernames(usernames, requester_id)
        return {
            username: self.get_status_icon(result.status) for username, result in resolved.items()
        }
