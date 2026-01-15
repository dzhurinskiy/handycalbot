"""Integration tests for user service."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from calendarbot.db.models import User
from calendarbot.services.user import UserService


class TestUserService:
    """Tests for UserService."""

    @pytest.mark.asyncio
    async def test_get_or_create_new_user(self, db_session: AsyncSession):
        """Test creating a new user."""
        service = UserService(db_session)

        user, created = await service.get_or_create_user(
            telegram_id=999888777,
            telegram_username="newuser",
        )
        await db_session.commit()

        assert created is True
        assert user.telegram_id == 999888777
        assert user.telegram_username == "newuser"
        assert user.timezone == "UTC"
        assert user.default_duration == 60

    @pytest.mark.asyncio
    async def test_get_or_create_existing_user(self, db_session: AsyncSession, test_user: User):
        """Test getting existing user."""
        service = UserService(db_session)

        user, created = await service.get_or_create_user(
            telegram_id=test_user.telegram_id,
        )

        assert created is False
        assert user.id == test_user.id

    @pytest.mark.asyncio
    async def test_update_timezone(self, db_session: AsyncSession, test_user: User):
        """Test updating user timezone."""
        service = UserService(db_session)

        updated = await service.update_timezone(test_user, "Europe/Berlin")
        await db_session.commit()

        assert updated.timezone == "Europe/Berlin"

    @pytest.mark.asyncio
    async def test_update_duration(self, db_session: AsyncSession, test_user: User):
        """Test updating default duration."""
        service = UserService(db_session)

        updated = await service.update_duration(test_user, 30)
        await db_session.commit()

        assert updated.default_duration == 30

    @pytest.mark.asyncio
    async def test_is_calendar_not_connected(self, db_session: AsyncSession, test_user: User):
        """Test checking calendar connection when not connected."""
        service = UserService(db_session)

        connected = await service.is_calendar_connected(test_user)

        assert connected is False

    @pytest.mark.asyncio
    async def test_get_user_summary(self, db_session: AsyncSession, test_user: User):
        """Test getting user summary."""
        service = UserService(db_session)

        summary = await service.get_user_summary(test_user)

        assert summary["telegram_id"] == test_user.telegram_id
        assert summary["timezone"] == "UTC"
        assert summary["default_duration"] == 60
        assert summary["google_calendar"] == "Not connected"
