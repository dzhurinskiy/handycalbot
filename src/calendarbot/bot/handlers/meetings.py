"""Meeting management command handlers."""

import logging
import secrets
from datetime import datetime, timedelta

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from calendarbot.db.session import async_session_factory
from calendarbot.i18n import get_text
from calendarbot.services.calendar import CalendarService
from calendarbot.services.user import UserService
from calendarbot.utils.timezone import TimezoneHelper

logger = logging.getLogger(__name__)

MEETINGS_PER_PAGE = 5


async def meetings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /meetings command - show paginated meeting list."""
    if not update.effective_user or not update.message:
        return

    try:
        await show_meetings_list(update, context, page=0, is_callback=False)
    except Exception as e:
        logger.exception(f"Error in meetings_command: {e}")
        await update.message.reply_text(f"Error loading meetings: {str(e)}")


async def show_meetings_list(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    page: int = 0,
    is_callback: bool = False,
) -> None:
    """Show paginated list of meetings with clickable buttons."""
    user_id = update.effective_user.id if update.effective_user else None
    if not user_id:
        return

    async def send_message(text: str, reply_markup=None):
        if is_callback and update.callback_query:
            await update.callback_query.edit_message_text(
                text, reply_markup=reply_markup, parse_mode="Markdown"
            )
        elif update.message:
            await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

    try:
        async with async_session_factory() as session:
            user_service = UserService(session)
            user = await user_service.get_user(user_id)

            if not user:
                t = get_text("en")
                await send_message(t.common.please_start_first)
                return

            t = get_text(user.language)

            if not await user_service.is_calendar_connected(user):
                await send_message(t.settings.click_to_connect.split("\n")[0])
                return

            calendar_service = CalendarService(session)
            all_meetings, is_privacy_mode = await calendar_service.get_upcoming_meetings(
                user, limit=50
            )
    except Exception as e:
        logger.exception(f"Error fetching meetings: {e}")
        await send_message(f"Error fetching meetings: {str(e)}")
        return

    if not all_meetings:
        no_meetings_text = t.meetings.no_upcoming_meetings
        if is_privacy_mode:
            no_meetings_text += f"\n\n{t.meetings.privacy_mode_note}"
        await send_message(no_meetings_text)
        return

    # Store meetings in context for detail view
    if context.bot_data is None:
        context.bot_data = {}
    meetings_key = f"meetings_{user_id}"
    context.bot_data[meetings_key] = all_meetings

    # Pagination
    total_meetings = len(all_meetings)
    start_idx = page * MEETINGS_PER_PAGE
    end_idx = start_idx + MEETINGS_PER_PAGE
    meetings_page = all_meetings[start_idx:end_idx]

    if not meetings_page:
        page = 0
        start_idx = 0
        end_idx = MEETINGS_PER_PAGE
        meetings_page = all_meetings[start_idx:end_idx]

    # Build meeting buttons
    buttons = []
    for idx, m in enumerate(meetings_page):
        global_idx = start_idx + idx
        start_time = m["start_time"]
        start_str = start_time.strftime("%H:%M %d %b")
        title = m["title"][:25] + "..." if len(m["title"]) > 25 else m["title"]
        attendees = len(m.get("attendees", []))
        attendee_str = f" 👥{attendees}" if attendees > 0 else ""
        label = f"📅 {title} | {start_str}{attendee_str}"
        buttons.append([InlineKeyboardButton(label, callback_data=f"md_{user_id}_{global_idx}")])

    # Navigation buttons
    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                t.meetings.previous_button, callback_data=f"ml_{user_id}_{page - 1}"
            )
        )
    if end_idx < total_meetings:
        nav_buttons.append(
            InlineKeyboardButton(t.meetings.next_button, callback_data=f"ml_{user_id}_{page + 1}")
        )
    if nav_buttons:
        buttons.append(nav_buttons)

    # Close button
    buttons.append([InlineKeyboardButton(t.meetings.close_button, callback_data="meetings_close")])

    # Header text
    total_pages = (total_meetings + MEETINGS_PER_PAGE - 1) // MEETINGS_PER_PAGE
    page_info = t.meetings.page_info.format(current=page + 1, total=total_pages)
    text = f"{t.meetings.upcoming_meetings}\n_{page_info} - {t.meetings.total_meetings.format(count=total_meetings)}_"

    if is_privacy_mode:
        text += f"\n\n{t.meetings.privacy_mode_note}"

    await send_message(text, reply_markup=InlineKeyboardMarkup(buttons))


async def meetings_page_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle pagination for meetings list."""
    query = update.callback_query
    if not query or not query.data:
        return

    await query.answer()

    try:
        parts = query.data.split("_")
        page = int(parts[2])
        await show_meetings_list(update, context, page=page, is_callback=True)
    except Exception as e:
        logger.exception(f"Error in meetings_page_callback: {e}")
        await query.edit_message_text(f"Error: {str(e)}")


