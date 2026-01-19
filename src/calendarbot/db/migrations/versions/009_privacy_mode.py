"""Add privacy_mode column to oauth_tokens.

Revision ID: 009_privacy_mode
Revises: 008_oauth_email
Create Date: 2026-01-19

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "009_privacy_mode"
down_revision: str | None = "008_oauth_email"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add privacy_mode column to oauth_tokens.

    privacy_mode: True = limited scopes (create only, no read)
                  False/NULL = full access (default, existing behavior)
    """
    conn = op.get_bind()

    # Add privacy_mode column if it doesn't exist
    conn.execute(sa.text("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_name = 'oauth_tokens' AND column_name = 'privacy_mode'
                ) THEN
                    ALTER TABLE oauth_tokens ADD COLUMN privacy_mode BOOLEAN DEFAULT FALSE;
                END IF;
            END $$;
            """))


def downgrade() -> None:
    """Remove privacy_mode column."""
    conn = op.get_bind()
    conn.execute(sa.text("""
            ALTER TABLE oauth_tokens DROP COLUMN IF EXISTS privacy_mode
            """))
