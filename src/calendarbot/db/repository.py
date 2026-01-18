"""Data access layer."""

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from calendarbot.db.models import (
    Meeting,
    OAuthToken,
    PendingInvite,
    RecentContact,
    User,
    UsernameLookup,
)

# Sentinel value to distinguish "not provided" from None
_UNSET: Any = object()


class UserRepository:
    """User data access."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        """Get user by Telegram ID."""
        result = await self.session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one_or_none()

    async def get_or_create(
        self,
        telegram_id: int,
        telegram_username: str | None = None,
        timezone: str | None = None,
        language: str | None = None,
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
            language=language or "en",
        )
        self.session.add(user)
        await self.session.flush()
        return user, True

    async def update_settings(
        self,
        user: User,
        timezone: str | None = None,
        default_duration: int | None = None,
        default_reminder: str | None = _UNSET,
        notifications_enabled: bool | None = None,
        language: str | None = None,
        allow_username_invites: bool | None = None,
    ) -> User:
        """Update user settings."""
        if timezone is not None:
            user.timezone = timezone
        if default_duration is not None:
            user.default_duration = default_duration
        if default_reminder is not _UNSET:  # Allow setting to None
            user.default_reminder = default_reminder
        if notifications_enabled is not None:
            user.notifications_enabled = notifications_enabled
        if language is not None:
            user.language = language
        if allow_username_invites is not None:
            user.allow_username_invites = allow_username_invites
        await self.session.flush()
        return user

    async def get_by_username(self, username: str) -> User | None:
        """Get user by Telegram username (case-insensitive)."""
        result = await self.session.execute(
            select(User).where(User.telegram_username.ilike(username))
        )
        return result.scalar_one_or_none()

    async def get_users_by_usernames(self, usernames: list[str]) -> list[User]:
        """Get multiple users by their Telegram usernames."""
        if not usernames:
            return []
        # Use case-insensitive matching
        from sqlalchemy import func as sa_func

        lower_usernames = [u.lower() for u in usernames]
        result = await self.session.execute(
            select(User).where(sa_func.lower(User.telegram_username).in_(lower_usernames))
        )
        return list(result.scalars().all())


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
        reminders: list[int] | None = None,
    ) -> Meeting:
        """Save meeting to local cache."""
        # Convert reminders list to comma-separated string
        reminders_str = ",".join(str(r) for r in reminders) if reminders else None

        meeting = Meeting(
            user_id=user_id,
            external_id=external_id,
            provider=provider,
            title=title,
            start_time=start_time,
            end_time=end_time,
            attendees={"emails": attendees} if attendees else None,
            reminders=reminders_str,
            reminders_sent=None,
        )
        self.session.add(meeting)
        await self.session.flush()
        return meeting

    async def get_meetings_with_pending_reminders(self, now: datetime) -> list[Meeting]:
        """Get meetings that have reminders that need to be sent.

        Returns meetings where:
        - start_time is in the future
        - reminders field is set
        - there are reminders that haven't been sent yet
        """
        result = await self.session.execute(
            select(Meeting)
            .where(
                Meeting.start_time > now,
                Meeting.reminders.isnot(None),
            )
            .order_by(Meeting.start_time)
        )
        return list(result.scalars().all())

    async def mark_reminder_sent(self, meeting_id: int, reminder_minutes: int) -> None:
        """Mark a specific reminder as sent for a meeting."""
        result = await self.session.execute(select(Meeting).where(Meeting.id == meeting_id))
        meeting = result.scalar_one_or_none()
        if meeting:
            sent = set()
            if meeting.reminders_sent:
                sent = set(meeting.reminders_sent.split(","))
            sent.add(str(reminder_minutes))
            meeting.reminders_sent = ",".join(sorted(sent, key=int))
            await self.session.flush()

    async def delete_by_external_id(self, user_id: int, external_id: str, provider: str) -> bool:
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


class PendingInviteRepository:
    """Pending invite data access."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        inviter_telegram_id: int,
        invitee_username: str,
        meeting_id: str,
        meeting_title: str,
        meeting_time: datetime,
    ) -> PendingInvite:
        """Create a pending invite for an unregistered user."""
        invite = PendingInvite(
            inviter_telegram_id=inviter_telegram_id,
            invitee_username=invitee_username.lower(),  # Store lowercase for consistency
            meeting_id=meeting_id,
            meeting_title=meeting_title,
            meeting_time=meeting_time,
        )
        self.session.add(invite)
        await self.session.flush()
        return invite

    async def get_by_username(self, username: str) -> list[PendingInvite]:
        """Get all pending invites for a username."""
        result = await self.session.execute(
            select(PendingInvite).where(PendingInvite.invitee_username == username.lower())
        )
        return list(result.scalars().all())

    async def get_by_id(self, invite_id: int) -> PendingInvite | None:
        """Get a specific pending invite by ID."""
        result = await self.session.execute(
            select(PendingInvite).where(PendingInvite.id == invite_id)
        )
        return result.scalar_one_or_none()

    async def delete(self, invite: PendingInvite) -> None:
        """Delete a pending invite."""
        await self.session.delete(invite)

    async def delete_by_username(self, username: str) -> int:
        """Delete all pending invites for a username. Returns count deleted."""
        invites = await self.get_by_username(username)
        for invite in invites:
            await self.session.delete(invite)
        return len(invites)


