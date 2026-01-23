"""Inline query handler for meeting creation with edit menu."""

import contextlib
import logging
import re
import uuid
from datetime import datetime, timedelta
from urllib.parse import quote

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
    ContextTypes,
    InlineQueryHandler,
    MessageHandler,
    filters,
)

from calendarbot.db.repository import PendingInviteRepository, RecentContactRepository
from calendarbot.db.session import async_session_factory
from calendarbot.i18n import get_text
from calendarbot.services.calendar import CalendarService
from calendarbot.services.parser import MeetingParser
from calendarbot.services.user import UserService
from calendarbot.services.username_resolver import UsernameResolverService
from calendarbot.utils.timezone import TimezoneHelper

logger = logging.getLogger(__name__)

# Duration options in minutes
DURATION_OPTIONS = [15, 30, 45, 60, 90, 120]
# Reminder options in minutes (0 = none, 1440 = 1 day)
REMINDER_OPTIONS = [0, 5, 10, 15, 30, 60, 1440]


def _escape_markdown(text: str) -> str:
    """Escape special Markdown characters in text."""
    special_chars = ["_", "*", "`", "["]
    for char in special_chars:
        text = text.replace(char, f"\\{char}")
    return text


def _format_reminders(reminders: list[int], t) -> str:
    """Format reminder list for display."""
    parts = []
    for m in reminders:
        if m >= 1440:
            days = m // 1440
            if days > 1:
                parts.append(f"{days} {t.settings.days}")
            else:
                parts.append(f"{days} {t.settings.day}")
        elif m >= 60:
            hours = m // 60
            if hours > 1:
                parts.append(f"{hours} {t.settings.hours}")
            else:
                parts.append(f"{hours} {t.settings.hour}")
        else:
            parts.append(f"{m} {t.settings.minutes}")
    return ", ".join(parts)


def _format_duration(minutes: int, t) -> str:
    """Format duration for display."""
    duration_map = {
        15: t.inline.duration_15_min,
        30: t.inline.duration_30_min,
        45: t.inline.duration_45_min,
        60: t.inline.duration_1_hour,
        90: t.inline.duration_1_5_hours,
        120: t.inline.duration_2_hours,
    }
    return duration_map.get(minutes, f"{minutes} min")


def _format_reminder_option(minutes: int, t) -> str:
    """Format reminder option for button."""
    reminder_map = {
        0: t.inline.reminder_none,
        5: t.inline.reminder_5_min,
        10: t.inline.reminder_10_min,
        15: t.inline.reminder_15_min,
        30: t.inline.reminder_30_min,
        60: t.inline.reminder_1_hour,
        1440: t.inline.reminder_1_day,
    }
    return reminder_map.get(minutes, f"{minutes} min")


def build_add_to_calendar_url(
    title: str,
    start: datetime,
    end: datetime,
    timezone: str,
    details: str | None = None,
) -> str:
    """Build a universal Google Calendar 'Add to Calendar' URL."""
    start_utc = TimezoneHelper.to_utc(start, timezone)
    end_utc = TimezoneHelper.to_utc(end, timezone)
    start_str = start_utc.strftime("%Y%m%dT%H%M%SZ")
    end_str = end_utc.strftime("%Y%m%dT%H%M%SZ")
    params = {
        "action": "TEMPLATE",
        "text": title,
        "dates": f"{start_str}/{end_str}",
    }
    if details:
        params["details"] = details
    query = "&".join(f"{k}={quote(str(v))}" for k, v in params.items())
    return f"https://calendar.google.com/calendar/render?{query}"


