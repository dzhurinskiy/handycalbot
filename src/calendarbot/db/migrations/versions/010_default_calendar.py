"""Add default_calendar column to users.

Revision ID: 010_default_calendar
Revises: 009_privacy_mode
Create Date: 2026-01-23

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "010_default_calendar"
down_revision: str | None = "009_privacy_mode"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add default_calendar column to users.

    default_calendar: 'google', 'outlook', or NULL (use priority logic)
    """
    conn = op.get_bind()

    # Add default_calendar column if it doesn't exist
    conn.execute(
        sa.text("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_name = 'users' AND column_name = 'default_calendar'
                ) THEN
                    ALTER TABLE users ADD COLUMN default_calendar VARCHAR(20) DEFAULT NULL;
                END IF;
            END $$;
            """)
    )


def downgrade() -> None:
    """Remove default_calendar column."""
    conn = op.get_bind()
    conn.execute(
        sa.text("""
            ALTER TABLE users DROP COLUMN IF EXISTS default_calendar
            """)
    )