class UsernameLookupRepository:
    """Username lookup rate limiting data access."""

    RATE_LIMIT = 50  # lookups per hour per user
    WINDOW_HOURS = 1

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create(self, telegram_id: int) -> UsernameLookup:
        """Get or create a lookup record for a user."""
        result = await self.session.execute(
            select(UsernameLookup).where(UsernameLookup.requester_telegram_id == telegram_id)
        )
        lookup = result.scalar_one_or_none()

        if not lookup:
            lookup = UsernameLookup(
                requester_telegram_id=telegram_id,
                lookup_count=0,
                window_start=datetime.now(tz=UTC),
            )
            self.session.add(lookup)
            await self.session.flush()

        return lookup

    async def check_and_increment(self, telegram_id: int, count: int = 1) -> bool:
        """Check if user is within rate limit and increment counter.

        Returns True if within limit, False if rate limited.
        """
        from datetime import timedelta

        lookup = await self.get_or_create(telegram_id)
        now = datetime.now(tz=UTC)

        # Make window_start timezone-aware if it isn't
        window_start = lookup.window_start
        if window_start.tzinfo is None:
            window_start = window_start.replace(tzinfo=UTC)

        # Reset window if expired
        if now - window_start > timedelta(hours=self.WINDOW_HOURS):
            lookup.lookup_count = 0
            lookup.window_start = now

        # Check limit
        if lookup.lookup_count + count > self.RATE_LIMIT:
            return False

        # Increment and allow
        lookup.lookup_count += count
        await self.session.flush()
        return True

    async def get_remaining(self, telegram_id: int) -> int:
        """Get remaining lookups for a user in current window."""
        from datetime import timedelta

        lookup = await self.get_or_create(telegram_id)
        now = datetime.now(tz=UTC)

        # Make window_start timezone-aware if it isn't
        window_start = lookup.window_start
        if window_start.tzinfo is None:
            window_start = window_start.replace(tzinfo=UTC)

        # If window expired, full limit available
        if now - window_start > timedelta(hours=self.WINDOW_HOURS):
            return self.RATE_LIMIT

        return max(0, self.RATE_LIMIT - lookup.lookup_count)


class RecentContactRepository:
    """Recent contact data access."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_recent_contacts(self, user_id: int, limit: int = 10) -> list[RecentContact]:
        """Get recent contacts for a user, ordered by use count and last used."""
        result = await self.session.execute(
            select(RecentContact)
            .where(RecentContact.user_id == user_id)
            .order_by(RecentContact.use_count.desc(), RecentContact.last_used.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def add_or_update_contact(
        self,
        user_id: int,
        identifier: str,
        contact_type: str,
        display_name: str | None = None,
    ) -> RecentContact:
        """Add a new contact or update existing one (increment use count)."""
        result = await self.session.execute(
            select(RecentContact).where(
                RecentContact.user_id == user_id,
                RecentContact.contact_identifier == identifier,
            )
        )
        contact = result.scalar_one_or_none()

        if contact:
            contact.use_count += 1
            contact.last_used = datetime.now(tz=UTC)
            if display_name:
                contact.display_name = display_name
        else:
            contact = RecentContact(
                user_id=user_id,
                contact_identifier=identifier,
                contact_type=contact_type,
                display_name=display_name,
            )
            self.session.add(contact)

        await self.session.flush()
        return contact

    async def remove_contact(self, user_id: int, identifier: str) -> bool:
        """Remove a contact by identifier. Returns True if deleted."""
        result = await self.session.execute(
            select(RecentContact).where(
                RecentContact.user_id == user_id,
                RecentContact.contact_identifier == identifier,
            )
        )
        contact = result.scalar_one_or_none()

        if contact:
            await self.session.delete(contact)
            return True
        return False
