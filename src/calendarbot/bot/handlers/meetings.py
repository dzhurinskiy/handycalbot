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


MEETINGS_PER_PAGE = 5


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /cancel command - show meetings to cancel."""
    if not update.effective_user or not update.message:
        return

    try:
        await show_cancel_menu(update, context, page=0, is_callback=False)
    except Exception as e:
        logger.exception(f"Error in cancel_command: {e}")
        await update.message.reply_text(f"Error loading meetings: {str(e)}")


async def show_cancel_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    page: int = 0,
    is_callback: bool = False,
) -> None:
    """Show paginated list of meetings to cancel."""
    user_id = update.effective_user.id if update.effective_user else None
    if not user_id:
        logger.warning("show_cancel_menu called without user_id")
        return

    async def send_message(text: str, reply_markup=None):
        """Helper to send message based on context."""
        if is_callback and update.callback_query:
            await update.callback_query.edit_message_text(
                text, reply_markup=reply_markup, parse_mode="Markdown"
            )
        elif update.message:
            await update.message.reply_text(
                text, reply_markup=reply_markup, parse_mode="Markdown"
            )

    try:
        async with async_session_factory() as session:
            user_service = UserService(session)
            user = await user_service.get_user(user_id)

            if not user:
                await send_message("Please run /start first.")
                return

            if not await user_service.is_calendar_connected(user):
                await send_message("Please connect your Google Calendar first with /connect")
                return

            calendar_service = CalendarService(session)
            # Fetch more meetings to enable pagination
            all_meetings = await calendar_service.get_upcoming_meetings(user, limit=50)
    except Exception as e:
        logger.exception(f"Error fetching meetings for cancel: {e}")
        await send_message(f"Error fetching meetings: {str(e)}")
        return

    if not all_meetings:
        await send_message("No upcoming meetings to cancel.")
        return

    # Store meeting IDs in context.bot_data with short keys
    # (Google Calendar event IDs can be very long, exceeding Telegram's 64-byte callback_data limit)
    if context.bot_data is None:
        context.bot_data = {}

    # Create a mapping for this user's cancel session
    cancel_key = f"cancel_meetings_{user_id}"
    context.bot_data[cancel_key] = {str(i): m["id"] for i, m in enumerate(all_meetings)}

    # Pagination
    total_meetings = len(all_meetings)
    start_idx = page * MEETINGS_PER_PAGE
    end_idx = start_idx + MEETINGS_PER_PAGE
    meetings_page = all_meetings[start_idx:end_idx]

    if not meetings_page:
        # Page out of range, show first page
        page = 0
        start_idx = 0
        end_idx = MEETINGS_PER_PAGE
        meetings_page = all_meetings[start_idx:end_idx]

    # Build meeting buttons using short numeric indices
    buttons = []
    for idx, m in enumerate(meetings_page):
        global_idx = start_idx + idx  # Index in full list
        start = m["start_time"].strftime("%H:%M %d %b")
        title = m["title"][:25] + "..." if len(m["title"]) > 25 else m["title"]
        attendees = len(m.get("attendees", []))
        attendee_str = f" 👥{attendees}" if attendees > 0 else ""
        label = f"🗑 {title} | {start}{attendee_str}"
        # Use short index instead of full event ID
        buttons.append([InlineKeyboardButton(label, callback_data=f"cm_{user_id}_{global_idx}")])

    # Navigation buttons
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"cp_{user_id}_{page - 1}"))
    if end_idx < total_meetings:
        nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"cp_{user_id}_{page + 1}"))
    if nav_buttons:
        buttons.append(nav_buttons)

    # Cancel button
    buttons.append([InlineKeyboardButton("❌ Don't cancel anything", callback_data="cancel_none")])

    # Header text
    page_info = f"Page {page + 1}/{(total_meetings + MEETINGS_PER_PAGE - 1) // MEETINGS_PER_PAGE}"
    text = f"**Select a meeting to cancel:**\n_{page_info} • {total_meetings} total meetings_"

    await send_message(text, reply_markup=InlineKeyboardMarkup(buttons))


async def cancel_page_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle pagination buttons for cancel menu."""
    query = update.callback_query
    if not query or not query.data:
        return

    await query.answer()

    try:
        # Extract page number from format: cp_{user_id}_{page}
        parts = query.data.split("_")
        page = int(parts[2])
        await show_cancel_menu(update, context, page=page, is_callback=True)
    except Exception as e:
        logger.exception(f"Error in cancel_page_callback: {e}")
        await query.edit_message_text(f"Error: {str(e)}")


async def cancel_meeting_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle cancel meeting button press."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    await query.answer("Cancelling meeting...")

    try:
        # Extract user_id and index from format: cm_{user_id}_{index}
        parts = query.data.split("_")
        stored_user_id = int(parts[1])
        meeting_idx = parts[2]

        # Verify user
        if stored_user_id != update.effective_user.id:
            await query.edit_message_text("Error: This is not your cancel menu.")
            return

        # Get actual event ID from stored mapping
        cancel_key = f"cancel_meetings_{stored_user_id}"
        if not context.bot_data or cancel_key not in context.bot_data:
            await query.edit_message_text("Error: Session expired. Please use /cancel again.")
            return

        event_id = context.bot_data[cancel_key].get(meeting_idx)
        if not event_id:
            await query.edit_message_text("Error: Meeting not found. Please use /cancel again.")
            return

        async with async_session_factory() as session:
            user_service = UserService(session)
            user = await user_service.get_user(update.effective_user.id)

            if not user:
                await query.edit_message_text("Error: User not found.")
                return

            calendar_service = CalendarService(session)
            result = await calendar_service.cancel_meeting(user, event_id)
            await session.commit()

        # Clean up stored data
        context.bot_data.pop(cancel_key, None)

        if "error" in result:
            await query.edit_message_text(f"❌ Error: {result['error']}")
        else:
            await query.edit_message_text(
                f"✅ Meeting cancelled: **{result['title']}**\n\n"
                "_Attendees will be notified automatically._",
                parse_mode="Markdown",
            )
    except Exception as e:
        logger.exception(f"Error in cancel_meeting_callback: {e}")
        await query.edit_message_text(f"Error cancelling meeting: {str(e)}")


async def cancel_none_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle 'Don't cancel' button press."""
    query = update.callback_query
    if not query:
        return

    await query.answer()
    await query.edit_message_text("No meeting cancelled.")


def setup_meeting_handlers(app: Application) -> None:
    """Register meeting handlers."""
    app.add_handler(CommandHandler("meetings", meetings_command))
    app.add_handler(CommandHandler("cancel", cancel_command))
    # Cancel menu callbacks - patterns use short format to fit Telegram's 64-byte limit
    # cm_{user_id}_{index} - cancel meeting
    # cp_{user_id}_{page} - change page
    app.add_handler(CallbackQueryHandler(cancel_none_callback, pattern=r"^cancel_none$"))
    app.add_handler(CallbackQueryHandler(cancel_page_callback, pattern=r"^cp_\d+_\d+$"))
    app.add_handler(CallbackQueryHandler(cancel_meeting_callback, pattern=r"^cm_\d+_\d+$"))
