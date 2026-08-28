"""Add meeting_url column to meetings.

Revision ID: 011_meeting_url
Revises: 010_default_calendar
Create Date: 2026-08-28

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "011_meeting_url"
down_revision: str | None = "010_default_calendar"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add nullable meeting_url column to meetings for storing join links."""
    conn = op.get_bind()
    conn.execute(sa.text("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_name = 'meetings' AND column_name = 'meeting_url'
                ) THEN
                    ALTER TABLE meetings ADD COLUMN meeting_url TEXT DEFAULT NULL;
                END IF;
            END $$;
            """))


def downgrade() -> None:
    """Remove meeting_url column."""
    conn = op.get_bind()
    conn.execute(sa.text("""
            ALTER TABLE meetings DROP COLUMN IF EXISTS meeting_url
            """))
