"""Start and help command handlers."""

import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes

from calendarbot.db.session import async_session_factory
from calendarbot.services.user import UserService
from calendarbot.utils.timezone import guess_timezone_from_language

logger = logging.getLogger(__name__)

WELCOME_MESSAGE = """
Welcome to *HandyCalBot*! 📅

I help you schedule meetings directly from Telegram.

*Quick Start:*
1️⃣ Connect your Google Calendar with /connect
2️⃣ Create meetings by typing @handycalbot in any chat

*Inline Usage:*
`@handycalbot 14:30 "Meeting Title" email@example.com`
`@handycalbot 10:00 25-01-2026 "Project Sync"`
`@handycalbot 14:30 "Meeting" r 10m` (with reminder)

*All Commands:*
/start - Welcome message
/help - Show help and usage
/connect - Connect Google Calendar
/disconnect - Disconnect calendar
/meetings - List upcoming meetings
/cancel - Cancel a meeting
/settings - View your settings
/timezone - Change timezone
/duration - Set default duration
/reminder - Set default reminder
/notifications - Toggle reminders
/donate - Support the bot ⭐
"""

HELP_MESSAGE = """
*HandyCalBot Help* 📅

*Creating Meetings (Inline):*
Type `@handycalbot` in any chat followed by:
• Time (required): `HH:MM` (24-hour format)
• Date (optional): `DD-MM-YYYY`
• Title (required): `"Your Meeting Title"`
• Attendees (optional): `email@example.com`
• Reminder (optional): `r 10m` or `r 10m/30m` or just `r`

*Reminder Format:*
• `r 10m` - remind 10 minutes before
• `r 1h` - remind 1 hour before
• `r 1d` - remind 1 day before
• `r 10m/30m` - multiple reminders
• `r` - use your default reminder
• (no r) - no reminder

*Examples:*
`@handycalbot 14:30 "Team Standup"`
`@handycalbot 10:00 25-01-2026 "Review" john@co.com`
`@handycalbot 16:00 "Quick Call" r 15m`
`@handycalbot 14:00 "Meeting" alice@co.com r 10m/1h`

*All Commands:*
/start - Welcome message
/help - This help message
/connect - Connect Google Calendar
/disconnect - Disconnect calendar
/meetings - Show upcoming meetings
/cancel - Cancel a meeting
/settings - View your settings
/timezone - Set your timezone
/duration - Set default meeting duration
/reminder - Set default reminder
/notifications - Toggle reminder notifications
/donate - Support the bot with Stars ⭐
"""


async def start_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    if not update.effective_user or not update.message:
        return

    # Guess timezone from Telegram language setting
    guessed_timezone = guess_timezone_from_language(update.effective_user.language_code)

    async with async_session_factory() as session:
        user_service = UserService(session)
        user, is_new = await user_service.get_or_create_user(
            telegram_id=update.effective_user.id,
            telegram_username=update.effective_user.username,
            timezone=guessed_timezone,
        )
        await session.commit()

        if is_new:
            logger.info(
                f"New user registered: {update.effective_user.id} "
                f"(lang={update.effective_user.language_code}, tz={guessed_timezone})"
            )
            # Inform user about detected timezone
            timezone_msg = f"\n\n📍 I've set your timezone to `{guessed_timezone}` based on your Telegram language. Use /timezone to change it if needed."
        else:
            timezone_msg = ""

    # Add Donate button
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("⭐ Support HandyCalBot", callback_data="donate_menu")]]
    )

    await update.message.reply_text(
        WELCOME_MESSAGE + timezone_msg,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


async def help_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    if not update.message:
        return

    await update.message.reply_text(
        HELP_MESSAGE,
        parse_mode="Markdown",
    )


def setup_start_handlers(app: Application) -> None:
    """Register start/help handlers."""
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