def _build_preview_keyboard(result_id: str, t) -> InlineKeyboardMarkup:
    """Build the initial preview keyboard with Create, Edit, Cancel buttons."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"✅ {t.inline.create_meeting_button}", callback_data=f"create_{result_id}"
                ),
                InlineKeyboardButton(
                    f"✏️ {t.inline.edit_button}", callback_data=f"edit_{result_id}"
                ),
                InlineKeyboardButton(
                    f"❌ {t.inline.cancel_button}", callback_data=f"discard_{result_id}"
                ),
            ]
        ]
    )


def _build_edit_menu_keyboard(result_id: str, meeting_data: dict, t) -> InlineKeyboardMarkup:
    """Build the edit menu keyboard."""
    m = meeting_data["meeting"]
    attendee_count = len(m.get("attendees", [])) + len(m.get("usernames", []))
    has_link = (
        m.get("meet_link") or m.get("teams_link") or m.get("zoom_link") or m.get("custom_link")
    )

    # Build link button text
    link_text = t.inline.edit_link_button
    if has_link:
        link_text = "🔗 ✓"

    buttons = [
        [
            InlineKeyboardButton(t.inline.edit_title_button, callback_data=f"em_title_{result_id}"),
            InlineKeyboardButton(t.inline.edit_time_button, callback_data=f"em_time_{result_id}"),
            InlineKeyboardButton(t.inline.edit_date_button, callback_data=f"em_date_{result_id}"),
        ],
        [
            InlineKeyboardButton(
                t.inline.edit_duration_button, callback_data=f"em_dur_{result_id}"
            ),
            InlineKeyboardButton(
                t.inline.edit_reminder_button, callback_data=f"em_rem_{result_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                f"👥 ({attendee_count})" if attendee_count else t.inline.edit_attendees_button,
                callback_data=f"em_att_{result_id}",
            ),
            InlineKeyboardButton(link_text, callback_data=f"em_link_{result_id}"),
        ],
    ]

    # Add calendar selection button if both calendars are connected
    if meeting_data.get("has_both_calendars"):
        target = meeting_data.get("target_calendar", "google")
        cal_label = "📅 Google" if target == "google" else "📆 Outlook"
        buttons.append([InlineKeyboardButton(cal_label, callback_data=f"em_cal_{result_id}")])

    buttons.append(
        [InlineKeyboardButton(t.inline.back_button, callback_data=f"em_back_{result_id}")]
    )
    return InlineKeyboardMarkup(buttons)


def _build_duration_keyboard(result_id: str, t) -> InlineKeyboardMarkup:
    """Build duration selection keyboard."""
    buttons = [
        [
            InlineKeyboardButton(t.inline.duration_15_min, callback_data=f"dur_{result_id}_15"),
            InlineKeyboardButton(t.inline.duration_30_min, callback_data=f"dur_{result_id}_30"),
            InlineKeyboardButton(t.inline.duration_45_min, callback_data=f"dur_{result_id}_45"),
        ],
        [
            InlineKeyboardButton(t.inline.duration_1_hour, callback_data=f"dur_{result_id}_60"),
            InlineKeyboardButton(t.inline.duration_1_5_hours, callback_data=f"dur_{result_id}_90"),
            InlineKeyboardButton(t.inline.duration_2_hours, callback_data=f"dur_{result_id}_120"),
        ],
        [
            InlineKeyboardButton(t.inline.back_button, callback_data=f"edit_{result_id}"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)


def _build_reminder_keyboard(result_id: str, t) -> InlineKeyboardMarkup:
    """Build reminder selection keyboard."""
    buttons = [
        [
            InlineKeyboardButton(t.inline.reminder_none, callback_data=f"rem_{result_id}_0"),
            InlineKeyboardButton(t.inline.reminder_5_min, callback_data=f"rem_{result_id}_5"),
            InlineKeyboardButton(t.inline.reminder_10_min, callback_data=f"rem_{result_id}_10"),
        ],
        [
            InlineKeyboardButton(t.inline.reminder_15_min, callback_data=f"rem_{result_id}_15"),
            InlineKeyboardButton(t.inline.reminder_30_min, callback_data=f"rem_{result_id}_30"),
            InlineKeyboardButton(t.inline.reminder_1_hour, callback_data=f"rem_{result_id}_60"),
        ],
        [
            InlineKeyboardButton(t.inline.reminder_1_day, callback_data=f"rem_{result_id}_1440"),
            InlineKeyboardButton(t.inline.back_button, callback_data=f"edit_{result_id}"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)


def _build_attendees_keyboard(
    result_id: str, meeting_data: dict, recent_contacts: list, t
) -> InlineKeyboardMarkup:
    """Build attendees management keyboard."""
    m = meeting_data["meeting"]
    buttons = []

    # Current attendees with remove buttons
    for i, email in enumerate(m.get("attendees", [])):
        display = email[:20] + "..." if len(email) > 23 else email
        buttons.append(
            [
                InlineKeyboardButton(f"📧 {display}", callback_data="noop"),
                InlineKeyboardButton("🗑️", callback_data=f"att_rem_{result_id}_e{i}"),
            ]
        )

    for i, username in enumerate(m.get("usernames", [])):
        display = f"@{username}"[:20] + "..." if len(username) > 18 else f"@{username}"
        buttons.append(
            [
                InlineKeyboardButton(display, callback_data="noop"),
                InlineKeyboardButton("🗑️", callback_data=f"att_rem_{result_id}_u{i}"),
            ]
        )

    # Recent contacts (up to 3)
    if recent_contacts:
        rc_row = []
        for i, contact in enumerate(recent_contacts[:3]):
            display = contact.contact_identifier[:15]
            if contact.contact_type == "username":
                display = f"@{display}"
            rc_row.append(InlineKeyboardButton(display, callback_data=f"att_rc_{result_id}_{i}"))
        if rc_row:
            buttons.append(rc_row)

    # Add and Back buttons
    buttons.append(
        [
            InlineKeyboardButton(
                t.inline.type_manually_button, callback_data=f"att_add_{result_id}"
            ),
        ]
    )
    buttons.append(
        [
            InlineKeyboardButton(t.inline.back_button, callback_data=f"edit_{result_id}"),
        ]
    )

    return InlineKeyboardMarkup(buttons)


def _build_link_keyboard(
    result_id: str,
    meeting_data: dict,
    t,
    calendar_provider: str | None = None,
    zoom_connected: bool = False,
) -> InlineKeyboardMarkup:
    """Build link management keyboard.

    Args:
        result_id: The meeting result ID
        meeting_data: The meeting data dictionary
        t: Translation object
        calendar_provider: 'google', 'outlook', or None
        zoom_connected: Whether Zoom is connected
    """
    m = meeting_data["meeting"]
    has_link = (
        m.get("meet_link") or m.get("teams_link") or m.get("zoom_link") or m.get("custom_link")
    )

    buttons = []
    if has_link:
        # Show remove option - determine which link type to display
        if m.get("meet_link"):
            link_display = m.get("meet_link") if m.get("meet_link") != "pending" else "Google Meet"
        elif m.get("teams_link"):
            link_display = (
                m.get("teams_link") if m.get("teams_link") != "pending" else "Microsoft Teams"
            )
        elif m.get("zoom_link"):
            link_display = m.get("zoom_link") if m.get("zoom_link") != "pending" else "Zoom Meeting"
        else:
            link_display = m.get("custom_link", "")
        short_link = link_display[:30] + "..." if len(link_display) > 33 else link_display
        buttons.append([InlineKeyboardButton(f"🔗 {short_link}", callback_data="noop")])
        buttons.append(
            [
                InlineKeyboardButton(
                    t.inline.remove_link_button, callback_data=f"link_rem_{result_id}"
                )
            ]
        )
    else:
        # Show add options based on calendar provider
        if calendar_provider == "google":
            buttons.append(
                [
                    InlineKeyboardButton(
                        t.inline.auto_google_meet, callback_data=f"link_meet_{result_id}"
                    )
                ]
            )
        elif calendar_provider == "outlook":
            buttons.append(
                [
                    InlineKeyboardButton(
                        t.inline.auto_teams_meeting, callback_data=f"link_teams_{result_id}"
                    )
                ]
            )
        else:
            # No calendar connected or unknown provider - show Google Meet as default
            buttons.append(
                [
                    InlineKeyboardButton(
                        t.inline.auto_google_meet, callback_data=f"link_meet_{result_id}"
                    )
                ]
            )

        # Show Zoom option if connected
        if zoom_connected:
            buttons.append(
                [
                    InlineKeyboardButton(
                        t.inline.auto_zoom_meeting, callback_data=f"link_zoom_{result_id}"
                    )
                ]
            )

        buttons.append(
            [
                InlineKeyboardButton(
                    t.inline.paste_custom_link, callback_data=f"link_custom_{result_id}"
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(t.inline.back_button, callback_data=f"edit_{result_id}"),
        ]
    )

    return InlineKeyboardMarkup(buttons)


def _build_meeting_preview_text(meeting_data: dict, t, _user_timezone: str) -> str:
    """Build the meeting preview text from meeting data."""
    m = meeting_data["meeting"]

    start_dt = datetime.fromisoformat(m["start_datetime"])
    end_dt = datetime.fromisoformat(m["end_datetime"])

    # Calculate duration in minutes
    duration = int((end_dt - start_dt).total_seconds() / 60)

    text = f"📅 *{_escape_markdown(m['title'])}*\n"
    text += f"🕐 {m['time']}"
    if m.get("date"):
        text += f", {m['date']}"
    text += "\n"
    text += f"⏱️ {_format_duration(duration, t)}\n"

    # Attendees
    attendees = m.get("attendees", [])
    usernames = m.get("usernames", [])
    if attendees or usernames:
        all_att = attendees + [f"@{_escape_markdown(u)}" for u in usernames]
        text += f"👥 {len(all_att)}: {', '.join(all_att[:3])}"
        if len(all_att) > 3:
            text += f" +{len(all_att) - 3}"
        text += "\n"

    # Reminder
    reminders = m.get("reminders")
    if reminders:
        text += f"🔔 {_format_reminders(reminders, t)}\n"
    elif m.get("use_default_reminder"):
        text += "🔔 (default)\n"

    # Link
    if m.get("meet_link"):
        text += "🎥 Google Meet\n"
    elif m.get("teams_link"):
        text += "📹 Microsoft Teams\n"
    elif m.get("zoom_link"):
        text += "📹 Zoom Meeting\n"
    elif m.get("custom_link"):
        text += "🔗 Custom link\n"

    return text


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline queries - parse meeting command and show preview."""
    query = update.inline_query
    if not query or not query.from_user:
        return

    text = query.query.strip()

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(query.from_user.id)

        if not user:
            t = get_text("en")
            results = [
                InlineQueryResultArticle(
                    id="not_registered",
                    title=t.inline.please_start_first_title,
                    description=t.inline.please_start_first_description,
                    input_message_content=InputTextMessageContent(
                        t.inline.please_start_first_message
                    ),
                )
            ]
            await query.answer(results, cache_time=60)
            return

        t = get_text(user.language)

        if not text:
            results = [
                InlineQueryResultArticle(
                    id="help",
                    title=t.inline.how_to_create,
                    description=t.inline.inline_help_description,
                    input_message_content=InputTextMessageContent(t.inline.inline_help_message),
                )
            ]
            await query.answer(results, cache_time=300)
            return

        calendar_connected = await user_service.is_calendar_connected(user)
        google_connected = await user_service.is_calendar_connected(user, "google")
        outlook_connected = await user_service.is_outlook_connected(user)
        has_both_calendars = google_connected and outlook_connected
        default_calendar = user.default_calendar or ("google" if google_connected else "outlook")
        user_timezone = user.timezone
        user_default_duration = user.default_duration
        user_default_reminder = user.default_reminder
        user_telegram_id = query.from_user.id

    parser = MeetingParser(
        user_timezone=user_timezone,
        default_duration=user_default_duration,
    )
    meeting = parser.parse(text)

    if not meeting:
        results = [
            InlineQueryResultArticle(
                id="parse_error",
                title=t.inline.could_not_parse,
                description=t.inline.parse_error_description,
                input_message_content=InputTextMessageContent(t.inline.parse_error_message),
            )
        ]
        await query.answer(results, cache_time=10)
        return

    # Resolve usernames if present
    username_statuses: dict[str, str] = {}
    rate_limited = False
    if meeting.usernames:
        async with async_session_factory() as session:
            resolver = UsernameResolverService(session)
            remaining = await resolver.get_remaining_lookups(user_telegram_id)
            if remaining < len(meeting.usernames):
                rate_limited = True
            else:
                username_statuses = await resolver.get_username_statuses(
                    meeting.usernames, user_telegram_id
                )

    preview = parser.format_preview(
        meeting,
        default_reminder=user_default_reminder,
        username_statuses=username_statuses if not rate_limited else None,
    )

    if rate_limited:
        preview += f"\n\n{t.inline.rate_limit_warning}"

    if not calendar_connected:
        preview += f"\n\n{t.inline.calendar_not_connected_warning}"

    result_id = str(uuid.uuid4())

    # Calculate duration from start/end times
    duration = int((meeting.end_datetime - meeting.start_datetime).total_seconds() / 60)

    if context.bot_data is None:
        context.bot_data = {}
    context.bot_data[f"meeting_{result_id}"] = {
        "user_id": query.from_user.id,
        "state": "preview",
        "original_query": text,
        "has_both_calendars": has_both_calendars,
        "target_calendar": default_calendar,  # Which calendar to create in
        "meeting": {
            "time": meeting.time,
            "date": meeting.date,
            "title": meeting.title,
            "attendees": meeting.attendees,
            "usernames": meeting.usernames,
            "start_datetime": meeting.start_datetime.isoformat(),
            "end_datetime": meeting.end_datetime.isoformat(),
            "reminders": meeting.reminders,
            "use_default_reminder": meeting.use_default_reminder,
            "duration": duration,
            "meet_link": None,
            "teams_link": None,
            "zoom_link": None,
            "custom_link": None,
        },
    }

    keyboard = _build_preview_keyboard(result_id, t)

    date_display = meeting.date or t.inline.today
    total_attendees = len(meeting.attendees) + len(meeting.usernames)

    results = [
        InlineQueryResultArticle(
            id=result_id,
            title=f"📅 {meeting.title}",
            description=f"{meeting.time} {date_display} - {t.inline.attendees_label.format(count=total_attendees)}",
            input_message_content=InputTextMessageContent(
                preview,
                parse_mode=None,
            ),
            reply_markup=keyboard,
        )
    ]

    await query.answer(results, cache_time=0, is_personal=True)


