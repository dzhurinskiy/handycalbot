"""Feedback command handler."""

import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from calendarbot.config import get_settings
from calendarbot.db.session import async_session_factory
from calendarbot.i18n import get_text
from calendarbot.services.user import UserService

logger = logging.getLogger(__name__)

# Conversation state
AWAITING_FEEDBACK = 1


async def feedback_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /feedback command - prompt user to send feedback."""
    if not update.effective_user or not update.message:
        return ConversationHandler.END

    # Get user's language
    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

    await update.message.reply_text(
        f"{t.feedback.feedback_title}\n\n"
        f"{t.feedback.feedback_prompt}\n"
        f"{t.feedback.feedback_abort_hint}",
        parse_mode="Markdown",
    )

    return AWAITING_FEEDBACK


async def receive_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle received feedback message."""
    if not update.message or not update.message.text or not update.effective_user:
        return ConversationHandler.END

    settings = get_settings()
    feedback_text = update.message.text

    # Get user's language for admin notification
    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        user_lang = user.language if user else "en"

    # Forward to admin if configured
    if settings.admin_chat_id:
        try:
            user_info = (
                f"@{update.effective_user.username}"
                if update.effective_user.username
                else f"ID: {update.effective_user.id}"
            )
            user_name = update.effective_user.full_name or "Unknown"

            admin_message = (
                f"📬 **New Feedback**\n\n"
                f"**From:** {user_name} ({user_info})\n"
                f"**Language:** {user_lang}\n\n"
                f"**Message:**\n{feedback_text}"
            )

            await context.bot.send_message(
                chat_id=settings.admin_chat_id,
                text=admin_message,
                parse_mode="Markdown",
            )
            logger.info(f"Feedback forwarded from user {update.effective_user.id}")
        except Exception as e:
            logger.error(f"Failed to forward feedback to admin: {e}")

    # Thank the user
    t = get_text(user_lang)
    await update.message.reply_text(
        f"{t.feedback.feedback_received}\n\n" f"{t.feedback.feedback_thank_you}",
        parse_mode="Markdown",
    )

    return ConversationHandler.END


async def abort_feedback(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> int:
    """Abort feedback submission."""
    if update.message:
        async with async_session_factory() as session:
            user_service = UserService(session)
            user = (
                await user_service.get_user(update.effective_user.id)
                if update.effective_user
                else None
            )
            t = get_text(user.language if user else "en")
        await update.message.reply_text(t.common.aborted)
    return ConversationHandler.END


def setup_feedback_handlers(app: Application) -> None:
    """Register feedback handlers."""
    feedback_handler = ConversationHandler(
        entry_points=[CommandHandler("feedback", feedback_command)],
        states={
            AWAITING_FEEDBACK: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_feedback),
            ],
        },
        fallbacks=[
            CommandHandler("abort", abort_feedback),
            MessageHandler(filters.COMMAND, abort_feedback),
        ],
    )
    app.add_handler(feedback_handler)
