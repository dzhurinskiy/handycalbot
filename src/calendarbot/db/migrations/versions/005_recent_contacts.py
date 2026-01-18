"""Add recent_contacts table for storing frequently invited users.

Revision ID: 005_recent_contacts
Revises: 004_username_invites
Create Date: 2026-01-18

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "005_recent_contacts"
down_revision: str | None = "004_username_invites"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create recent_contacts table for storing frequently invited users."""
    conn = op.get_bind()

    # Create recent_contacts table (idempotent - IF NOT EXISTS)
    conn.execute(
        sa.text(
            """
            CREATE TABLE IF NOT EXISTS recent_contacts (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                contact_identifier VARCHAR(255) NOT NULL,
                contact_type VARCHAR(20) NOT NULL,
                display_name VARCHAR(255),
                use_count INTEGER NOT NULL DEFAULT 1,
                last_used TIMESTAMP WITH TIME ZONE DEFAULT now(),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
            )
            """
        )
    )

    # Create index for faster lookups by user_id (idempotent)
    conn.execute(
        sa.text(
            """
            CREATE INDEX IF NOT EXISTS idx_recent_contacts_user_id
            ON recent_contacts (user_id)
            """
        )
    )

    # Create unique constraint on user_id + contact_identifier (idempotent)
    conn.execute(
        sa.text(
            """
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_constraint
                    WHERE conname = 'uq_recent_contacts_user_identifier'
                ) THEN
                    ALTER TABLE recent_contacts
                    ADD CONSTRAINT uq_recent_contacts_user_identifier
                    UNIQUE (user_id, contact_identifier);
                END IF;
            END $$;
            """
        )
    )


def downgrade() -> None:
    """Remove recent_contacts table."""
    conn = op.get_bind()

    # Drop indexes and tables (idempotent with IF EXISTS)
    conn.execute(sa.text("DROP INDEX IF EXISTS idx_recent_contacts_user_id"))
    conn.execute(sa.text("DROP TABLE IF EXISTS recent_contacts"))