async def edit_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show the edit menu."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    result_id = query.data.replace("edit_", "")

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

    if meeting_data["user_id"] != update.effective_user.id:
        await query.answer(t.inline.not_your_meeting, show_alert=True)
        return

    await query.answer()

    meeting_data["state"] = "edit_menu"
    keyboard = _build_edit_menu_keyboard(result_id, meeting_data, t)

    await query.edit_message_text(
        t.inline.edit_menu_title, parse_mode="Markdown", reply_markup=keyboard
    )


async def back_to_preview_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Return to the meeting preview."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    result_id = query.data.replace("em_back_", "")

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")
        user_timezone = user.timezone if user else "UTC"

    if context.bot_data is None:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    meeting_data = context.bot_data.get(f"meeting_{result_id}")
    if not meeting_data:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    await query.answer()

    meeting_data["state"] = "preview"

    # Rebuild preview text
    preview = _build_meeting_preview_text(meeting_data, t, user_timezone)
    keyboard = _build_preview_keyboard(result_id, t)

    await query.edit_message_text(preview, parse_mode="Markdown", reply_markup=keyboard)


async def edit_duration_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show duration selection."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    result_id = query.data.replace("em_dur_", "")

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

    keyboard = _build_duration_keyboard(result_id, t)
    await query.edit_message_text(
        t.inline.select_duration, parse_mode="Markdown", reply_markup=keyboard
    )


