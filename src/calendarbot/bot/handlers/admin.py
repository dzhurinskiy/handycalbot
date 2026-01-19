"""Admin command handlers for bot statistics."""

import logging
from datetime import datetime, timedelta

from sqlalchemy import func, select
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from calendarbot.config import get_settings
from calendarbot.db.models import Meeting, OAuthToken, PendingInvite, User
from calendarbot.db.session import async_session_factory

logger = logging.getLogger(__name__)


def is_admin_chat(update: Update) -> bool:
    """Check if the message is from the admin chat."""
    settings = get_settings()
    if not settings.admin_chat_id:
        return False
    return update.effective_chat and update.effective_chat.id == settings.admin_chat_id


async def stats_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /stats command - show bot statistics (admin only)."""
    if not update.message or not is_admin_chat(update):
        return

    async with async_session_factory() as session:
        # Use naive datetime for comparison with database columns
        now = datetime.utcnow()
        day_ago = now - timedelta(days=1)
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)

        # Total users
        total_users = await session.scalar(select(func.count(User.id)))

        # Users with Google Calendar connected
        google_connected = await session.scalar(
            select(func.count(OAuthToken.id)).where(OAuthToken.provider == "google")
        )

        # Users with Zoom connected
        zoom_connected = await session.scalar(
            select(func.count(OAuthToken.id)).where(OAuthToken.provider == "zoom")
        )

        # Total meetings
        total_meetings = await session.scalar(select(func.count(Meeting.id)))

        # Meetings in last 24h (by created_at)
        meetings_24h = await session.scalar(
            select(func.count(Meeting.id)).where(Meeting.created_at >= day_ago)
        )

        # Meetings in last 7 days
        meetings_7d = await session.scalar(
            select(func.count(Meeting.id)).where(Meeting.created_at >= week_ago)
        )

        # Meetings in last 30 days
        meetings_30d = await session.scalar(
            select(func.count(Meeting.id)).where(Meeting.created_at >= month_ago)
        )

        # Pending invites
        pending_invites = await session.scalar(select(func.count(PendingInvite.id)))

        # Language distribution
        lang_result = await session.execute(
            select(User.language, func.count(User.id)).group_by(User.language)
        )
        lang_distribution = dict(lang_result.all())

        # Users with notifications enabled
        notif_enabled = await session.scalar(
            select(func.count(User.id)).where(User.notifications_enabled.is_(True))
        )

        # Users allowing username invites
        username_invites_enabled = await session.scalar(
            select(func.count(User.id)).where(User.allow_username_invites.is_(True))
        )

    # Format language distribution
    lang_str = ", ".join(f"{lang}: {count}" for lang, count in sorted(lang_distribution.items()))

    stats_message = f"""📊 **Bot Statistics**

**Users:**
• Total: {total_users}
• Google Calendar: {google_connected}
• Zoom: {zoom_connected}
• Notifications on: {notif_enabled}
• Username invites on: {username_invites_enabled}

**Meetings:**
• Total: {total_meetings}
• Last 24h: {meetings_24h}
• Last 7 days: {meetings_7d}
• Last 30 days: {meetings_30d}

**Other:**
• Pending invites: {pending_invites}

**Languages:**
{lang_str}

_Generated at {now.strftime('%Y-%m-%d %H:%M:%S')} UTC_"""

    await update.message.reply_text(stats_message, parse_mode="Markdown")


def setup_admin_handlers(app: Application) -> None:
    """Register admin handlers."""
    app.add_handler(CommandHandler("stats", stats_command))
