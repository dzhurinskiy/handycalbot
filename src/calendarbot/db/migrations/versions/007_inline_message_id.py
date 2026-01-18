"""Add inline_message_id to edit_sessions.

Revision ID: 007_inline_msg_id
Revises: 006_edit_sessions
Create Date: 2026-01-18
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "007_inline_msg_id"
down_revision: str | None = "006_edit_sessions"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add inline_message_id column to edit_sessions table."""
    op.add_column(
        "edit_sessions",
        sa.Column("inline_message_id", sa.String(255), nullable=True),
    )


def downgrade() -> None:
    """Remove inline_message_id column from edit_sessions table."""
    op.drop_column("edit_sessions", "inline_message_id")
