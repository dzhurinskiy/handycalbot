"""Add email_encrypted column to oauth_tokens.

Revision ID: 008_oauth_email
Revises: 007_inline_msg_id
Create Date: 2026-01-18

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "008_oauth_email"
down_revision: str | None = "007_inline_msg_id"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add email_encrypted column to oauth_tokens."""
    conn = op.get_bind()

    # Add email_encrypted column if it doesn't exist
    conn.execute(sa.text("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_name = 'oauth_tokens' AND column_name = 'email_encrypted'
                ) THEN
                    ALTER TABLE oauth_tokens ADD COLUMN email_encrypted TEXT;
                END IF;
            END $$;
            """))


def downgrade() -> None:
    """Remove email_encrypted column."""
    conn = op.get_bind()
    conn.execute(sa.text("""
            ALTER TABLE oauth_tokens DROP COLUMN IF EXISTS email_encrypted
            """))
