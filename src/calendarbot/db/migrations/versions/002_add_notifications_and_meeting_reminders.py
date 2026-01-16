"""Add notifications_enabled to users and reminders to meetings.

Revision ID: 002_add_notifications_and_meeting_reminders
Revises: 001_add_default_reminder
Create Date: 2026-01-16

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "002_add_notifications_and_meeting_reminders"
down_revision: str | None = "001_add_default_reminder"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add new columns."""
    # Add notifications_enabled to users table
    op.add_column(
        "users",
        sa.Column("notifications_enabled", sa.Boolean(), nullable=False, server_default="true"),
    )

    # Add reminders and reminders_sent to meetings table
    op.add_column(
        "meetings",
        sa.Column("reminders", sa.String(100), nullable=True),
    )
    op.add_column(
        "meetings",
        sa.Column("reminders_sent", sa.String(100), nullable=True),
    )


def downgrade() -> None:
    """Remove added columns."""
    op.drop_column("meetings", "reminders_sent")
    op.drop_column("meetings", "reminders")
    op.drop_column("users", "notifications_enabled")
