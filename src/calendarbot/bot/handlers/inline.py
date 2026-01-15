"""Inline query handler for meeting creation."""

import logging
import uuid

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Update,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    ChosenInlineResultHandler,
    ContextTypes,
    InlineQueryHandler,
)

from calendarbot.db.session import async_session_factory
from calendarbot.services.calendar import CalendarService
from calendarbot.services.parser import MeetingParser
from calendarbot.services.user import UserService

logger = logging.getLogger(__name__)


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline queries - parse meeting command and show preview."""
    query = update.inline_query
    if not query or not query.from_user:
        return

    text = query.query.strip()

    if not text:
        # Show help when empty
        results = [
            InlineQueryResultArticle(
                id="help",
                title="How to create a meeting",
                description='Type: 14:30 "Meeting Title" email@example.com',
                input_message_content=InputTextMessageContent(
                    "To create a meeting, type:\n"
                    '@handycalbot 14:30 "Meeting Title" email@example.com\n\n'
                    "Format: TIME [DATE] \"TITLE\" [EMAILS]"
                ),
            )
        ]
        await query.answer(results, cache_time=300)
        return

    # Get user settings
    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(query.from_user.id)

        if not user:
            results = [
                InlineQueryResultArticle(
                    id="not_registered",
                    title="Please start the bot first",
                    description="Click to open bot and run /start",
                    input_message_content=InputTextMessageContent(
                        "Please start @handycalbot first by sending /start"
                    ),
                )
            ]
            await query.answer(results, cache_time=60)
            return

        # Check if calendar is connected
        calendar_connected = await user_service.is_calendar_connected(user)

    # Parse the query
    parser = MeetingParser(
        user_timezone=user.timezone if user else "UTC",
        default_duration=user.default_duration if user else 60,
    )
    meeting = parser.parse(text)

    if not meeting:
        results = [
            InlineQueryResultArticle(
                id="parse_error",
                title="Could not parse meeting",
                description='Use format: 14:30 "Meeting Title" emails...',
                input_message_content=InputTextMessageContent(
                    "Could not parse meeting. Use format:\n"
                    '14:30 "Meeting Title" email@example.com\n\n'
                    "Time and title in quotes are required."
                ),
            )
        ]
        await query.answer(results, cache_time=10)
        return

    # Generate preview
    preview = parser.format_preview(meeting)

    if not calendar_connected:
        preview += "\n\n⚠️ Calendar not connected - /connect first"

    # Generate unique ID for this meeting
    result_id = str(uuid.uuid4())

    # Store meeting data temporarily for creation
    if context.bot_data is None:
        context.bot_data = {}
    context.bot_data[f"meeting_{result_id}"] = {
        "user_id": query.from_user.id,
        "meeting": {
            "time": meeting.time,
            "date": meeting.date,
            "title": meeting.title,
            "attendees": meeting.attendees,
            "start_datetime": meeting.start_datetime.isoformat(),
            "end_datetime": meeting.end_datetime.isoformat(),
        },
    }

    # Create inline keyboard for confirmation
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Create Meeting", callback_data=f"create_{result_id}"),
            InlineKeyboardButton("❌ Cancel", callback_data=f"discard_{result_id}"),
        ]
    ])

    results = [
        InlineQueryResultArticle(
            id=result_id,
            title=f"📅 {meeting.title}",
            description=f"{meeting.time} {meeting.date or 'today'} • {len(meeting.attendees)} attendee(s)",
            input_message_content=InputTextMessageContent(
                preview,
                parse_mode=None,
            ),
            reply_markup=keyboard,
        )
    ]

    await query.answer(results, cache_time=0, is_personal=True)


async def create_meeting_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle Create Meeting button press."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    await query.answer("Creating meeting...")

    result_id = query.data.replace("create_", "")

    # Get stored meeting data
    if context.bot_data is None:
        await query.edit_message_text("Error: Meeting data expired. Please try again.")
        return

    meeting_data = context.bot_data.get(f"meeting_{result_id}")
    if not meeting_data:
        await query.edit_message_text("Error: Meeting data expired. Please try again.")
        return

    # Verify user
    if meeting_data["user_id"] != update.effective_user.id:
        await query.answer("This is not your meeting!", show_alert=True)
        return

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if not user:
            await query.edit_message_text("Error: User not found. Please /start the bot.")
            return

        # Reconstruct ParsedMeeting
        from datetime import datetime
        from calendarbot.services.parser import ParsedMeeting

        m = meeting_data["meeting"]
        parsed = ParsedMeeting(
            time=m["time"],
            date=m["date"],
            title=m["title"],
            attendees=m["attendees"],
            start_datetime=datetime.fromisoformat(m["start_datetime"]),
            end_datetime=datetime.fromisoformat(m["end_datetime"]),
        )

        calendar_service = CalendarService(session)
        result = await calendar_service.create_meeting(user, parsed)
        await session.commit()

    # Clean up stored data
    del context.bot_data[f"meeting_{result_id}"]

    if "error" in result:
        await query.edit_message_text(f"❌ Error: {result['error']}")
    else:
        start_str = result["start"].strftime("%H:%M on %d %b %Y")
        text = f"✅ Meeting created!\n\n"
        text += f"**{result['title']}**\n"
        text += f"🕐 {start_str}\n"
        if result["attendees"]:
            text += f"👥 Invites sent to: {', '.join(result['attendees'])}\n"
        if result.get("link"):
            text += f"\n[Open in Google Calendar]({result['link']})"

        await query.edit_message_text(text, parse_mode="Markdown")


async def discard_meeting_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle Cancel button press."""
    query = update.callback_query
    if not query or not query.data:
        return

    await query.answer("Cancelled")

    result_id = query.data.replace("discard_", "")

    # Clean up stored data
    if context.bot_data:
        context.bot_data.pop(f"meeting_{result_id}", None)

    await query.edit_message_text("Meeting cancelled.")


def setup_inline_handlers(app: Application) -> None:
    """Register inline query handlers."""
    app.add_handler(InlineQueryHandler(inline_query))
    app.add_handler(CallbackQueryHandler(create_meeting_callback, pattern=r"^create_"))
    app.add_handler(CallbackQueryHandler(discard_meeting_callback, pattern=r"^discard_"))
