"""Add username invite feature tables.

Revision ID: 004_username_invites
Revises: 003_user_language
Create Date: 2026-01-17

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "004_username_invites"
down_revision: str | None = "003_user_language"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add username invite feature tables and columns."""
    conn = op.get_bind()

    # Add privacy setting to users table (idempotent - check if column exists)
    result = conn.execute(sa.text("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name='users' AND column_name='allow_username_invites'
            """))
    if result.fetchone() is None:
        op.add_column(
            "users",
            sa.Column(
                "allow_username_invites",
                sa.Boolean(),
                nullable=False,
                server_default="true",
            ),
        )

    # Create pending_invites table (idempotent - IF NOT EXISTS)
    conn.execute(sa.text("""
            CREATE TABLE IF NOT EXISTS pending_invites (
                id SERIAL PRIMARY KEY,
                inviter_telegram_id BIGINT NOT NULL,
                invitee_username VARCHAR(255) NOT NULL,
                meeting_id VARCHAR(255) NOT NULL,
                meeting_title VARCHAR(255) NOT NULL,
                meeting_time TIMESTAMP WITH TIME ZONE NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
            )
            """))

    # Create index for faster lookups by invitee username (idempotent)
    conn.execute(sa.text("""
            CREATE INDEX IF NOT EXISTS idx_pending_invites_username
            ON pending_invites (invitee_username)
            """))

    # Create rate_limit_cache table for username lookups (idempotent)
    conn.execute(sa.text("""
            CREATE TABLE IF NOT EXISTS username_lookups (
                id SERIAL PRIMARY KEY,
                requester_telegram_id BIGINT NOT NULL UNIQUE,
                lookup_count INTEGER NOT NULL DEFAULT 0,
                window_start TIMESTAMP WITH TIME ZONE DEFAULT now()
            )
            """))

    # Create index for faster lookups by requester (idempotent)
    conn.execute(sa.text("""
            CREATE INDEX IF NOT EXISTS idx_username_lookups_requester
            ON username_lookups (requester_telegram_id)
            """))


def downgrade() -> None:
    """Remove username invite feature tables and columns."""
    conn = op.get_bind()

    # Drop indexes and tables (idempotent with IF EXISTS)
    conn.execute(sa.text("DROP INDEX IF EXISTS idx_username_lookups_requester"))
    conn.execute(sa.text("DROP TABLE IF EXISTS username_lookups"))
    conn.execute(sa.text("DROP INDEX IF EXISTS idx_pending_invites_username"))
    conn.execute(sa.text("DROP TABLE IF EXISTS pending_invites"))

    # Drop column if it exists
    result = conn.execute(sa.text("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name='users' AND column_name='allow_username_invites'
            """))
    if result.fetchone() is not None:
        op.drop_column("users", "allow_username_invites")