async def meeting_detail_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show meeting details with Edit/Cancel/Back buttons."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    await query.answer()

    try:
        parts = query.data.split("_")
        stored_user_id = int(parts[1])
        meeting_idx = int(parts[2])

        if stored_user_id != update.effective_user.id:
            return

        meetings_key = f"meetings_{stored_user_id}"
        if not context.bot_data or meetings_key not in context.bot_data:
            async with async_session_factory() as session:
                user_service = UserService(session)
                user = await user_service.get_user(update.effective_user.id)
                t = get_text(user.language if user else "en")
            await query.edit_message_text(t.meetings.session_expired)
            return

        meetings = context.bot_data[meetings_key]
        if meeting_idx >= len(meetings):
            async with async_session_factory() as session:
                user_service = UserService(session)
                user = await user_service.get_user(update.effective_user.id)
                t = get_text(user.language if user else "en")
            await query.edit_message_text(t.meetings.meeting_not_found)
            return

        m = meetings[meeting_idx]

        async with async_session_factory() as session:
            user_service = UserService(session)
            user = await user_service.get_user(update.effective_user.id)
            t = get_text(user.language if user else "en")

        # Format meeting details
        start_time = m["start_time"]
        end_time = m["end_time"]
        duration_mins = int((end_time - start_time).total_seconds() / 60)

        # Format duration display
        if duration_mins >= 60:
            hours = duration_mins // 60
            mins = duration_mins % 60
            duration_str = f"{hours}h" + (f" {mins}m" if mins else "")
        else:
            duration_str = f"{duration_mins}m"

        text = f"📅 **{m['title']}**\n\n"
        text += f"🕐 {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}\n"
        text += f"📆 {start_time.strftime('%a, %d %b %Y')}\n"
        text += f"⏱️ {duration_str}\n"

        attendees = m.get("attendees", [])
        if attendees:
            attendee_list = ", ".join(attendees[:5])
            if len(attendees) > 5:
                attendee_list += f" (+{len(attendees) - 5})"
            text += f"👥 {attendee_list}\n"

        # Store current meeting index for edit operations
        context.bot_data[f"current_meeting_{stored_user_id}"] = meeting_idx

        buttons = [
            [
                InlineKeyboardButton(
                    t.meetings.edit_button, callback_data=f"me_{stored_user_id}_{meeting_idx}"
                ),
                InlineKeyboardButton(
                    t.meetings.cancel_meeting_button,
                    callback_data=f"mc_{stored_user_id}_{meeting_idx}",
                ),
            ],
            [
                InlineKeyboardButton(
                    t.meetings.back_to_list_button, callback_data=f"ml_{stored_user_id}_0"
                )
            ],
        ]

        await query.edit_message_text(
            text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="Markdown"
        )

    except Exception as e:
        logger.exception(f"Error in meeting_detail_callback: {e}")
        await query.edit_message_text(f"Error: {str(e)}")


