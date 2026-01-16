"""Data access layer."""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from calendarbot.db.models import Meeting, OAuthToken, User


class UserRepository:
    """User data access."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        """Get user by Telegram ID."""
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def get_or_create(
        self, telegram_id: int, telegram_username: str | None = None, timezone: str | None = None
    ) -> tuple[User, bool]:
        """Get existing user or create new one. Returns (user, created)."""
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            # Update username if changed
            if telegram_username and user.telegram_username != telegram_username:
                user.telegram_username = telegram_username
            return user, False

        user = User(
            telegram_id=telegram_id,
            telegram_username=telegram_username,
            timezone=timezone or "UTC",
        )
        self.session.add(user)
        await self.session.flush()
        return user, True

    async def update_settings(
        self,
        user: User,
        timezone: str | None = None,
        default_duration: int | None = None,
        default_reminder: str | None = ...,  # Use ... as sentinel to distinguish from None
    ) -> User:
        """Update user settings."""
        if timezone is not None:
            user.timezone = timezone
        if default_duration is not None:
            user.default_duration = default_duration
        if default_reminder is not ...:  # Allow setting to None
            user.default_reminder = default_reminder
        await self.session.flush()
        return user


class OAuthTokenRepository:
    """OAuth token data access."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_token(self, user_id: int, provider: str) -> OAuthToken | None:
        """Get OAuth token for user and provider."""
        result = await self.session.execute(
            select(OAuthToken).where(
                OAuthToken.user_id == user_id,
                OAuthToken.provider == provider,
            )
        )
        return result.scalar_one_or_none()

    async def save_token(
        self,
        user_id: int,
        provider: str,
        access_token_encrypted: str,
        refresh_token_encrypted: str,
        expires_at: datetime,
        calendar_id: str | None = None,
    ) -> OAuthToken:
        """Save or update OAuth token."""
        token = await self.get_token(user_id, provider)

        if token:
            token.access_token_encrypted = access_token_encrypted
            token.refresh_token_encrypted = refresh_token_encrypted
            token.expires_at = expires_at
            if calendar_id:
                token.calendar_id = calendar_id
        else:
            token = OAuthToken(
                user_id=user_id,
                provider=provider,
                access_token_encrypted=access_token_encrypted,
                refresh_token_encrypted=refresh_token_encrypted,
                expires_at=expires_at,
                calendar_id=calendar_id,
            )
            self.session.add(token)

        await self.session.flush()
        return token

    async def delete_token(self, user_id: int, provider: str) -> bool:
        """Delete OAuth token."""
        token = await self.get_token(user_id, provider)
        if token:
            await self.session.delete(token)
            return True
        return False


class MeetingRepository:
    """Meeting data access."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_upcoming(
        self, user_id: int, from_time: datetime | None = None, limit: int = 10
    ) -> list[Meeting]:
        """Get upcoming meetings for user."""
        if from_time is None:
            from_time = datetime.utcnow()

        result = await self.session.execute(
            select(Meeting)
            .where(Meeting.user_id == user_id, Meeting.start_time >= from_time)
            .order_by(Meeting.start_time)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def save_meeting(
        self,
        user_id: int,
        external_id: str,
        provider: str,
        title: str,
        start_time: datetime,
        end_time: datetime,
        attendees: list[str] | None = None,
    ) -> Meeting:
        """Save meeting to local cache."""
        meeting = Meeting(
            user_id=user_id,
            external_id=external_id,
            provider=provider,
            title=title,
            start_time=start_time,
            end_time=end_time,
            attendees={"emails": attendees} if attendees else None,
        )
        self.session.add(meeting)
        await self.session.flush()
        return meeting

    async def delete_by_external_id(
        self, user_id: int, external_id: str, provider: str
    ) -> bool:
        """Delete meeting by external ID."""
        result = await self.session.execute(
            select(Meeting).where(
                Meeting.user_id == user_id,
                Meeting.external_id == external_id,
                Meeting.provider == provider,
            )
        )
        meeting = result.scalar_one_or_none()
        if meeting:
            await self.session.delete(meeting)
            return True
        return False
