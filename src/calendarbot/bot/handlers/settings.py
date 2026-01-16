"""Settings command handlers."""

import logging
import secrets

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from calendarbot.db.session import async_session_factory
from calendarbot.integrations.google import GoogleOAuthFlow
from calendarbot.services.user import UserService
from calendarbot.utils.timezone import TimezoneHelper

logger = logging.getLogger(__name__)

# Conversation states
AWAITING_TIMEZONE = 1
AWAITING_DURATION = 2
AWAITING_REMINDER = 3

# Reminder options in minutes
REMINDER_OPTIONS = [
    (None, "No reminder"),
    (10, "10 minutes"),
    (15, "15 minutes"),
    (30, "30 minutes"),
    (60, "1 hour"),
    (1440, "1 day"),
]


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /settings command - show current settings."""
    if not update.effective_user or not update.message:
        return

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if not user:
            await update.message.reply_text("Please run /start first.")
            return

        summary = await user_service.get_user_summary(user)

        # Format reminder display
        reminder_display = _format_reminder_setting(user.default_reminder)

    text = f"""
**Your Settings** ⚙️

📍 Timezone: `{summary['timezone']}`
⏱️ Default Duration: `{summary['default_duration']} minutes`
🔔 Default Reminder: `{reminder_display}`
📅 Google Calendar: {summary['google_calendar']}

