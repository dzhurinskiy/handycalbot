"""Add edit_sessions table for private chat edit flow.

Revision ID: 006_edit_sessions
Revises: 005_recent_contacts
Create Date: 2026-01-18

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "006_edit_sessions"
down_revision: str | None = "005_recent_contacts"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create edit_sessions table for storing temporary edit sessions."""
    conn = op.get_bind()

    # Create edit_sessions table (idempotent - IF NOT EXISTS)
    conn.execute(sa.text("""
            CREATE TABLE IF NOT EXISTS edit_sessions (
                id VARCHAR(36) PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                edit_type VARCHAR(50) NOT NULL,
                meeting_data JSONB NOT NULL,
                chat_id BIGINT,
                message_id INTEGER,
                inline_message_id VARCHAR(255),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
                expires_at TIMESTAMP WITH TIME ZONE NOT NULL
            )
            """))

    # Add inline_message_id column if it doesn't exist (for existing tables)
    conn.execute(sa.text("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_name = 'edit_sessions' AND column_name = 'inline_message_id'
                ) THEN
                    ALTER TABLE edit_sessions ADD COLUMN inline_message_id VARCHAR(255);
                END IF;
            END $$;
            """))

    # Create index for faster lookups by user_id (idempotent)
    conn.execute(sa.text("""
            CREATE INDEX IF NOT EXISTS ix_edit_sessions_user_id
            ON edit_sessions (user_id)
            """))

    # Create index for cleanup of expired sessions (idempotent)
    conn.execute(sa.text("""
            CREATE INDEX IF NOT EXISTS ix_edit_sessions_expires
            ON edit_sessions (expires_at)
            """))


def downgrade() -> None:
    """Remove edit_sessions table."""
    conn = op.get_bind()

    # Drop indexes and tables (idempotent with IF EXISTS)
    conn.execute(sa.text("DROP INDEX IF EXISTS ix_edit_sessions_expires"))
    conn.execute(sa.text("DROP INDEX IF EXISTS ix_edit_sessions_user_id"))
    conn.execute(sa.text("DROP TABLE IF EXISTS edit_sessions"))