async def set_duration_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set meeting duration."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    # Parse dur_{id}_{minutes}
    parts = query.data.split("_")
    if len(parts) != 3:
        return

    result_id = parts[1]
    duration = int(parts[2])

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

    # Update duration and end time
    m = meeting_data["meeting"]
    start_dt = datetime.fromisoformat(m["start_datetime"])
    end_dt = start_dt + timedelta(minutes=duration)
    m["duration"] = duration
    m["end_datetime"] = end_dt.isoformat()

    await query.answer(t.inline.field_updated.format(field="Duration"))

    # Return to edit menu
    keyboard = _build_edit_menu_keyboard(result_id, meeting_data, t)
    await query.edit_message_text(
        t.inline.edit_menu_title, parse_mode="Markdown", reply_markup=keyboard
    )


async def edit_reminder_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show reminder selection."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    result_id = query.data.replace("em_rem_", "")

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

    keyboard = _build_reminder_keyboard(result_id, t)
    await query.edit_message_text(
        t.inline.select_reminder, parse_mode="Markdown", reply_markup=keyboard
    )


async def set_reminder_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set meeting reminder."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    # Parse rem_{id}_{minutes}
    parts = query.data.split("_")
    if len(parts) != 3:
        return

    result_id = parts[1]
    reminder_mins = int(parts[2])

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
    if reminder_mins == 0:
        m["reminders"] = None
        m["use_default_reminder"] = False
    else:
        m["reminders"] = [reminder_mins]
        m["use_default_reminder"] = False

    await query.answer(t.inline.field_updated.format(field="Reminder"))

    keyboard = _build_edit_menu_keyboard(result_id, meeting_data, t)
    await query.edit_message_text(
        t.inline.edit_menu_title, parse_mode="Markdown", reply_markup=keyboard
    )


async def edit_attendees_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show attendees management."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    result_id = query.data.replace("em_att_", "")

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

        # Get recent contacts
        recent_contacts = []
        if user:
            rc_repo = RecentContactRepository(session)
            recent_contacts = await rc_repo.get_recent_contacts(user.id, limit=3)

    if context.bot_data is None:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    meeting_data = context.bot_data.get(f"meeting_{result_id}")
    if not meeting_data:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    await query.answer()

    # Build attendees text
    m = meeting_data["meeting"]
    text = f"👥 *{t.inline.current_attendees.replace('*', '')}*\n\n"

    if not m.get("attendees") and not m.get("usernames"):
        text += "_None_\n"
    else:
        for email in m.get("attendees", []):
            text += f"• {email}\n"
        for username in m.get("usernames", []):
            text += f"• @{_escape_markdown(username)}\n"

    if recent_contacts:
        text += f"\n{t.inline.recent_contacts_title}\n"

    keyboard = _build_attendees_keyboard(result_id, meeting_data, recent_contacts, t)
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)


async def remove_attendee_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove an attendee."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    # Parse att_rem_{id}_{type}{index}
    match = re.match(r"att_rem_([^_]+)_([eu])(\d+)", query.data)
    if not match:
        return

    result_id = match.group(1)
    att_type = match.group(2)  # 'e' for email, 'u' for username
    index = int(match.group(3))

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

        recent_contacts = []
        if user:
            rc_repo = RecentContactRepository(session)
            recent_contacts = await rc_repo.get_recent_contacts(user.id, limit=3)

    if context.bot_data is None:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    meeting_data = context.bot_data.get(f"meeting_{result_id}")
    if not meeting_data:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    m = meeting_data["meeting"]
    removed = None

    if att_type == "e" and index < len(m.get("attendees", [])):
        removed = m["attendees"].pop(index)
    elif att_type == "u" and index < len(m.get("usernames", [])):
        removed = "@" + m["usernames"].pop(index)

    if removed:
        await query.answer(t.inline.attendee_removed.format(attendee=removed))
    else:
        await query.answer()

    # Refresh attendees view
    text = f"👥 *{t.inline.current_attendees.replace('*', '')}*\n\n"
    if not m.get("attendees") and not m.get("usernames"):
        text += "_None_\n"
    else:
        for email in m.get("attendees", []):
            text += f"• {email}\n"
        for username in m.get("usernames", []):
            text += f"• @{_escape_markdown(username)}\n"

    if recent_contacts:
        text += f"\n{t.inline.recent_contacts_title}\n"

    keyboard = _build_attendees_keyboard(result_id, meeting_data, recent_contacts, t)
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)


