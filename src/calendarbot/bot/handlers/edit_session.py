"""Edit session handlers for private chat editing flow."""

import logging
import uuid
from datetime import UTC, datetime, timedelta

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from calendarbot.db.repository import EditSessionRepository
from calendarbot.db.session import async_session_factory
from calendarbot.i18n import get_text
from calendarbot.services.parser import MeetingParser
from calendarbot.services.user import UserService

logger = logging.getLogger(__name__)

# Time presets for the time selection grid
TIME_PRESETS_MORNING = ["08:00", "09:00", "10:00", "11:00"]
TIME_PRESETS_AFTERNOON = ["12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]


def _build_time_selection_keyboard(result_id: str, t) -> InlineKeyboardMarkup:
    """Build time selection keyboard with preset times."""
    buttons = []

    # Morning row
    morning_row = [
        InlineKeyboardButton(time, callback_data=f"time_{result_id}_{time.replace(':', '')}")
        for time in TIME_PRESETS_MORNING
    ]
    buttons.append(morning_row)

    # Afternoon rows (split for better display)
    afternoon_row1 = [
        InlineKeyboardButton(time, callback_data=f"time_{result_id}_{time.replace(':', '')}")
        for time in TIME_PRESETS_AFTERNOON[:4]
    ]
    buttons.append(afternoon_row1)

    afternoon_row2 = [
        InlineKeyboardButton(time, callback_data=f"time_{result_id}_{time.replace(':', '')}")
        for time in TIME_PRESETS_AFTERNOON[4:]
    ]
    buttons.append(afternoon_row2)

    # Custom and Back buttons
    buttons.append(
        [
            InlineKeyboardButton(
                t.inline.custom_time_button, callback_data=f"time_custom_{result_id}"
            ),
            InlineKeyboardButton(t.inline.back_button, callback_data=f"edit_{result_id}"),
        ]
    )

    return InlineKeyboardMarkup(buttons)


def _build_date_selection_keyboard(result_id: str, t) -> InlineKeyboardMarkup:
    """Build date selection keyboard with preset dates."""
    buttons = [
        [
            InlineKeyboardButton(t.inline.date_today, callback_data=f"date_{result_id}_today"),
            InlineKeyboardButton(
                t.inline.date_tomorrow, callback_data=f"date_{result_id}_tomorrow"
            ),
        ],
        [
            InlineKeyboardButton(
                t.inline.date_day_after, callback_data=f"date_{result_id}_dayafter"
            ),
            InlineKeyboardButton(
                t.inline.date_in_3_days, callback_data=f"date_{result_id}_in3days"
            ),
        ],
        [
            InlineKeyboardButton(
                t.inline.date_in_a_week, callback_data=f"date_{result_id}_inaweek"
            ),
        ],
        [
            InlineKeyboardButton(
                t.inline.custom_date_button, callback_data=f"date_custom_{result_id}"
            ),
            InlineKeyboardButton(t.inline.back_button, callback_data=f"edit_{result_id}"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)


async def create_edit_session(
    user_id: int,
    edit_type: str,
    meeting_data: dict,
    chat_id: int | None = None,
    message_id: int | None = None,
) -> str:
    """Create an edit session and return the session ID."""
    session_id = str(uuid.uuid4())[:8]

    async with async_session_factory() as session:
        repo = EditSessionRepository(session)
        await repo.create(
            session_id=session_id,
            user_id=user_id,
            edit_type=edit_type,
            meeting_data=meeting_data,
            chat_id=chat_id,
            message_id=message_id,
        )
        await session.commit()

    return session_id


async def handle_edit_session_start(
    update: Update, context: ContextTypes.DEFAULT_TYPE, session_id: str
) -> None:
    """Handle deep link for edit session."""
    if not update.message or not update.effective_user:
        return

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

        if not user:
            await update.message.reply_text(t.inline.session_expired_restart)
            return

        repo = EditSessionRepository(session)
        edit_session = await repo.get(session_id)

        if not edit_session:
            await update.message.reply_text(t.inline.session_expired_restart)
            return

        if edit_session.user_id != user.id:
            await update.message.reply_text(t.inline.session_expired_restart)
            return

        if edit_session.expires_at < datetime.now(UTC):
            await repo.delete(session_id)
            await session.commit()
            await update.message.reply_text(t.inline.session_expired_restart)
            return

    # Store session ID in user_data for text input handling
    if context.user_data is not None:
        context.user_data["edit_session_id"] = session_id

    # Show appropriate prompt based on edit_type
    if edit_session.edit_type == "title":
        await _show_title_input_prompt(update, context, edit_session, t)
    elif edit_session.edit_type == "attendee":
        await _show_attendee_input_prompt(update, context, edit_session, t)
    elif edit_session.edit_type == "link":
        await _show_link_input_prompt(update, context, edit_session, t)
    elif edit_session.edit_type == "time":
        await _show_time_input_prompt(update, context, edit_session, t)
    elif edit_session.edit_type == "date":
        await _show_date_input_prompt(update, context, edit_session, t)


async def _show_title_input_prompt(update, _context, edit_session, t) -> None:
    """Show title input prompt."""
    current = edit_session.meeting_data.get("meeting", {}).get("title", "")
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    t.inline.cancel_edit_button, callback_data=f"cancel_edit_{edit_session.id}"
                )
            ]
        ]
    )
    await update.message.reply_text(
        t.inline.enter_new_title.format(current=current),
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


async def _show_attendee_input_prompt(update, _context, edit_session, t) -> None:
    """Show attendee input prompt."""
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    t.inline.cancel_edit_button, callback_data=f"cancel_edit_{edit_session.id}"
                )
            ]
        ]
    )
    await update.message.reply_text(
        t.inline.add_attendee_prompt,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


async def _show_link_input_prompt(update, _context, edit_session, t) -> None:
    """Show link input prompt."""
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    t.inline.cancel_edit_button, callback_data=f"cancel_edit_{edit_session.id}"
                )
            ]
        ]
    )
    await update.message.reply_text(
        t.inline.enter_link_prompt,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


async def _show_time_input_prompt(update, _context, edit_session, t) -> None:
    """Show time input prompt for custom time entry."""
    current = edit_session.meeting_data.get("meeting", {}).get("time", "")
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    t.inline.cancel_edit_button, callback_data=f"cancel_edit_{edit_session.id}"
                )
            ]
        ]
    )
    await update.message.reply_text(
        t.inline.enter_new_time.format(current=current),
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


async def _show_date_input_prompt(update, _context, edit_session, t) -> None:
    """Show date input prompt for custom date entry."""
    current = edit_session.meeting_data.get("meeting", {}).get("date", "today")
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    t.inline.cancel_edit_button, callback_data=f"cancel_edit_{edit_session.id}"
                )
            ]
        ]
    )
    await update.message.reply_text(
        t.inline.enter_new_date.format(current=current),
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


async def handle_private_edit_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text input for edit sessions in private chat."""
    if not update.message or not update.effective_chat or not update.effective_user:
        return

    # Only handle private chats
    if update.effective_chat.type != "private":
        return

    if context.user_data is None:
        return

    session_id = context.user_data.get("edit_session_id")
    if not session_id:
        return

    text = update.message.text.strip() if update.message.text else ""
    if not text:
        return

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")
        user_timezone = user.timezone if user else "UTC"

        repo = EditSessionRepository(session)
        edit_session = await repo.get(session_id)

        if not edit_session:
            context.user_data.pop("edit_session_id", None)
            return

        if edit_session.expires_at < datetime.now(UTC):
            await repo.delete(session_id)
            await session.commit()
            context.user_data.pop("edit_session_id", None)
            await update.message.reply_text(t.inline.session_expired_restart)
            return

        # Process input based on edit_type
        meeting_data = edit_session.meeting_data
        m = meeting_data.get("meeting", {})
        result_id = meeting_data.get("result_id")
        success = False

        if edit_session.edit_type == "title":
            m["title"] = text
            success = True

        elif edit_session.edit_type == "attendee":
            if text.startswith("@"):
                username = text[1:]
                if username:
                    usernames = m.get("usernames", [])
                    if username.lower() not in [u.lower() for u in usernames]:
                        usernames.append(username)
                        m["usernames"] = usernames
                    success = True
            elif "@" in text and "." in text:
                attendees = m.get("attendees", [])
                if text.lower() not in [a.lower() for a in attendees]:
                    attendees.append(text)
                    m["attendees"] = attendees
                success = True
            else:
                await update.message.reply_text(t.inline.invalid_email_format)
                return

        elif edit_session.edit_type == "link":
            if text.startswith(("http://", "https://")):
                m["custom_link"] = text
                m["meet_link"] = None
                success = True
            else:
                await update.message.reply_text(t.inline.invalid_link_format)
                return

        elif edit_session.edit_type == "time":
            parsed = MeetingParser.parse_time_only(text)
            if parsed:
                m["time"] = parsed["time_str"]
                old_start = datetime.fromisoformat(m["start_datetime"])
                new_start = old_start.replace(
                    hour=parsed["hour"], minute=parsed["minute"], second=0, microsecond=0
                )
                old_end = datetime.fromisoformat(m["end_datetime"])
                duration = old_end - old_start
                new_end = new_start + duration
                m["start_datetime"] = new_start.isoformat()
                m["end_datetime"] = new_end.isoformat()
                success = True
            else:
                await update.message.reply_text(t.inline.invalid_time_format)
                return

        elif edit_session.edit_type == "date":
            parsed = MeetingParser.parse_date_only(text, user_timezone)
            if parsed:
                m["date"] = parsed["date_str"]
                old_start = datetime.fromisoformat(m["start_datetime"])
                old_end = datetime.fromisoformat(m["end_datetime"])
                duration = old_end - old_start
                new_start = old_start.replace(
                    year=parsed["year"], month=parsed["month"], day=parsed["day"]
                )
                new_end = new_start + duration
                m["start_datetime"] = new_start.isoformat()
                m["end_datetime"] = new_end.isoformat()
                success = True
            else:
                await update.message.reply_text(t.inline.invalid_date_format)
                return

        if success:
            meeting_data["meeting"] = m

            # Update meeting data in database
            await repo.update_meeting_data(session_id, meeting_data)

            # Also update in-memory if still available
            if context.bot_data and result_id and f"meeting_{result_id}" in context.bot_data:
                context.bot_data[f"meeting_{result_id}"] = meeting_data

            # Clean up session
            await repo.delete(session_id)
            await session.commit()

            context.user_data.pop("edit_session_id", None)

            # Confirm and instruct to return
            await update.message.reply_text(t.inline.edit_complete_return)


async def cancel_edit_session_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle cancel edit session callback."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    session_id = query.data.replace("cancel_edit_", "")

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

        repo = EditSessionRepository(session)
        await repo.delete(session_id)
        await session.commit()

    if context.user_data:
        context.user_data.pop("edit_session_id", None)

    await query.answer(t.inline.edit_cancelled)
    await query.edit_message_text(t.inline.edit_cancelled)


async def time_selection_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show time selection grid."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    result_id = query.data.replace("em_time_", "")

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

    if context.bot_data is None:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    meeting_data = context.bot_data.get(f"meeting_{result_id}")
    if not meeting_data:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    await query.answer()

    keyboard = _build_time_selection_keyboard(result_id, t)
    await query.edit_message_text(
        t.inline.select_time_title,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


async def set_time_preset_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle preset time selection."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    # Parse time_{id}_{HHMM}
    parts = query.data.split("_")
    if len(parts) != 3:
        return

    result_id = parts[1]
    time_str = parts[2]  # e.g., "0800"

    hour = int(time_str[:2])
    minute = int(time_str[2:])

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

    if context.bot_data is None:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    meeting_data = context.bot_data.get(f"meeting_{result_id}")
    if not meeting_data:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    m = meeting_data["meeting"]

    # Update time
    m["time"] = f"{hour:02d}:{minute:02d}"
    old_start = datetime.fromisoformat(m["start_datetime"])
    new_start = old_start.replace(hour=hour, minute=minute, second=0, microsecond=0)
    old_end = datetime.fromisoformat(m["end_datetime"])
    duration = old_end - old_start
    new_end = new_start + duration
    m["start_datetime"] = new_start.isoformat()
    m["end_datetime"] = new_end.isoformat()

    await query.answer(t.inline.field_updated.format(field="Time"))

    # Return to edit menu - need to import the function from inline.py
    from calendarbot.bot.handlers.inline import _build_edit_menu_keyboard

    keyboard = _build_edit_menu_keyboard(result_id, meeting_data, t)
    await query.edit_message_text(
        t.inline.edit_menu_title, parse_mode="Markdown", reply_markup=keyboard
    )


async def time_custom_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle custom time button - redirect to private chat."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    result_id = query.data.replace("time_custom_", "")

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

    if not user:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    if context.bot_data is None:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    meeting_data = context.bot_data.get(f"meeting_{result_id}")
    if not meeting_data:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    # Store result_id in meeting_data for later sync
    meeting_data["result_id"] = result_id

    # Create edit session for private chat
    session_id = await create_edit_session(
        user_id=user.id,
        edit_type="time",
        meeting_data=meeting_data,
        chat_id=update.effective_chat.id if update.effective_chat else None,
        message_id=update.effective_message.message_id if update.effective_message else None,
    )

    await query.answer()

    # Show "Continue in private chat" button
    bot = await context.bot.get_me()
    deep_link = f"https://t.me/{bot.username}?start=edit_{session_id}"

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(t.inline.open_private_chat, url=deep_link)],
            [InlineKeyboardButton(t.inline.back_button, callback_data=f"edit_{result_id}")],
        ]
    )

    await query.edit_message_text(
        f"{t.inline.continue_in_private}\n\n{t.inline.custom_time_button}",
        reply_markup=keyboard,
    )


async def date_selection_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show date selection grid."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    result_id = query.data.replace("em_date_", "")

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

    if context.bot_data is None:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    meeting_data = context.bot_data.get(f"meeting_{result_id}")
    if not meeting_data:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    await query.answer()

    keyboard = _build_date_selection_keyboard(result_id, t)
    await query.edit_message_text(
        t.inline.select_date_title,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


async def set_date_preset_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle preset date selection."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    # Parse date_{id}_{preset}
    parts = query.data.split("_")
    if len(parts) != 3:
        return

    result_id = parts[1]
    preset = parts[2]  # today, tomorrow, dayafter, in3days, inaweek

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

    if context.bot_data is None:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    meeting_data = context.bot_data.get(f"meeting_{result_id}")
    if not meeting_data:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    m = meeting_data["meeting"]

    # Calculate target date
    today = datetime.now().date()
    if preset == "today":
        target_date = today
    elif preset == "tomorrow":
        target_date = today + timedelta(days=1)
    elif preset == "dayafter":
        target_date = today + timedelta(days=2)
    elif preset == "in3days":
        target_date = today + timedelta(days=3)
    elif preset == "inaweek":
        target_date = today + timedelta(days=7)
    else:
        await query.answer()
        return

    # Update date
    m["date"] = target_date.strftime("%d-%m-%Y")
    old_start = datetime.fromisoformat(m["start_datetime"])
    old_end = datetime.fromisoformat(m["end_datetime"])
    duration = old_end - old_start
    new_start = old_start.replace(
        year=target_date.year, month=target_date.month, day=target_date.day
    )
    new_end = new_start + duration
    m["start_datetime"] = new_start.isoformat()
    m["end_datetime"] = new_end.isoformat()

    await query.answer(t.inline.field_updated.format(field="Date"))

    # Return to edit menu
    from calendarbot.bot.handlers.inline import _build_edit_menu_keyboard

    keyboard = _build_edit_menu_keyboard(result_id, meeting_data, t)
    await query.edit_message_text(
        t.inline.edit_menu_title, parse_mode="Markdown", reply_markup=keyboard
    )


async def date_custom_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle custom date button - redirect to private chat."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    result_id = query.data.replace("date_custom_", "")

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

    if not user:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    if context.bot_data is None:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    meeting_data = context.bot_data.get(f"meeting_{result_id}")
    if not meeting_data:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    # Store result_id in meeting_data for later sync
    meeting_data["result_id"] = result_id

    # Create edit session for private chat
    session_id = await create_edit_session(
        user_id=user.id,
        edit_type="date",
        meeting_data=meeting_data,
        chat_id=update.effective_chat.id if update.effective_chat else None,
        message_id=update.effective_message.message_id if update.effective_message else None,
    )

    await query.answer()

    # Show "Continue in private chat" button
    bot = await context.bot.get_me()
    deep_link = f"https://t.me/{bot.username}?start=edit_{session_id}"

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(t.inline.open_private_chat, url=deep_link)],
            [InlineKeyboardButton(t.inline.back_button, callback_data=f"edit_{result_id}")],
        ]
    )

    await query.edit_message_text(
        f"{t.inline.continue_in_private}\n\n{t.inline.custom_date_button}",
        reply_markup=keyboard,
    )


async def title_private_chat_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle title edit button - redirect to private chat."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    result_id = query.data.replace("em_title_", "")

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

    if not user:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    if context.bot_data is None:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    meeting_data = context.bot_data.get(f"meeting_{result_id}")
    if not meeting_data:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    # Store result_id in meeting_data for later sync
    meeting_data["result_id"] = result_id

    # Create edit session for private chat
    session_id = await create_edit_session(
        user_id=user.id,
        edit_type="title",
        meeting_data=meeting_data,
        chat_id=update.effective_chat.id if update.effective_chat else None,
        message_id=update.effective_message.message_id if update.effective_message else None,
    )

    await query.answer()

    # Show "Continue in private chat" button
    bot = await context.bot.get_me()
    deep_link = f"https://t.me/{bot.username}?start=edit_{session_id}"

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(t.inline.open_private_chat, url=deep_link)],
            [InlineKeyboardButton(t.inline.back_button, callback_data=f"edit_{result_id}")],
        ]
    )

    await query.edit_message_text(
        f"{t.inline.continue_in_private}\n\n{t.inline.edit_title_button}",
        reply_markup=keyboard,
    )


async def attendee_private_chat_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle attendee add button - redirect to private chat for manual entry."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    result_id = query.data.replace("att_add_", "")

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

    if not user:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    if context.bot_data is None:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    meeting_data = context.bot_data.get(f"meeting_{result_id}")
    if not meeting_data:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    # Store result_id in meeting_data for later sync
    meeting_data["result_id"] = result_id

    # Create edit session for private chat
    session_id = await create_edit_session(
        user_id=user.id,
        edit_type="attendee",
        meeting_data=meeting_data,
        chat_id=update.effective_chat.id if update.effective_chat else None,
        message_id=update.effective_message.message_id if update.effective_message else None,
    )

    await query.answer()

    # Show "Continue in private chat" button
    bot = await context.bot.get_me()
    deep_link = f"https://t.me/{bot.username}?start=edit_{session_id}"

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(t.inline.open_private_chat, url=deep_link)],
            [InlineKeyboardButton(t.inline.back_button, callback_data=f"em_att_{result_id}")],
        ]
    )

    await query.edit_message_text(
        f"{t.inline.continue_in_private}\n\n{t.inline.type_manually_button}",
        reply_markup=keyboard,
    )


async def link_private_chat_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle custom link button - redirect to private chat."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    result_id = query.data.replace("link_custom_", "")

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

    if not user:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    if context.bot_data is None:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    meeting_data = context.bot_data.get(f"meeting_{result_id}")
    if not meeting_data:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    # Store result_id in meeting_data for later sync
    meeting_data["result_id"] = result_id

    # Create edit session for private chat
    session_id = await create_edit_session(
        user_id=user.id,
        edit_type="link",
        meeting_data=meeting_data,
        chat_id=update.effective_chat.id if update.effective_chat else None,
        message_id=update.effective_message.message_id if update.effective_message else None,
    )

    await query.answer()

    # Show "Continue in private chat" button
    bot = await context.bot.get_me()
    deep_link = f"https://t.me/{bot.username}?start=edit_{session_id}"

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(t.inline.open_private_chat, url=deep_link)],
            [InlineKeyboardButton(t.inline.back_button, callback_data=f"em_link_{result_id}")],
        ]
    )

    await query.edit_message_text(
        f"{t.inline.continue_in_private}\n\n{t.inline.paste_custom_link}",
        reply_markup=keyboard,
    )


def setup_edit_session_handlers(app: Application) -> None:
    """Register edit session handlers."""
    # Cancel edit session
    app.add_handler(CallbackQueryHandler(cancel_edit_session_callback, pattern=r"^cancel_edit_"))

    # Time selection grid and presets
    app.add_handler(CallbackQueryHandler(time_selection_callback, pattern=r"^em_time_"))
    app.add_handler(CallbackQueryHandler(set_time_preset_callback, pattern=r"^time_[^c]"))
    app.add_handler(CallbackQueryHandler(time_custom_callback, pattern=r"^time_custom_"))

    # Date selection grid and presets
    app.add_handler(CallbackQueryHandler(date_selection_callback, pattern=r"^em_date_"))
    app.add_handler(CallbackQueryHandler(set_date_preset_callback, pattern=r"^date_[^c]"))
    app.add_handler(CallbackQueryHandler(date_custom_callback, pattern=r"^date_custom_"))

    # Title, attendee, and link redirects to private chat
    app.add_handler(CallbackQueryHandler(title_private_chat_callback, pattern=r"^em_title_"))
    app.add_handler(CallbackQueryHandler(attendee_private_chat_callback, pattern=r"^att_add_"))
    app.add_handler(CallbackQueryHandler(link_private_chat_callback, pattern=r"^link_custom_"))

    # Private chat text input handler (high group number to not interfere)
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE,
            handle_private_edit_text,
        ),
        group=4,  # Higher priority than inline handler in group 5
    )
