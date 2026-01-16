"""Add default_reminder column to users table.

Revision ID: 001_add_default_reminder
Revises:
Create Date: 2026-01-16

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "001_add_default_reminder"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add default_reminder column."""
    op.add_column(
        "users",
        sa.Column("default_reminder", sa.String(100), nullable=True, default=None),
    )


def downgrade() -> None:
    """Remove default_reminder column."""
    op.drop_column("users", "default_reminder")