async def meeting_edit_menu_callback(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show edit menu with field buttons."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    await query.answer()

    try:
        parts = query.data.split("_")
        stored_user_id = int(parts[1])
        meeting_idx = int(parts[2])

        if stored_user_id != update.effective_user.id:
            return

        async with async_session_factory() as session:
            user_service = UserService(session)
            user = await user_service.get_user(update.effective_user.id)
            t = get_text(user.language if user else "en")

        text = t.meetings.edit_menu_title

        buttons = [
            [
                InlineKeyboardButton(
                    t.meetings.edit_title_btn, callback_data=f"met_{stored_user_id}_{meeting_idx}"
                ),
                InlineKeyboardButton(
                    t.meetings.edit_time_btn, callback_data=f"meti_{stored_user_id}_{meeting_idx}"
                ),
            ],
            [
                InlineKeyboardButton(
                    t.meetings.edit_date_btn, callback_data=f"meda_{stored_user_id}_{meeting_idx}"
                ),
                InlineKeyboardButton(
                    t.meetings.edit_duration_btn,
                    callback_data=f"medu_{stored_user_id}_{meeting_idx}",
                ),
            ],
            [
                InlineKeyboardButton(
                    t.meetings.edit_attendees_btn,
                    callback_data=f"meatt_{stored_user_id}_{meeting_idx}",
                ),
                InlineKeyboardButton(
                    t.meetings.edit_link_btn, callback_data=f"meli_{stored_user_id}_{meeting_idx}"
                ),
            ],
            [
                InlineKeyboardButton(
                    t.inline.back_button, callback_data=f"md_{stored_user_id}_{meeting_idx}"
                )
            ],
        ]

        await query.edit_message_text(
            text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="Markdown"
        )

    except Exception as e:
        logger.exception(f"Error in meeting_edit_menu_callback: {e}")
        await query.edit_message_text(f"Error: {str(e)}")


async def meeting_edit_time_callback(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show time selection grid."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    await query.answer()

    try:
        parts = query.data.split("_")
        stored_user_id = int(parts[1])
        meeting_idx = int(parts[2])

        if stored_user_id != update.effective_user.id:
            return

        async with async_session_factory() as session:
            user_service = UserService(session)
            user = await user_service.get_user(update.effective_user.id)
            t = get_text(user.language if user else "en")

        # Time grid
        times_morning = ["08:00", "09:00", "10:00", "11:00"]
        times_afternoon = ["12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]

        text = t.inline.select_time_title

        buttons = []
        # Morning row
        row = []
        for time in times_morning:
            row.append(
                InlineKeyboardButton(
                    time,
                    callback_data=f"mst_{stored_user_id}_{meeting_idx}_{time.replace(':', '')}",
                )
            )
        buttons.append(row)

        # Afternoon rows
        row = []
        for time in times_afternoon:
            row.append(
                InlineKeyboardButton(
                    time,
                    callback_data=f"mst_{stored_user_id}_{meeting_idx}_{time.replace(':', '')}",
                )
            )
            if len(row) == 4:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)

        # Custom + Back
        buttons.append(
            [
                InlineKeyboardButton(
                    t.inline.custom_time_button,
                    callback_data=f"mstc_{stored_user_id}_{meeting_idx}",
                ),
                InlineKeyboardButton(
                    t.inline.back_button, callback_data=f"me_{stored_user_id}_{meeting_idx}"
                ),
            ]
        )

        await query.edit_message_text(
            text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="Markdown"
        )

    except Exception as e:
        logger.exception(f"Error in meeting_edit_time_callback: {e}")
        await query.edit_message_text(f"Error: {str(e)}")


async def meeting_set_time_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle time selection from grid."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    await query.answer()

    try:
        parts = query.data.split("_")
        stored_user_id = int(parts[1])
        meeting_idx = int(parts[2])
        time_str = parts[3]  # e.g., "0900"

        if stored_user_id != update.effective_user.id:
            return

        hour = int(time_str[:2])
        minute = int(time_str[2:])

        meetings_key = f"meetings_{stored_user_id}"
        if not context.bot_data or meetings_key not in context.bot_data:
            return

        meetings = context.bot_data[meetings_key]
        m = meetings[meeting_idx]

        async with async_session_factory() as session:
            user_service = UserService(session)
            user = await user_service.get_user(update.effective_user.id)

            if not user:
                return

            t = get_text(user.language)

            # Calculate new times keeping the same duration
            old_start = m["start_time"]
            old_end = m["end_time"]
            duration = old_end - old_start

            new_start = old_start.replace(hour=hour, minute=minute)
            new_end = new_start + duration

            # Update meeting
            calendar_service = CalendarService(session)
            result = await calendar_service.update_meeting(
                user=user,
                event_id=m["id"],
                start_time=new_start,
                end_time=new_end,
            )
            await session.commit()

        if "error" in result:
            await query.edit_message_text(f"❌ {result['error']}")
            return

        # Update local cache
        m["start_time"] = new_start
        m["end_time"] = new_end

        await query.edit_message_text(
            t.meetings.field_updated.format(field=t.meetings.edit_time_btn),
            parse_mode="Markdown",
        )

        # Return to detail view after short delay
        await meeting_detail_callback(update, context)

    except Exception as e:
        logger.exception(f"Error in meeting_set_time_callback: {e}")
        await query.edit_message_text(f"Error: {str(e)}")


async def meeting_edit_date_callback(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show date selection grid."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    await query.answer()

    try:
        parts = query.data.split("_")
        stored_user_id = int(parts[1])
        meeting_idx = int(parts[2])

        if stored_user_id != update.effective_user.id:
            return

        async with async_session_factory() as session:
            user_service = UserService(session)
            user = await user_service.get_user(update.effective_user.id)
            t = get_text(user.language if user else "en")
            user_tz = TimezoneHelper.get_timezone(user.timezone if user else "UTC")

        text = t.inline.select_date_title

        # Date options relative to today
        today = datetime.now(user_tz).date()
        dates = [
            (t.inline.date_today, today),
            (t.inline.date_tomorrow, today + timedelta(days=1)),
            (t.inline.date_day_after, today + timedelta(days=2)),
            (t.inline.date_in_3_days, today + timedelta(days=3)),
            (t.inline.date_in_a_week, today + timedelta(days=7)),
        ]

        buttons = []
        for label, date in dates:
            date_str = date.strftime("%Y%m%d")
            buttons.append(
                [
                    InlineKeyboardButton(
                        f"{label} ({date.strftime('%d %b')})",
                        callback_data=f"msd_{stored_user_id}_{meeting_idx}_{date_str}",
                    )
                ]
            )

        buttons.append(
            [
                InlineKeyboardButton(
                    t.inline.custom_date_button,
                    callback_data=f"msdc_{stored_user_id}_{meeting_idx}",
                ),
                InlineKeyboardButton(
                    t.inline.back_button, callback_data=f"me_{stored_user_id}_{meeting_idx}"
                ),
            ]
        )

        await query.edit_message_text(
            text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="Markdown"
        )

    except Exception as e:
        logger.exception(f"Error in meeting_edit_date_callback: {e}")
        await query.edit_message_text(f"Error: {str(e)}")


async def meeting_set_date_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle date selection from grid."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    await query.answer()

    try:
        parts = query.data.split("_")
        stored_user_id = int(parts[1])
        meeting_idx = int(parts[2])
        date_str = parts[3]  # e.g., "20260120"

        if stored_user_id != update.effective_user.id:
            return

        year = int(date_str[:4])
        month = int(date_str[4:6])
        day = int(date_str[6:])

        meetings_key = f"meetings_{stored_user_id}"
        if not context.bot_data or meetings_key not in context.bot_data:
            return

        meetings = context.bot_data[meetings_key]
        m = meetings[meeting_idx]

        async with async_session_factory() as session:
            user_service = UserService(session)
            user = await user_service.get_user(update.effective_user.id)

            if not user:
                return

            t = get_text(user.language)

            # Keep the same time, change the date
            old_start = m["start_time"]
            old_end = m["end_time"]
            duration = old_end - old_start

            new_start = old_start.replace(year=year, month=month, day=day)
            new_end = new_start + duration

            # Update meeting
            calendar_service = CalendarService(session)
            result = await calendar_service.update_meeting(
                user=user,
                event_id=m["id"],
                start_time=new_start,
                end_time=new_end,
            )
            await session.commit()

        if "error" in result:
            await query.edit_message_text(f"❌ {result['error']}")
            return

        # Update local cache
        m["start_time"] = new_start
        m["end_time"] = new_end

        await query.edit_message_text(
            t.meetings.field_updated.format(field=t.meetings.edit_date_btn),
            parse_mode="Markdown",
        )

        # Show detail view
        # Recreate callback_data for detail view
        query.data = f"md_{stored_user_id}_{meeting_idx}"
        await meeting_detail_callback(update, context)

    except Exception as e:
        logger.exception(f"Error in meeting_set_date_callback: {e}")
        await query.edit_message_text(f"Error: {str(e)}")


async def meeting_edit_duration_callback(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Show duration selection grid."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    await query.answer()

    try:
        parts = query.data.split("_")
        stored_user_id = int(parts[1])
        meeting_idx = int(parts[2])

        if stored_user_id != update.effective_user.id:
            return

        async with async_session_factory() as session:
            user_service = UserService(session)
            user = await user_service.get_user(update.effective_user.id)
            t = get_text(user.language if user else "en")

        text = t.inline.select_duration

        durations = [
            (t.inline.duration_15_min, 15),
            (t.inline.duration_30_min, 30),
            (t.inline.duration_45_min, 45),
            (t.inline.duration_1_hour, 60),
            (t.inline.duration_1_5_hours, 90),
            (t.inline.duration_2_hours, 120),
        ]

        buttons = []
        row = []
        for label, mins in durations:
            row.append(
                InlineKeyboardButton(
                    label, callback_data=f"msdu_{stored_user_id}_{meeting_idx}_{mins}"
                )
            )
            if len(row) == 3:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)

        buttons.append(
            [
                InlineKeyboardButton(
                    t.inline.back_button, callback_data=f"me_{stored_user_id}_{meeting_idx}"
                )
            ]
        )

        await query.edit_message_text(
            text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="Markdown"
        )

    except Exception as e:
        logger.exception(f"Error in meeting_edit_duration_callback: {e}")
        await query.edit_message_text(f"Error: {str(e)}")


async def meeting_set_duration_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle duration selection."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    await query.answer()

    try:
        parts = query.data.split("_")
        stored_user_id = int(parts[1])
        meeting_idx = int(parts[2])
        duration_mins = int(parts[3])

        if stored_user_id != update.effective_user.id:
            return

        meetings_key = f"meetings_{stored_user_id}"
        if not context.bot_data or meetings_key not in context.bot_data:
            return

        meetings = context.bot_data[meetings_key]
        m = meetings[meeting_idx]

        async with async_session_factory() as session:
            user_service = UserService(session)
            user = await user_service.get_user(update.effective_user.id)

            if not user:
                return

            t = get_text(user.language)

            # Keep start time, change end time
            new_end = m["start_time"] + timedelta(minutes=duration_mins)

            # Update meeting
            calendar_service = CalendarService(session)
            result = await calendar_service.update_meeting(
                user=user,
                event_id=m["id"],
                end_time=new_end,
            )
            await session.commit()

        if "error" in result:
            await query.edit_message_text(f"❌ {result['error']}")
            return

        # Update local cache
        m["end_time"] = new_end

        await query.edit_message_text(
            t.meetings.field_updated.format(field=t.meetings.edit_duration_btn),
            parse_mode="Markdown",
        )

        # Show detail view
        query.data = f"md_{stored_user_id}_{meeting_idx}"
        await meeting_detail_callback(update, context)

    except Exception as e:
        logger.exception(f"Error in meeting_set_duration_callback: {e}")
        await query.edit_message_text(f"Error: {str(e)}")


async def meeting_edit_title_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Redirect to private chat for title editing."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    await query.answer()

    try:
        parts = query.data.split("_")
        stored_user_id = int(parts[1])
        meeting_idx = int(parts[2])

        if stored_user_id != update.effective_user.id:
            return

        meetings_key = f"meetings_{stored_user_id}"
        if not context.bot_data or meetings_key not in context.bot_data:
            return

        meetings = context.bot_data[meetings_key]
        m = meetings[meeting_idx]

        async with async_session_factory() as session:
            user_service = UserService(session)
            user = await user_service.get_user(update.effective_user.id)
            t = get_text(user.language if user else "en")

        # Create edit session
        session_id = secrets.token_urlsafe(8)
        if context.bot_data is None:
            context.bot_data = {}

        context.bot_data[f"edit_meeting_{session_id}"] = {
            "user_id": stored_user_id,
            "meeting_idx": meeting_idx,
            "event_id": m["id"],
            "field": "title",
            "current": m["title"],
        }

        # Deep link to private chat
        bot = await context.bot.get_me()
        deep_link = f"https://t.me/{bot.username}?start=medit_{session_id}"

        keyboard = [
            [InlineKeyboardButton(t.inline.open_private_chat, url=deep_link)],
            [
                InlineKeyboardButton(
                    t.inline.back_button, callback_data=f"me_{stored_user_id}_{meeting_idx}"
                )
            ],
        ]

        await query.edit_message_text(
            f"{t.inline.continue_in_private}\n\n📝 {t.meetings.edit_title_btn}",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    except Exception as e:
        logger.exception(f"Error in meeting_edit_title_callback: {e}")
        await query.edit_message_text(f"Error: {str(e)}")


async def meeting_edit_attendees_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Redirect to private chat for attendees editing."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    await query.answer()

    try:
        parts = query.data.split("_")
        stored_user_id = int(parts[1])
        meeting_idx = int(parts[2])

        if stored_user_id != update.effective_user.id:
            return

        meetings_key = f"meetings_{stored_user_id}"
        if not context.bot_data or meetings_key not in context.bot_data:
            return

        meetings = context.bot_data[meetings_key]
        m = meetings[meeting_idx]

        async with async_session_factory() as session:
            user_service = UserService(session)
            user = await user_service.get_user(update.effective_user.id)
            t = get_text(user.language if user else "en")

        # Create edit session
        session_id = secrets.token_urlsafe(8)
        if context.bot_data is None:
            context.bot_data = {}

        context.bot_data[f"edit_meeting_{session_id}"] = {
            "user_id": stored_user_id,
            "meeting_idx": meeting_idx,
            "event_id": m["id"],
            "field": "attendees",
            "current": m.get("attendees", []),
        }

        # Deep link to private chat
        bot = await context.bot.get_me()
        deep_link = f"https://t.me/{bot.username}?start=medit_{session_id}"

        keyboard = [
            [InlineKeyboardButton(t.inline.open_private_chat, url=deep_link)],
            [
                InlineKeyboardButton(
                    t.inline.back_button, callback_data=f"me_{stored_user_id}_{meeting_idx}"
                )
            ],
        ]

        await query.edit_message_text(
            f"{t.inline.continue_in_private}\n\n👥 {t.meetings.edit_attendees_btn}",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    except Exception as e:
        logger.exception(f"Error in meeting_edit_attendees_callback: {e}")
        await query.edit_message_text(f"Error: {str(e)}")


async def meeting_edit_link_callback(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show link editing options."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    await query.answer()

    try:
        parts = query.data.split("_")
        stored_user_id = int(parts[1])
        meeting_idx = int(parts[2])

        if stored_user_id != update.effective_user.id:
            return

        async with async_session_factory() as session:
            user_service = UserService(session)
            user = await user_service.get_user(update.effective_user.id)
            t = get_text(user.language if user else "en")

            # Check if Zoom is connected
            from calendarbot.db.repository import OAuthTokenRepository

            token_repo = OAuthTokenRepository(session)
            zoom_connected = (
                await token_repo.get_token(user.id, "zoom") is not None if user else False
            )

        text = t.inline.add_link_title

        buttons = [
            [
                InlineKeyboardButton(
                    t.inline.auto_google_meet, callback_data=f"mslm_{stored_user_id}_{meeting_idx}"
                )
            ],
        ]

        if zoom_connected:
            buttons.append(
                [
                    InlineKeyboardButton(
                        t.inline.auto_zoom_meeting,
                        callback_data=f"mslz_{stored_user_id}_{meeting_idx}",
                    )
                ]
            )

        buttons.append(
            [
                InlineKeyboardButton(
                    t.inline.paste_custom_link, callback_data=f"mslc_{stored_user_id}_{meeting_idx}"
                )
            ]
        )
        buttons.append(
            [
                InlineKeyboardButton(
                    t.inline.back_button, callback_data=f"me_{stored_user_id}_{meeting_idx}"
                )
            ]
        )

        await query.edit_message_text(
            text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="Markdown"
        )

    except Exception as e:
        logger.exception(f"Error in meeting_edit_link_callback: {e}")
        await query.edit_message_text(f"Error: {str(e)}")


async def meeting_set_link_meet_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Add Google Meet link to meeting."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    await query.answer()

    try:
        parts = query.data.split("_")
        stored_user_id = int(parts[1])
        meeting_idx = int(parts[2])

        if stored_user_id != update.effective_user.id:
            return

        meetings_key = f"meetings_{stored_user_id}"
        if not context.bot_data or meetings_key not in context.bot_data:
            return

        meetings = context.bot_data[meetings_key]
        m = meetings[meeting_idx]

        async with async_session_factory() as session:
            user_service = UserService(session)
            user = await user_service.get_user(update.effective_user.id)

            if not user:
                return

            t = get_text(user.language)

            # Update meeting with Meet link
            calendar_service = CalendarService(session)
            result = await calendar_service.update_meeting(
                user=user,
                event_id=m["id"],
                generate_meet_link=True,
            )
            await session.commit()

        if "error" in result:
            await query.edit_message_text(f"❌ {result['error']}")
            return

        await query.edit_message_text(t.inline.link_added, parse_mode="Markdown")

        # Show detail view
        query.data = f"md_{stored_user_id}_{meeting_idx}"
        await meeting_detail_callback(update, context)

    except Exception as e:
        logger.exception(f"Error in meeting_set_link_meet_callback: {e}")
        await query.edit_message_text(f"Error: {str(e)}")


async def meeting_cancel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle cancel meeting from detail view."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    try:
        parts = query.data.split("_")
        stored_user_id = int(parts[1])
        meeting_idx = int(parts[2])

        if stored_user_id != update.effective_user.id:
            return

        meetings_key = f"meetings_{stored_user_id}"
        if not context.bot_data or meetings_key not in context.bot_data:
            async with async_session_factory() as session:
                user_service = UserService(session)
                user = await user_service.get_user(update.effective_user.id)
                t = get_text(user.language if user else "en")
            await query.answer(t.meetings.session_expired, show_alert=True)
            return

        meetings = context.bot_data[meetings_key]
        if meeting_idx >= len(meetings):
            return

        m = meetings[meeting_idx]

        async with async_session_factory() as session:
            user_service = UserService(session)
            user = await user_service.get_user(update.effective_user.id)
            t = get_text(user.language if user else "en")

        await query.answer(t.meetings.cancelling_meeting)

        async with async_session_factory() as session:
            user_service = UserService(session)
            user = await user_service.get_user(update.effective_user.id)

            if not user:
                return

            calendar_service = CalendarService(session)
            result = await calendar_service.cancel_meeting(user, m["id"])
            await session.commit()

        if "error" in result:
            await query.edit_message_text(f"❌ Error: {result['error']}")
        else:
            # Remove from local cache
            meetings.pop(meeting_idx)
            await query.edit_message_text(
                f"{t.meetings.meeting_cancelled.format(title=result['title'])}\n\n{t.meetings.attendees_notified}",
                parse_mode="Markdown",
            )

    except Exception as e:
        logger.exception(f"Error in meeting_cancel_callback: {e}")
        await query.edit_message_text(f"Error: {str(e)}")


async def meetings_close_callback(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle close button."""
    query = update.callback_query
    if not query:
        return

    await query.answer()

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = (
            await user_service.get_user(update.effective_user.id) if update.effective_user else None
        )
        t = get_text(user.language if user else "en")

    await query.edit_message_text(t.meetings.closed)


# Keep /cancel command for backwards compatibility
async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /cancel command - redirect to /meetings."""
    await meetings_command(update, context)


def setup_meeting_handlers(app: Application) -> None:
    """Register meeting handlers."""
    app.add_handler(CommandHandler("meetings", meetings_command))
    app.add_handler(CommandHandler("cancel", cancel_command))

    # Meetings list pagination: ml_{user_id}_{page}
    app.add_handler(CallbackQueryHandler(meetings_page_callback, pattern=r"^ml_\d+_\d+$"))

    # Meeting detail: md_{user_id}_{index}
    app.add_handler(CallbackQueryHandler(meeting_detail_callback, pattern=r"^md_\d+_\d+$"))

    # Meeting edit menu: me_{user_id}_{index}
    app.add_handler(CallbackQueryHandler(meeting_edit_menu_callback, pattern=r"^me_\d+_\d+$"))

    # Edit fields
    app.add_handler(CallbackQueryHandler(meeting_edit_title_callback, pattern=r"^met_\d+_\d+$"))
    app.add_handler(CallbackQueryHandler(meeting_edit_time_callback, pattern=r"^meti_\d+_\d+$"))
    app.add_handler(CallbackQueryHandler(meeting_edit_date_callback, pattern=r"^meda_\d+_\d+$"))
    app.add_handler(CallbackQueryHandler(meeting_edit_duration_callback, pattern=r"^medu_\d+_\d+$"))
    app.add_handler(
        CallbackQueryHandler(meeting_edit_attendees_callback, pattern=r"^meatt_\d+_\d+$")
    )
    app.add_handler(CallbackQueryHandler(meeting_edit_link_callback, pattern=r"^meli_\d+_\d+$"))

    # Set field values
    app.add_handler(CallbackQueryHandler(meeting_set_time_callback, pattern=r"^mst_\d+_\d+_\d+$"))
    app.add_handler(CallbackQueryHandler(meeting_set_date_callback, pattern=r"^msd_\d+_\d+_\d+$"))
    app.add_handler(
        CallbackQueryHandler(meeting_set_duration_callback, pattern=r"^msdu_\d+_\d+_\d+$")
    )

    # Link options
    app.add_handler(CallbackQueryHandler(meeting_set_link_meet_callback, pattern=r"^mslm_\d+_\d+$"))

    # Cancel meeting: mc_{user_id}_{index}
    app.add_handler(CallbackQueryHandler(meeting_cancel_callback, pattern=r"^mc_\d+_\d+$"))

    # Close
    app.add_handler(CallbackQueryHandler(meetings_close_callback, pattern=r"^meetings_close$"))
