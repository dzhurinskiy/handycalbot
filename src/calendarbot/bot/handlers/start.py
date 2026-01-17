"""Start and help command handlers."""

import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes

from calendarbot.db.session import async_session_factory
from calendarbot.i18n import detect_language, get_text
from calendarbot.services.user import UserService
from calendarbot.utils.timezone import guess_timezone_from_language

logger = logging.getLogger(__name__)


async def start_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    if not update.effective_user or not update.message:
        return

    # Guess timezone from Telegram language setting
    guessed_timezone = guess_timezone_from_language(update.effective_user.language_code)
    # Detect language from Telegram settings
    detected_language = detect_language(update.effective_user.language_code)

    async with async_session_factory() as session:
        user_service = UserService(session)
        user, is_new = await user_service.get_or_create_user(
            telegram_id=update.effective_user.id,
            telegram_username=update.effective_user.username,
            timezone=guessed_timezone,
            language=detected_language,
        )
        await session.commit()

        # Get translations based on user's language
        user_lang = user.language if user else "en"
        t = get_text(user_lang)

        if is_new:
            logger.info(
                f"New user registered: {update.effective_user.id} "
                f"(lang={update.effective_user.language_code}, tz={guessed_timezone})"
            )
            # Inform user about detected timezone
            timezone_msg = f"\n\n{t.start.timezone_detected.format(timezone=guessed_timezone)}"
        else:
            timezone_msg = ""

    # Add Donate button
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(f"* {t.start.support_button}", callback_data="donate_menu")]]
    )

    await update.message.reply_text(
        t.start.welcome_message + timezone_msg,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


async def help_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    if not update.message:
        return

    # Get user's language preference
    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id) if update.effective_user else None
        user_lang = user.language if user else "en"

    t = get_text(user_lang)

    await update.message.reply_text(
        t.start.help_message,
        parse_mode="Markdown",
    )


def setup_start_handlers(app: Application) -> None:
    """Register start/help handlers."""
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