async def add_recent_contact_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a recent contact as attendee."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    # Parse att_rc_{id}_{index}
    parts = query.data.split("_")
    if len(parts) != 4:
        return

    result_id = parts[2]
    contact_index = int(parts[3])

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

        recent_contacts = []
        if user:
            rc_repo = RecentContactRepository(session)
            recent_contacts = await rc_repo.get_recent_contacts(user.id, limit=3)

    if context.bot_data is None:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    meeting_data = context.bot_data.get(f"meeting_{result_id}")
    if not meeting_data:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    if contact_index >= len(recent_contacts):
        await query.answer()
        return

    contact = recent_contacts[contact_index]
    m = meeting_data["meeting"]

    # Add contact
    if contact.contact_type == "email":
        if contact.contact_identifier not in m.get("attendees", []):
            if "attendees" not in m:
                m["attendees"] = []
            m["attendees"].append(contact.contact_identifier)
            await query.answer(t.inline.attendee_added.format(attendee=contact.contact_identifier))
        else:
            await query.answer("Already added")
    else:
        # Username
        username = contact.contact_identifier.lstrip("@")
        if username not in m.get("usernames", []):
            if "usernames" not in m:
                m["usernames"] = []
            m["usernames"].append(username)
            await query.answer(t.inline.attendee_added.format(attendee=f"@{username}"))
        else:
            await query.answer("Already added")

    # Refresh attendees view
    text = f"👥 *{t.inline.current_attendees.replace('*', '')}*\n\n"
    if not m.get("attendees") and not m.get("usernames"):
        text += "_None_\n"
    else:
        for email in m.get("attendees", []):
            text += f"• {email}\n"
        for username in m.get("usernames", []):
            text += f"• @{_escape_markdown(username)}\n"

    if recent_contacts:
        text += f"\n{t.inline.recent_contacts_title}\n"

    keyboard = _build_attendees_keyboard(result_id, meeting_data, recent_contacts, t)
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)


async def add_attendee_start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start adding an attendee manually."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    result_id = query.data.replace("att_add_", "")

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

    # Set state to waiting for attendee input
    meeting_data["state"] = "adding_attendee"

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(t.inline.cancel_edit_button, callback_data=f"em_att_{result_id}")]]
    )

    await query.edit_message_text(
        t.inline.add_attendee_prompt, parse_mode="Markdown", reply_markup=keyboard
    )


async def edit_calendar_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Toggle target calendar between Google and Outlook."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    result_id = query.data.replace("em_cal_", "")

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

    if meeting_data["user_id"] != update.effective_user.id:
        await query.answer(t.inline.not_your_meeting, show_alert=True)
        return

    # Toggle calendar
    current = meeting_data.get("target_calendar", "google")
    new_target = "outlook" if current == "google" else "google"
    meeting_data["target_calendar"] = new_target

    # Show which calendar is now selected
    cal_name = "Google Calendar" if new_target == "google" else "Outlook Calendar"
    await query.answer(f"📅 {cal_name}")

    # Update edit menu to show new calendar selection
    keyboard = _build_edit_menu_keyboard(result_id, meeting_data, t)
    await query.edit_message_text(
        t.inline.edit_menu_title, parse_mode="Markdown", reply_markup=keyboard
    )


async def edit_link_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show link management."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    result_id = query.data.replace("em_link_", "")

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

        # Get calendar provider and Zoom connection status
        calendar_provider = None
        zoom_connected = False
        if user:
            calendar_service = CalendarService(session)
            calendar_provider = await calendar_service.get_calendar_provider(user)
            zoom_connected = await user_service.is_zoom_connected(user)

    if context.bot_data is None:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    meeting_data = context.bot_data.get(f"meeting_{result_id}")
    if not meeting_data:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    await query.answer()

    keyboard = _build_link_keyboard(
        result_id,
        meeting_data,
        t,
        calendar_provider=calendar_provider,
        zoom_connected=zoom_connected,
    )
    await query.edit_message_text(
        t.inline.add_link_title, parse_mode="Markdown", reply_markup=keyboard
    )


async def add_google_meet_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Flag to generate Google Meet link on creation."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    result_id = query.data.replace("link_meet_", "")

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
    m["meet_link"] = "pending"  # Will be generated on create
    m["teams_link"] = None
    m["zoom_link"] = None
    m["custom_link"] = None

    await query.answer(t.inline.link_added)

    # Return to edit menu
    keyboard = _build_edit_menu_keyboard(result_id, meeting_data, t)
    await query.edit_message_text(
        t.inline.edit_menu_title, parse_mode="Markdown", reply_markup=keyboard
    )


async def add_zoom_link_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Flag to generate Zoom meeting link on creation."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    result_id = query.data.replace("link_zoom_", "")

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

        # Check if user has Zoom connected
        if user:
            zoom_connected = await user_service.is_zoom_connected(user)
            if not zoom_connected:
                await query.answer(t.inline.zoom_not_connected, show_alert=True)
                return

    if context.bot_data is None:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    meeting_data = context.bot_data.get(f"meeting_{result_id}")
    if not meeting_data:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    m = meeting_data["meeting"]
    m["zoom_link"] = "pending"  # Will be generated on create
    m["meet_link"] = None
    m["teams_link"] = None
    m["custom_link"] = None

    await query.answer(t.inline.link_added)

    # Return to edit menu
    keyboard = _build_edit_menu_keyboard(result_id, meeting_data, t)
    await query.edit_message_text(
        t.inline.edit_menu_title, parse_mode="Markdown", reply_markup=keyboard
    )


async def add_teams_link_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Flag to generate Microsoft Teams link on creation."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    result_id = query.data.replace("link_teams_", "")

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

        # Check if user has Outlook connected
        if user:
            outlook_connected = await user_service.is_outlook_connected(user)
            if not outlook_connected:
                await query.answer(t.inline.outlook_not_connected, show_alert=True)
                return

    if context.bot_data is None:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    meeting_data = context.bot_data.get(f"meeting_{result_id}")
    if not meeting_data:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    m = meeting_data["meeting"]
    m["teams_link"] = "pending"  # Will be generated on create
    m["meet_link"] = None
    m["zoom_link"] = None
    m["custom_link"] = None

    await query.answer(t.inline.link_added)

    # Return to edit menu
    keyboard = _build_edit_menu_keyboard(result_id, meeting_data, t)
    await query.edit_message_text(
        t.inline.edit_menu_title, parse_mode="Markdown", reply_markup=keyboard
    )


async def add_custom_link_start_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Start adding a custom link."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    result_id = query.data.replace("link_custom_", "")

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

    meeting_data["state"] = "adding_link"

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(t.inline.cancel_edit_button, callback_data=f"em_link_{result_id}")]]
    )

    await query.edit_message_text(
        t.inline.enter_link_prompt, parse_mode="Markdown", reply_markup=keyboard
    )


