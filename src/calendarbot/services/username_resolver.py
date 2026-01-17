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
    NOT_FOUND = "not_found"  # Username not found in our system


@dataclass
class ResolvedUser:
    """Result of resolving a username."""

    username: str
    status: UsernameStatus
    can_invite: bool
    # Note: NO email field - email is never exposed to protect privacy


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
            user = user_map.get(username_lower)

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
    ) -> tuple[list[str], list[str]]:
        """Get actual emails for meeting creation (after user confirms).

        This is called during actual meeting creation, not preview.
        Returns emails for users who have:
        1. Connected their calendar (so we have their email)
        2. Enabled allow_username_invites

        Args:
            usernames: List of usernames (without @ prefix)
            requester_id: Telegram ID of the user making the request

        Returns:
            Tuple of (resolved_emails, unresolved_usernames)
        """
        if not usernames:
            return [], []

        resolved_emails = []
        unresolved_usernames = []

        # Fetch users by usernames
        users = await self.user_repo.get_users_by_usernames(usernames)

        # Build username -> user mapping (case-insensitive)
        user_map = {}
        for user in users:
            if user.telegram_username:
                user_map[user.telegram_username.lower()] = user

        for username in usernames:
            username_lower = username.lower()
            user = user_map.get(username_lower)

            if not user or not user.allow_username_invites:
                unresolved_usernames.append(username)
                continue

            # Get user's email from OAuth token
            email = await self._get_user_email(user.id)
            if email:
                resolved_emails.append(email)
            else:
                # User hasn't connected calendar, treat as unresolved
                unresolved_usernames.append(username)

        return resolved_emails, unresolved_usernames

    async def _get_user_email(self, user_id: int) -> str | None:
        """Get user's email from their OAuth token.

        We use the email from the Google OAuth connection.
        """
        token = await self.token_repo.get_token(user_id, "google")
        if not token:
            return None

        # The email is stored in the access token response from Google
        # For now, we'll need to make an API call to get it
        # TODO: Consider caching the email in the user table
        try:
            from calendarbot.integrations.google import GoogleCalendarClient

            access_token = self.encryption.decrypt(token.access_token_encrypted)
            refresh_token = self.encryption.decrypt(token.refresh_token_encrypted)
            client = GoogleCalendarClient(
                access_token=access_token,
                refresh_token=refresh_token,
            )
            email = await client.get_user_email()
            return email
        except Exception as e:
            logger.error(f"Failed to get email for user {user_id}: {e}")
            return None

    def get_status_icon(self, status: UsernameStatus) -> str:
        """Get display icon for a username status."""
        icons = {
            UsernameStatus.REGISTERED: "✓",
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
