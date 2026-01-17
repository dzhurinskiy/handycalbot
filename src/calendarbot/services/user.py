"""User service for managing user data and settings."""

from sqlalchemy.ext.asyncio import AsyncSession

from calendarbot.db.models import User
from calendarbot.db.repository import OAuthTokenRepository, UserRepository


class UserService:
    """Business logic for user management."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.token_repo = OAuthTokenRepository(session)

    async def get_or_create_user(
        self,
        telegram_id: int,
        telegram_username: str | None = None,
        timezone: str | None = None,
        language: str | None = None,
    ) -> tuple[User, bool]:
        """Get or create user. Returns (user, is_new)."""
        return await self.user_repo.get_or_create(
            telegram_id, telegram_username, timezone, language
        )

    async def get_user(self, telegram_id: int) -> User | None:
        """Get user by Telegram ID."""
        return await self.user_repo.get_by_telegram_id(telegram_id)

    async def update_timezone(self, user: User, timezone: str) -> User:
        """Update user timezone."""
        return await self.user_repo.update_settings(user, timezone=timezone)

    async def update_duration(self, user: User, duration: int) -> User:
        """Update default meeting duration."""
        return await self.user_repo.update_settings(user, default_duration=duration)

    async def update_reminder(self, user: User, reminder: str | None) -> User:
        """Update default reminder setting."""
        return await self.user_repo.update_settings(user, default_reminder=reminder)

    async def update_notifications(self, user: User, enabled: bool) -> User:
        """Update notifications enabled setting."""
        return await self.user_repo.update_settings(user, notifications_enabled=enabled)

    async def update_language(self, user: User, language: str) -> User:
        """Update user's preferred language."""
        return await self.user_repo.update_settings(user, language=language)

    async def update_privacy(self, user: User, allow_username_invites: bool) -> User:
        """Update user's privacy setting for username invites."""
        return await self.user_repo.update_settings(
            user, allow_username_invites=allow_username_invites
        )

    async def is_calendar_connected(self, user: User, provider: str = "google") -> bool:
        """Check if user has connected their calendar."""
        token = await self.token_repo.get_token(user.id, provider)
        return token is not None

    async def disconnect_calendar(self, user: User, provider: str = "google") -> bool:
        """Disconnect calendar provider."""
        return await self.token_repo.delete_token(user.id, provider)

    async def get_user_summary(self, user: User) -> dict:
        """Get user settings summary."""
        google_connected = await self.is_calendar_connected(user, "google")

        return {
            "telegram_id": user.telegram_id,
            "username": user.telegram_username,
            "timezone": user.timezone,
            "default_duration": user.default_duration,
            "google_calendar": "Connected" if google_connected else "Not connected",
        }
