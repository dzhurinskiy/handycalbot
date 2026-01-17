"""Add language column to users table.

Revision ID: 003_user_language
Revises: 002_notifs_reminders
Create Date: 2026-01-17

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "003_user_language"
down_revision: str | None = "002_notifs_reminders"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add language column to users table."""
    op.add_column(
        "users",
        sa.Column("language", sa.String(10), nullable=False, server_default="en"),
    )


def downgrade() -> None:
    """Remove language column from users table."""
    op.drop_column("users", "language")