**Change Settings:**
/timezone - Change timezone
/duration - Change default duration
/reminder - Change default reminder
/connect - Connect Google Calendar
/disconnect - Disconnect Google Calendar
"""

    await update.message.reply_text(text, parse_mode="Markdown")


def _format_reminder_setting(reminder: str | None) -> str:
    """Format reminder setting for display."""
    if not reminder:
        return "No reminder"
    minutes_list = [int(x) for x in reminder.split(",")]
    parts = []
    for m in minutes_list:
        if m >= 1440:
            days = m // 1440
            parts.append(f"{days} day{'s' if days > 1 else ''}")
        elif m >= 60:
            hours = m // 60
            parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
        else:
            parts.append(f"{m} min")
    return ", ".join(parts) + " before"


async def connect_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /connect command - initiate Google OAuth."""
    if not update.effective_user or not update.message:
        return

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if not user:
            await update.message.reply_text("Please run /start first.")
            return

        # Check if already connected
        if await user_service.is_calendar_connected(user):
            await update.message.reply_text(
                "Google Calendar is already connected!\n"
                "Use /disconnect to unlink it first."
            )
            return

    # Generate OAuth state
    state = f"{update.effective_user.id}:{secrets.token_urlsafe(16)}"

    # Store state in context for verification
    if context.bot_data is None:
        context.bot_data = {}
    context.bot_data[f"oauth_state_{update.effective_user.id}"] = state

    # Generate auth URL
    oauth = GoogleOAuthFlow()
    auth_url = oauth.get_authorization_url(state)

    keyboard = [[InlineKeyboardButton("Connect Google Calendar", url=auth_url)]]

    await update.message.reply_text(
        "Click the button below to connect your Google Calendar.\n\n"
        "You'll be redirected to Google to authorize access.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def disconnect_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /disconnect command."""
    if not update.effective_user or not update.message:
        return

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if not user:
            await update.message.reply_text("Please run /start first.")
            return

        if not await user_service.is_calendar_connected(user):
            await update.message.reply_text("No calendar connected.")
            return

        await user_service.disconnect_calendar(user)
        await session.commit()

    await update.message.reply_text(
        "Google Calendar disconnected successfully.\n"
        "Use /connect to link it again."
    )


async def timezone_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /timezone command - start timezone selection."""
    if not update.message:
        return ConversationHandler.END

    # Show common timezones as buttons
    timezones = TimezoneHelper.get_common_timezones()
    buttons = []
    row = []

    for i, tz in enumerate(timezones):
        row.append(InlineKeyboardButton(tz, callback_data=f"tz_{tz}"))
        if (i + 1) % 2 == 0:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    await update.message.reply_text(
        "Select your timezone or type it manually (e.g., `Europe/Berlin`):",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="Markdown",
    )

    return AWAITING_TIMEZONE


async def timezone_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle timezone button selection (within conversation)."""
    await _handle_timezone_selection(update)
    return ConversationHandler.END


async def timezone_callback_standalone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle timezone button selection (standalone, e.g., from OAuth callback)."""
    await _handle_timezone_selection(update)


async def _handle_timezone_selection(update: Update) -> None:
    """Common logic for handling timezone selection."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    await query.answer()

    tz = query.data.replace("tz_", "")

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if user:
            await user_service.update_timezone(user, tz)
            await session.commit()

    await query.edit_message_text(
        f"✅ Timezone set to: `{tz}`\n\n"
        "You're all set! Create meetings using:\n"
        "`@handycalbot 14:30 \"Meeting Title\"`",
        parse_mode="Markdown"
    )


async def timezone_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle manual timezone input."""
    if not update.message or not update.message.text or not update.effective_user:
        return ConversationHandler.END

    tz = update.message.text.strip()

    if not TimezoneHelper.is_valid_timezone(tz):
        await update.message.reply_text(
            f"Invalid timezone: `{tz}`\n"
            "Please use a valid timezone like `Europe/London` or `America/New_York`.",
            parse_mode="Markdown",
        )
        return AWAITING_TIMEZONE

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if user:
            await user_service.update_timezone(user, tz)
            await session.commit()

    await update.message.reply_text(f"Timezone set to: `{tz}`", parse_mode="Markdown")
    return ConversationHandler.END


async def duration_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /duration command."""
    if not update.message:
        return ConversationHandler.END

    buttons = [
        [
            InlineKeyboardButton("15 min", callback_data="dur_15"),
            InlineKeyboardButton("30 min", callback_data="dur_30"),
        ],
        [
            InlineKeyboardButton("45 min", callback_data="dur_45"),
            InlineKeyboardButton("60 min", callback_data="dur_60"),
        ],
        [
            InlineKeyboardButton("90 min", callback_data="dur_90"),
            InlineKeyboardButton("120 min", callback_data="dur_120"),
        ],
    ]

    await update.message.reply_text(
        "Select default meeting duration:",
        reply_markup=InlineKeyboardMarkup(buttons),
    )

    return AWAITING_DURATION


async def duration_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle duration button selection."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return ConversationHandler.END

    await query.answer()

    duration = int(query.data.replace("dur_", ""))

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if user:
            await user_service.update_duration(user, duration)
            await session.commit()

    await query.edit_message_text(f"Default duration set to: {duration} minutes")
    return ConversationHandler.END


async def reminder_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /reminder command."""
    if not update.message:
        return ConversationHandler.END

    buttons = []
    for minutes, label in REMINDER_OPTIONS:
        callback_data = f"rem_{minutes}" if minutes is not None else "rem_none"
        buttons.append([InlineKeyboardButton(label, callback_data=callback_data)])

    await update.message.reply_text(
        "Select default reminder for new meetings:\n\n"
        "_You can override this per-meeting using `r 10m` in your inline query._",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="Markdown",
    )

    return AWAITING_REMINDER


async def reminder_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle reminder button selection."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return ConversationHandler.END

    await query.answer()

    # Parse the reminder value
    value = query.data.replace("rem_", "")
    if value == "none":
        reminder = None
    else:
        reminder = value  # Store as string

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if user:
            await user_service.update_reminder(user, reminder)
            await session.commit()

    display = _format_reminder_setting(reminder)
    await query.edit_message_text(
        f"✅ Default reminder set to: {display}\n\n"
        "_Use `r` in your inline query to apply this default, "
        "or `r 10m` to override with a specific time._",
        parse_mode="Markdown"
    )
    return ConversationHandler.END


async def cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel any conversation."""
    if update.message:
        await update.message.reply_text("Cancelled.")
    return ConversationHandler.END


def setup_settings_handlers(app: Application) -> None:
    """Register settings handlers."""
    # Simple commands
    app.add_handler(CommandHandler("settings", settings_command))
    app.add_handler(CommandHandler("connect", connect_command))
    app.add_handler(CommandHandler("disconnect", disconnect_command))

    # Standalone timezone callback (handles tz_ buttons from OAuth and other contexts)
    # This must be registered BEFORE the ConversationHandler to catch callbacks
    # that happen outside the /timezone conversation
    app.add_handler(CallbackQueryHandler(timezone_callback_standalone, pattern=r"^tz_"))

    # Timezone conversation (for /timezone command flow)
    tz_handler = ConversationHandler(
        entry_points=[CommandHandler("timezone", timezone_command)],
        states={
            AWAITING_TIMEZONE: [
                CallbackQueryHandler(timezone_callback, pattern=r"^tz_"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, timezone_text),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )
    app.add_handler(tz_handler)

    # Duration conversation
    dur_handler = ConversationHandler(
        entry_points=[CommandHandler("duration", duration_command)],
        states={
            AWAITING_DURATION: [
                CallbackQueryHandler(duration_callback, pattern=r"^dur_"),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )
    app.add_handler(dur_handler)

    # Reminder conversation
    rem_handler = ConversationHandler(
        entry_points=[CommandHandler("reminder", reminder_command)],
        states={
            AWAITING_REMINDER: [
                CallbackQueryHandler(reminder_callback, pattern=r"^rem_"),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )
    app.add_handler(rem_handler)
