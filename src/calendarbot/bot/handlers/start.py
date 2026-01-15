"""Start and help command handlers."""

import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from calendarbot.db.session import async_session_factory
from calendarbot.services.user import UserService
from calendarbot.utils.timezone import guess_timezone_from_language

logger = logging.getLogger(__name__)

WELCOME_MESSAGE = """
Welcome to HandyCalBot! 📅

I help you schedule meetings directly from Telegram.

**Quick Start:**
1. Connect your Google Calendar with /connect
2. Create meetings by typing @handycalbot in any chat

**Inline Usage:**
`@handycalbot 14:30 "Meeting Title" email@example.com`
`@handycalbot 10:00 25-01-2026 "Project Sync"`

**Commands:**
/connect - Connect Google Calendar
/disconnect - Disconnect calendar
/settings - View/change settings
/meetings - List upcoming meetings
/help - Show this message

Need help? Just type /help anytime!
"""

HELP_MESSAGE = """
**HandyCalBot Help** 📅

**Creating Meetings (Inline):**
Type `@handycalbot` in any chat followed by:
- Time (required): `HH:MM` (24-hour format)
- Date (optional): `DD-MM-YYYY`
- Title (required): `"Your Meeting Title"`
- Attendees (optional): `email1@example.com, email2@example.com`

**Examples:**
```
@handycalbot 14:30 "Team Standup"
@handycalbot 10:00 25-01-2026 "Project Review" john@company.com
@handycalbot 16:00 "Quick Call" alice@corp.com, bob@corp.com
```

**Commands:**
/start - Welcome message
/connect - Connect Google Calendar
/disconnect - Disconnect calendar
/settings - View and modify settings
/timezone - Set your timezone
/duration - Set default meeting duration
/meetings - Show upcoming meetings
/cancel - Cancel a meeting
/help - This help message

**Settings:**
- Timezone: Used for meeting times
- Duration: Default meeting length (currently 60 min)
"""


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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

    await update.message.reply_text(
        WELCOME_MESSAGE + timezone_msg,
        parse_mode="Markdown",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
