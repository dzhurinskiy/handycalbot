"""Meeting management command handlers."""

import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from calendarbot.db.session import async_session_factory
from calendarbot.services.calendar import CalendarService
from calendarbot.services.user import UserService

logger = logging.getLogger(__name__)


async def meetings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /meetings command - list upcoming meetings."""
    if not update.effective_user or not update.message:
        return

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if not user:
            await update.message.reply_text("Please run /start first.")
            return

        if not await user_service.is_calendar_connected(user):
            await update.message.reply_text(
                "Please connect your Google Calendar first with /connect"
            )
            return

        calendar_service = CalendarService(session)
        meetings = await calendar_service.get_upcoming_meetings(user, limit=10)

    if not meetings:
        await update.message.reply_text("No upcoming meetings found.")
        return

    text = "**Upcoming Meetings** 📅\n\n"

    for m in meetings:
        start = m["start_time"].strftime("%H:%M %d %b")
        end = m["end_time"].strftime("%H:%M")
        attendee_count = len(m["attendees"])

        text += f"• **{m['title']}**\n"
        text += f"  🕐 {start} - {end}\n"
        if attendee_count > 0:
            text += f"  👥 {attendee_count} attendee(s)\n"
        text += "\n"

    text += "_Use /cancel to cancel a meeting_"

    await update.message.reply_text(text, parse_mode="Markdown")


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /cancel command - show meetings to cancel."""
    if not update.effective_user or not update.message:
        return

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if not user:
            await update.message.reply_text("Please run /start first.")
            return

        if not await user_service.is_calendar_connected(user):
            await update.message.reply_text(
                "Please connect your Google Calendar first with /connect"
            )
            return

        calendar_service = CalendarService(session)
        meetings = await calendar_service.get_upcoming_meetings(user, limit=10)

    if not meetings:
        await update.message.reply_text("No upcoming meetings to cancel.")
        return

    buttons = []
    for m in meetings:
        start = m["start_time"].strftime("%H:%M %d %b")
        label = f"{m['title'][:20]} - {start}"
        buttons.append([InlineKeyboardButton(label, callback_data=f"cancel_{m['id']}")])

    buttons.append([InlineKeyboardButton("❌ Don't cancel anything", callback_data="cancel_none")])

    await update.message.reply_text(
        "Select a meeting to cancel:",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def cancel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle cancel meeting button press."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    await query.answer()

    if query.data == "cancel_none":
        await query.edit_message_text("No meeting cancelled.")
        return

    meeting_id = int(query.data.replace("cancel_", ""))

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if not user:
            await query.edit_message_text("Error: User not found.")
            return

        calendar_service = CalendarService(session)
        result = await calendar_service.cancel_meeting(user, meeting_id)
        await session.commit()

    if "error" in result:
        await query.edit_message_text(f"Error: {result['error']}")
    else:
        await query.edit_message_text(
            f"Meeting cancelled: **{result['title']}**",
            parse_mode="Markdown",
        )


def setup_meeting_handlers(app: Application) -> None:
    """Register meeting handlers."""
    app.add_handler(CommandHandler("meetings", meetings_command))
    app.add_handler(CommandHandler("cancel", cancel_command))
    app.add_handler(CallbackQueryHandler(cancel_callback, pattern=r"^cancel_"))
