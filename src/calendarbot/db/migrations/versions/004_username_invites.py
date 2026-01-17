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
    # Add privacy setting to users table
    op.add_column(
        "users",
        sa.Column(
            "allow_username_invites",
            sa.Boolean(),
            nullable=False,
            server_default="true",
        ),
    )

    # Create pending_invites table for unregistered users
    op.create_table(
        "pending_invites",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("inviter_telegram_id", sa.BigInteger(), nullable=False),
        sa.Column("invitee_username", sa.String(255), nullable=False),
        sa.Column("meeting_id", sa.String(255), nullable=False),
        sa.Column("meeting_title", sa.String(255), nullable=False),
        sa.Column("meeting_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )

    # Create index for faster lookups by invitee username
    op.create_index(
        "idx_pending_invites_username",
        "pending_invites",
        ["invitee_username"],
    )

    # Create rate_limit_cache table for username lookups
    op.create_table(
        "username_lookups",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("requester_telegram_id", sa.BigInteger(), nullable=False, unique=True),
        sa.Column("lookup_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "window_start",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )

    # Create index for faster lookups by requester
    op.create_index(
        "idx_username_lookups_requester",
        "username_lookups",
        ["requester_telegram_id"],
    )


def downgrade() -> None:
    """Remove username invite feature tables and columns."""
    op.drop_index("idx_username_lookups_requester", table_name="username_lookups")
    op.drop_table("username_lookups")
    op.drop_index("idx_pending_invites_username", table_name="pending_invites")
    op.drop_table("pending_invites")
    op.drop_column("users", "allow_username_invites")