async def remove_link_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove meeting link."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    result_id = query.data.replace("link_rem_", "")

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

        # Get calendar provider and Zoom connection status
        calendar_provider = None
        zoom_connected = False
        if user:
            calendar_service = CalendarService(session)
            calendar_provider = await calendar_service.get_calendar_provider(user)
            zoom_connected = await user_service.is_zoom_connected(user)

    if context.bot_data is None:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    meeting_data = context.bot_data.get(f"meeting_{result_id}")
    if not meeting_data:
        await query.answer(t.inline.meeting_data_expired, show_alert=True)
        return

    m = meeting_data["meeting"]
    m["meet_link"] = None
    m["teams_link"] = None
    m["zoom_link"] = None
    m["custom_link"] = None

    await query.answer(t.inline.link_removed)

    keyboard = _build_link_keyboard(
        result_id,
        meeting_data,
        t,
        calendar_provider=calendar_provider,
        zoom_connected=zoom_connected,
    )
    await query.edit_message_text(
        t.inline.add_link_title, parse_mode="Markdown", reply_markup=keyboard
    )


async def edit_title_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start title editing (show prompt)."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    result_id = query.data.replace("em_title_", "")

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

    meeting_data["state"] = "editing_title"
    current_title = meeting_data["meeting"]["title"]

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(t.inline.cancel_edit_button, callback_data=f"edit_{result_id}")]]
    )

    await query.edit_message_text(
        t.inline.enter_new_title.format(current=current_title),
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


async def edit_time_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start time editing."""
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

    meeting_data["state"] = "editing_time"
    current_time = meeting_data["meeting"]["time"]

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(t.inline.cancel_edit_button, callback_data=f"edit_{result_id}")]]
    )

    await query.edit_message_text(
        t.inline.enter_new_time.format(current=current_time),
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


async def edit_date_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start date editing."""
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

    meeting_data["state"] = "editing_date"
    current_date = meeting_data["meeting"].get("date") or "today"

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(t.inline.cancel_edit_button, callback_data=f"edit_{result_id}")]]
    )

    await query.edit_message_text(
        t.inline.enter_new_date.format(current=current_date),
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


async def noop_callback(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle no-op callbacks (display-only buttons)."""
    query = update.callback_query
    if query:
        await query.answer()


async def create_meeting_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle Create Meeting button press."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

    await query.answer(t.inline.creating_meeting)

    result_id = query.data.replace("create_", "")

    try:
        if context.bot_data is None:
            await query.edit_message_text(t.inline.meeting_data_expired)
            return

        meeting_data = context.bot_data.get(f"meeting_{result_id}")
        if not meeting_data:
            await query.edit_message_text(t.inline.meeting_data_expired)
            return

        if meeting_data["user_id"] != update.effective_user.id:
            await query.answer(t.inline.not_your_meeting, show_alert=True)
            return

        async with async_session_factory() as session:
            user_service = UserService(session)
            user = await user_service.get_user(update.effective_user.id)

            if not user:
                await query.edit_message_text(t.common.please_start_first)
                return

            t = get_text(user.language)

            from calendarbot.services.parser import ParsedMeeting

            m = meeting_data["meeting"]
            usernames = m.get("usernames", [])

            from calendarbot.services.username_resolver import MeetingInviteResult

            resolve_result: MeetingInviteResult | None = None
            if usernames:
                resolver = UsernameResolverService(session)
                resolve_result = await resolver.get_emails_for_meeting(
                    usernames, update.effective_user.id
                )

            resolved_emails = resolve_result.emails if resolve_result else []
            all_attendees = m["attendees"] + resolved_emails
            logger.info(
                f"Creating meeting: usernames={usernames}, resolved_emails_count={len(resolved_emails)}, "
                f"direct_attendees={m['attendees']}, all_attendees_count={len(all_attendees)}"
            )

            parsed = ParsedMeeting(
                time=m["time"],
                date=m["date"],
                title=m["title"],
                attendees=all_attendees,
                usernames=[],
                start_datetime=datetime.fromisoformat(m["start_datetime"]),
                end_datetime=datetime.fromisoformat(m["end_datetime"]),
                reminders=m.get("reminders"),
                use_default_reminder=m.get("use_default_reminder", False),
            )

            # Determine if we need to generate Meet, Teams, or Zoom link
            generate_meet_link = m.get("meet_link") == "pending"
            generate_teams_link = m.get("teams_link") == "pending"
            generate_zoom_link = m.get("zoom_link") == "pending"
            custom_link = m.get("custom_link")

            # Use target calendar if both calendars are connected and user selected one
            target_calendar = meeting_data.get("target_calendar")

            calendar_service = CalendarService(session)
            result = await calendar_service.create_meeting(
                user,
                parsed,
                generate_meet_link=generate_meet_link,
                generate_zoom_link=generate_zoom_link,
                generate_teams_link=generate_teams_link,
                custom_link=custom_link,
                force_provider=target_calendar if meeting_data.get("has_both_calendars") else None,
            )

            # Save recent contacts
            if "event_id" in result:
                rc_repo = RecentContactRepository(session)
                for email in m["attendees"]:
                    await rc_repo.add_or_update_contact(user.id, email, "email")
                for username in usernames:
                    await rc_repo.add_or_update_contact(user.id, username, "username")

            pending_invites_created: list[str] = []
            not_found_usernames = resolve_result.not_found if resolve_result else []
            if not_found_usernames and "event_id" in result:
                pending_repo = PendingInviteRepository(session)
                for username in not_found_usernames:
                    await pending_repo.create(
                        inviter_telegram_id=update.effective_user.id,
                        invitee_username=username,
                        meeting_id=result["event_id"],
                        meeting_title=parsed.title,
                        meeting_time=parsed.start_datetime,
                    )
                    pending_invites_created.append(username)

            await session.commit()

        context.bot_data.pop(f"meeting_{result_id}", None)

        if "error" in result:
            await query.edit_message_text(f"❌ Error: {result['error']}")
        else:
            start_str = result["start"].strftime("%H:%M on %d %b %Y")
            safe_title = _escape_markdown(result["title"])
            text = f"✅ {t.inline.meeting_created}\n\n"
            text += f"*{safe_title}*\n"
            text += f"🕐 {start_str}\n"

            reminders = result.get("reminders")
            if reminders:
                reminder_text = _format_reminders(reminders, t)
                text += f"{t.inline.reminder_label.format(reminder=reminder_text)}\n"

            # Show Meet/Teams/Zoom link if generated
            if result.get("meet_link"):
                text += f"🎥 [Google Meet]({result['meet_link']})\n"
            elif result.get("teams_link"):
                text += f"📹 [Microsoft Teams]({result['teams_link']})\n"
            elif result.get("zoom_link"):
                text += f"📹 [Zoom Meeting]({result['zoom_link']})\n"
            elif result.get("custom_link"):
                text += f"🔗 {result['custom_link']}\n"

            invited_usernames = resolve_result.invited if resolve_result else []
            no_calendar_usernames = resolve_result.no_calendar if resolve_result else []
            privacy_disabled_usernames = resolve_result.privacy_disabled if resolve_result else []

            if result["attendees"] or invited_usernames:
                text += f"\n{t.inline.invitations_sent}\n"
                for username in invited_usernames:
                    safe_username = _escape_markdown(username)
                    text += f"  • @{safe_username} ✅\n"
                for email in m["attendees"]:
                    text += f"  • {email}\n"

            if no_calendar_usernames:
                text += f"\n{t.inline.no_calendar_users_note}\n"
                for username in no_calendar_usernames:
                    safe_username = _escape_markdown(username)
                    text += f"  • @{safe_username}\n"

            if privacy_disabled_usernames:
                text += f"\n{t.inline.privacy_disabled_users_note}\n"
                for username in privacy_disabled_usernames:
                    safe_username = _escape_markdown(username)
                    text += f"  • @{safe_username}\n"

            if pending_invites_created:
                bot_username = (await context.bot.get_me()).username
                text += f"\n{t.inline.pending_invites_note}\n"
                for username in pending_invites_created:
                    safe_username = _escape_markdown(username)
                    text += f"  • @{safe_username}\n"
                register_url = f"https://t.me/{bot_username}?start=invite"
                text += f"\n👆 {t.inline.register_link_text}: {register_url}\n"

            # Determine meeting link to include in calendar event details
            meeting_link = (
                result.get("zoom_link") or result.get("meet_link") or result.get("custom_link")
            )
            add_to_cal_url = build_add_to_calendar_url(
                title=result["title"],
                start=result["start"],
                end=result["end"],
                timezone=user.timezone,
                details=meeting_link,
            )

            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton(t.inline.add_to_calendar_button, url=add_to_cal_url)]]
            )

            has_any_attendees = (
                result["attendees"]
                or invited_usernames
                or no_calendar_usernames
                or privacy_disabled_usernames
                or pending_invites_created
            )
            if has_any_attendees:
                add_calendar_text = t.inline.not_listed_add_calendar.replace("_", "")
                text += f"\n{add_calendar_text}"
            else:
                add_calendar_text = t.inline.click_to_add_calendar.replace("_", "")
                text += f"\n{add_calendar_text}"

            await query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)

    except Exception as e:
        logger.exception(f"Error creating meeting: {e}")
        with contextlib.suppress(Exception):
            await query.edit_message_text(f"❌ Error creating meeting: {str(e)}")


async def discard_meeting_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle Cancel button press."""
    query = update.callback_query
    if not query or not query.data:
        return

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = (
            await user_service.get_user(update.effective_user.id) if update.effective_user else None
        )
        t = get_text(user.language if user else "en")

    await query.answer(t.common.cancelled)

    result_id = query.data.replace("discard_", "")

    if context.bot_data:
        context.bot_data.pop(f"meeting_{result_id}", None)

    await query.edit_message_text(t.inline.meeting_cancelled)


async def handle_inline_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text input for inline meeting editing (title, time, date, attendees, links)."""
    if not update.message or not update.message.text or not update.effective_user:
        return

    user_id = update.effective_user.id
    text = update.message.text.strip()

    if not context.bot_data:
        return

    # All states that require text input
    text_input_states = (
        "editing_title",
        "editing_time",
        "editing_date",
        "adding_attendee",
        "adding_link",
    )

    # Find the meeting this user is editing
    meeting_key = None
    meeting_data = None
    for key, data in context.bot_data.items():
        if key.startswith("meeting_") and data.get("user_id") == user_id:
            state = data.get("state", "")
            if state in text_input_states:
                meeting_key = key
                meeting_data = data
                break

    if not meeting_data or not meeting_key:
        return  # No active editing session

    result_id = meeting_key.replace("meeting_", "")
    state = meeting_data.get("state")

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(user_id)
        t = get_text(user.language if user else "en")
        user_timezone = user.timezone if user else "UTC"

    m = meeting_data["meeting"]

    if state == "editing_title":
        # Update title
        m["title"] = text
        meeting_data["state"] = "edit_menu"

        preview = _build_meeting_preview_text(meeting_data, t, user_timezone)
        keyboard = _build_edit_menu_keyboard(result_id, meeting_data, t)
        await update.message.reply_text(
            t.inline.field_updated + "\n\n" + preview,
            parse_mode="Markdown",
            reply_markup=keyboard,
        )

    elif state == "editing_time":
        # Parse time input (e.g., "14:00", "2pm", "14.30")
        try:
            parsed = MeetingParser.parse_time_only(text)
            if parsed:
                # Update time string and recalculate datetimes
                m["time"] = parsed["time_str"]

                # Recalculate start_datetime preserving the date
                old_start = datetime.fromisoformat(m["start_datetime"])
                new_start = old_start.replace(
                    hour=parsed["hour"], minute=parsed["minute"], second=0, microsecond=0
                )

                # Calculate duration from old times
                old_end = datetime.fromisoformat(m["end_datetime"])
                duration = old_end - old_start

                new_end = new_start + duration

                m["start_datetime"] = new_start.isoformat()
                m["end_datetime"] = new_end.isoformat()

                meeting_data["state"] = "edit_menu"

                preview = _build_meeting_preview_text(meeting_data, t, user_timezone)
                keyboard = _build_edit_menu_keyboard(result_id, meeting_data, t)
                await update.message.reply_text(
                    t.inline.field_updated + "\n\n" + preview,
                    parse_mode="Markdown",
                    reply_markup=keyboard,
                )
            else:
                await update.message.reply_text(t.inline.invalid_time_format)
        except Exception:
            await update.message.reply_text(t.inline.invalid_time_format)

    elif state == "editing_date":
        # Parse date input (e.g., "tomorrow", "Jan 20", "20.01")
        try:
            parsed = MeetingParser.parse_date_only(text, user_timezone)
            if parsed:
                m["date"] = parsed["date_str"]

                # Update start and end datetime with new date
                old_start = datetime.fromisoformat(m["start_datetime"])
                old_end = datetime.fromisoformat(m["end_datetime"])
                duration = old_end - old_start

                new_start = old_start.replace(
                    year=parsed["year"], month=parsed["month"], day=parsed["day"]
                )
                new_end = new_start + duration

                m["start_datetime"] = new_start.isoformat()
                m["end_datetime"] = new_end.isoformat()

                meeting_data["state"] = "edit_menu"

                preview = _build_meeting_preview_text(meeting_data, t, user_timezone)
                keyboard = _build_edit_menu_keyboard(result_id, meeting_data, t)
                await update.message.reply_text(
                    t.inline.field_updated + "\n\n" + preview,
                    parse_mode="Markdown",
                    reply_markup=keyboard,
                )
            else:
                await update.message.reply_text(t.inline.invalid_date_format)
        except Exception:
            await update.message.reply_text(t.inline.invalid_date_format)

    elif state == "adding_attendee":
        # Validate and add attendee
        if text.startswith("@"):
            # Username
            username = text[1:]  # Remove @
            if username:
                usernames = m.get("usernames", [])
                if username.lower() not in [u.lower() for u in usernames]:
                    usernames.append(username)
                    m["usernames"] = usernames
                await update.message.reply_text(t.inline.attendee_added)
        elif "@" in text and "." in text:
            # Email
            attendees = m.get("attendees", [])
            if text.lower() not in [a.lower() for a in attendees]:
                attendees.append(text)
                m["attendees"] = attendees
            await update.message.reply_text(t.inline.attendee_added)
        else:
            await update.message.reply_text(t.inline.invalid_email_format)
            return  # Don't change state, let user try again

        # Return to attendees menu
        meeting_data["state"] = "edit_menu"

        async with async_session_factory() as session:
            recent_repo = RecentContactRepository(session)
            recent_contacts = await recent_repo.get_recent_contacts(user.id if user else 0, limit=5)

        keyboard = _build_attendees_keyboard(result_id, meeting_data, recent_contacts, t)
        text_msg = t.inline.current_attendees + "\n\n"
        all_att = m.get("attendees", []) + [f"@{u}" for u in m.get("usernames", [])]
        if all_att:
            text_msg += "\n".join(f"• {a}" for a in all_att)
        else:
            text_msg += t.inline.no_attendees

        await update.message.reply_text(text_msg, parse_mode="Markdown", reply_markup=keyboard)

    elif state == "adding_link":
        # Validate link (basic check)
        if text.startswith("http://") or text.startswith("https://"):
            m["custom_link"] = text
            m["meet_link"] = None  # Clear auto Meet if custom set
            await update.message.reply_text(t.inline.link_added)
        else:
            await update.message.reply_text(t.inline.invalid_link_format)
            return  # Don't change state

        # Return to edit menu
        meeting_data["state"] = "edit_menu"

        preview = _build_meeting_preview_text(meeting_data, t, user_timezone)
        keyboard = _build_edit_menu_keyboard(result_id, meeting_data, t)
        await update.message.reply_text(preview, parse_mode="Markdown", reply_markup=keyboard)


def setup_inline_handlers(app: Application) -> None:
    """Register inline query handlers."""
    app.add_handler(InlineQueryHandler(inline_query))

    # Main actions
    app.add_handler(CallbackQueryHandler(create_meeting_callback, pattern=r"^create_"))
    app.add_handler(CallbackQueryHandler(discard_meeting_callback, pattern=r"^discard_"))

    # Edit menu
    app.add_handler(CallbackQueryHandler(edit_menu_callback, pattern=r"^edit_"))
    app.add_handler(CallbackQueryHandler(back_to_preview_callback, pattern=r"^em_back_"))

    # Edit field callbacks
    # Note: em_title_, em_time_, em_date_ are now handled by edit_session.py
    # which provides button grids and private chat redirect for custom input
    app.add_handler(CallbackQueryHandler(edit_duration_callback, pattern=r"^em_dur_"))
    app.add_handler(CallbackQueryHandler(edit_reminder_callback, pattern=r"^em_rem_"))
    app.add_handler(CallbackQueryHandler(edit_attendees_callback, pattern=r"^em_att_"))
    app.add_handler(CallbackQueryHandler(edit_link_callback, pattern=r"^em_link_"))
    app.add_handler(CallbackQueryHandler(edit_calendar_callback, pattern=r"^em_cal_"))

    # Duration/reminder selection
    app.add_handler(CallbackQueryHandler(set_duration_callback, pattern=r"^dur_"))
    app.add_handler(CallbackQueryHandler(set_reminder_callback, pattern=r"^rem_"))

    # Attendee management
    # Note: att_add_ is now handled by edit_session.py for private chat redirect
    app.add_handler(CallbackQueryHandler(remove_attendee_callback, pattern=r"^att_rem_"))
    app.add_handler(CallbackQueryHandler(add_recent_contact_callback, pattern=r"^att_rc_"))

    # Link management
    # Note: link_custom_ is now handled by edit_session.py for private chat redirect
    app.add_handler(CallbackQueryHandler(add_google_meet_callback, pattern=r"^link_meet_"))
    app.add_handler(CallbackQueryHandler(add_teams_link_callback, pattern=r"^link_teams_"))
    app.add_handler(CallbackQueryHandler(add_zoom_link_callback, pattern=r"^link_zoom_"))
    app.add_handler(CallbackQueryHandler(remove_link_callback, pattern=r"^link_rem_"))

    # No-op handler for display-only buttons
    app.add_handler(CallbackQueryHandler(noop_callback, pattern=r"^noop$"))

    # Text input handler for attendees and custom links
    # This must be added with a low group number so it doesn't interfere with other handlers
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_inline_text_input), group=5
    )
