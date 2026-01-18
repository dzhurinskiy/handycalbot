"""SQLAlchemy database models."""

from datetime import datetime
from typing import Any

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all models."""

    type_annotation_map = {
        dict[str, Any]: JSON,
    }


class User(Base):
    """Telegram user model."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    telegram_username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    timezone: Mapped[str] = mapped_column(String(50), default="UTC")
    default_duration: Mapped[int] = mapped_column(Integer, default=60)
    # Default reminder in minutes before meeting (None = no reminder)
    # Can store multiple reminders as comma-separated: "10,30" means 10min and 30min before
    default_reminder: Mapped[str | None] = mapped_column(String(100), nullable=True, default=None)
    # Whether to send Telegram notifications for meeting reminders
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    # User's preferred language code (en, es, fr, de, ru, ko, ja, zh)
    language: Mapped[str] = mapped_column(String(10), default="en")
    # Privacy setting: allow others to invite by @username
    allow_username_invites: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    oauth_tokens: Mapped[list["OAuthToken"]] = relationship(
        "OAuthToken", back_populates="user", cascade="all, delete-orphan"
    )
    meetings: Mapped[list["Meeting"]] = relationship(
        "Meeting", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, telegram_id={self.telegram_id})>"


class OAuthToken(Base):
    """OAuth tokens for calendar providers (encrypted)."""

    __tablename__ = "oauth_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    provider: Mapped[str] = mapped_column(String(50), nullable=False)  # 'google', 'outlook'
    access_token_encrypted: Mapped[str] = mapped_column(Text, nullable=False)
    refresh_token_encrypted: Mapped[str] = mapped_column(Text, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    calendar_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # User's email from the OAuth provider (encrypted for privacy)
    email_encrypted: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="oauth_tokens")

    __table_args__ = (Index("idx_oauth_user_provider", "user_id", "provider", unique=True),)

    def __repr__(self) -> str:
        return f"<OAuthToken(id={self.id}, user_id={self.user_id}, provider={self.provider})>"


class Meeting(Base):
    """Meeting cache for quick listing."""

    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    external_id: Mapped[str] = mapped_column(String(255), nullable=False)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    attendees: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    # Reminders in minutes before meeting (comma-separated, e.g., "10,30")
    reminders: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # Which reminders have been sent (comma-separated minutes that were sent)
    reminders_sent: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="meetings")

    __table_args__ = (
        Index("idx_meetings_user_start", "user_id", "start_time"),
        Index("idx_meetings_external", "user_id", "external_id", "provider", unique=True),
    )

    def __repr__(self) -> str:
        return f"<Meeting(id={self.id}, title={self.title})>"


class PendingInvite(Base):
    """Pending invites for unregistered users."""

    __tablename__ = "pending_invites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    inviter_telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    invitee_username: Mapped[str] = mapped_column(String(255), nullable=False)
    meeting_id: Mapped[str] = mapped_column(String(255), nullable=False)
    meeting_title: Mapped[str] = mapped_column(String(255), nullable=False)
    meeting_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (Index("idx_pending_invites_username", "invitee_username"),)

    def __repr__(self) -> str:
        return f"<PendingInvite(id={self.id}, invitee={self.invitee_username})>"


class UsernameLookup(Base):
    """Rate limiting for username lookups."""

    __tablename__ = "username_lookups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    requester_telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    lookup_count: Mapped[int] = mapped_column(Integer, default=0)
    window_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    __table_args__ = (Index("idx_username_lookups_requester", "requester_telegram_id"),)

    def __repr__(self) -> str:
        return f"<UsernameLookup(id={self.id}, requester={self.requester_telegram_id})>"


class RecentContact(Base):
    """Recent contacts for quick attendee selection."""

    __tablename__ = "recent_contacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    # Email address or @username
    contact_identifier: Mapped[str] = mapped_column(String(255), nullable=False)
    # "email" or "username"
    contact_type: Mapped[str] = mapped_column(String(20), nullable=False)
    # Optional display name
    display_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # How many times this contact has been used
    use_count: Mapped[int] = mapped_column(Integer, default=1)
    last_used: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("idx_recent_contacts_user_id", "user_id"),
        Index("uq_recent_contacts_user_identifier", "user_id", "contact_identifier", unique=True),
    )

    def __repr__(self) -> str:
        return f"<RecentContact(id={self.id}, contact={self.contact_identifier})>"


class EditSession(Base):
    """Temporary edit sessions for private chat flow."""

    __tablename__ = "edit_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    # Type of edit: "title", "attendee", "link", "time", "date"
    edit_type: Mapped[str] = mapped_column(String(50), nullable=False)
    # Full meeting data dict
    meeting_data: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    # Original chat where edit was initiated (for reference)
    chat_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    # Original message ID (for reference)
    message_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Inline message ID (for inline query results)
    inline_message_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        Index("ix_edit_sessions_user_id", "user_id"),
        Index("ix_edit_sessions_expires", "expires_at"),
    )

    def __repr__(self) -> str:
        return f"<EditSession(id={self.id}, user_id={self.user_id}, edit_type={self.edit_type})>"
