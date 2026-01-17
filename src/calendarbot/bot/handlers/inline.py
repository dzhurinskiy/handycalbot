"""Inline query handler for meeting creation."""

import contextlib
import logging
import uuid
from datetime import datetime
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
)

from calendarbot.db.repository import PendingInviteRepository
from calendarbot.db.session import async_session_factory
from calendarbot.i18n import get_text
from calendarbot.services.calendar import CalendarService
from calendarbot.services.parser import MeetingParser
from calendarbot.services.user import UserService
from calendarbot.services.username_resolver import UsernameResolverService
from calendarbot.utils.timezone import TimezoneHelper

logger = logging.getLogger(__name__)


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


def build_add_to_calendar_url(
    title: str,
    start: datetime,
    end: datetime,
    timezone: str,
) -> str:
    """Build a universal Google Calendar 'Add to Calendar' URL.

    This URL works for anyone - they can add the event to their own calendar.
    """
    # Convert to UTC for the URL
    start_utc = TimezoneHelper.to_utc(start, timezone)
    end_utc = TimezoneHelper.to_utc(end, timezone)

    # Format: YYYYMMDDTHHmmssZ
    start_str = start_utc.strftime("%Y%m%dT%H%M%SZ")
    end_str = end_utc.strftime("%Y%m%dT%H%M%SZ")

    params = {
        "action": "TEMPLATE",
        "text": title,
        "dates": f"{start_str}/{end_str}",
    }

    query = "&".join(f"{k}={quote(str(v))}" for k, v in params.items())
    return f"https://calendar.google.com/calendar/render?{query}"


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline queries - parse meeting command and show preview."""
    query = update.inline_query
    if not query or not query.from_user:
        return

    text = query.query.strip()

    # Get user settings
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
            # Show help when empty
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

        # Check if calendar is connected
        calendar_connected = await user_service.is_calendar_connected(user)

        # Extract user settings while session is active (avoid detached object issues)
        user_timezone = user.timezone
        user_default_duration = user.default_duration
        user_default_reminder = user.default_reminder
        user_telegram_id = query.from_user.id

    # Parse the query
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
            # Check rate limit first
            remaining = await resolver.get_remaining_lookups(user_telegram_id)
            if remaining < len(meeting.usernames):
                rate_limited = True
            else:
                username_statuses = await resolver.get_username_statuses(
                    meeting.usernames, user_telegram_id
                )

    # Generate preview with reminder info and username statuses
    preview = parser.format_preview(
        meeting,
        default_reminder=user_default_reminder,
        username_statuses=username_statuses if not rate_limited else None,
    )

    if rate_limited:
        preview += f"\n\n{t.inline.rate_limit_warning}"

    if not calendar_connected:
        preview += f"\n\n{t.inline.calendar_not_connected_warning}"

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
            "usernames": meeting.usernames,
            "start_datetime": meeting.start_datetime.isoformat(),
            "end_datetime": meeting.end_datetime.isoformat(),
            "reminders": meeting.reminders,
            "use_default_reminder": meeting.use_default_reminder,
        },
    }

    # Create inline keyboard for confirmation
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"✅ {t.inline.create_meeting_button}", callback_data=f"create_{result_id}"
                ),
                InlineKeyboardButton(
                    f"❌ {t.inline.cancel_button}", callback_data=f"discard_{result_id}"
                ),
            ]
        ]
    )

    date_display = meeting.date or t.inline.today

    # Count total attendees (emails + usernames)
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


async def create_meeting_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle Create Meeting button press."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    # Get user's language first
    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

    await query.answer(t.inline.creating_meeting)

    result_id = query.data.replace("create_", "")

    try:
        # Get stored meeting data
        if context.bot_data is None:
            await query.edit_message_text(t.inline.meeting_data_expired)
            return

        meeting_data = context.bot_data.get(f"meeting_{result_id}")
        if not meeting_data:
            await query.edit_message_text(t.inline.meeting_data_expired)
            return

        # Verify user
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

            # Reconstruct ParsedMeeting
            from calendarbot.services.parser import ParsedMeeting

            m = meeting_data["meeting"]
            usernames = m.get("usernames", [])

            # Resolve usernames to emails
            resolved_emails: list[str] = []
            unresolved_usernames: list[str] = []
            if usernames:
                resolver = UsernameResolverService(session)
                resolved_emails, unresolved_usernames = await resolver.get_emails_for_meeting(
                    usernames, update.effective_user.id
                )

            # Combine manual emails with resolved username emails
            all_attendees = m["attendees"] + resolved_emails

            parsed = ParsedMeeting(
                time=m["time"],
                date=m["date"],
                title=m["title"],
                attendees=all_attendees,
                usernames=[],  # Clear usernames as they're now resolved
                start_datetime=datetime.fromisoformat(m["start_datetime"]),
                end_datetime=datetime.fromisoformat(m["end_datetime"]),
                reminders=m.get("reminders"),
                use_default_reminder=m.get("use_default_reminder", False),
            )

            calendar_service = CalendarService(session)
            result = await calendar_service.create_meeting(user, parsed)

            # Create pending invites for unresolved usernames
            pending_invites_created: list[str] = []
            if unresolved_usernames and "event_id" in result:
                pending_repo = PendingInviteRepository(session)
                for username in unresolved_usernames:
                    await pending_repo.create(
                        inviter_telegram_id=update.effective_user.id,
                        invitee_username=username,
                        meeting_id=result["event_id"],
                        meeting_title=parsed.title,
                        meeting_time=parsed.start_datetime,
                    )
                    pending_invites_created.append(username)

            await session.commit()

        # Clean up stored data
        context.bot_data.pop(f"meeting_{result_id}", None)

        if "error" in result:
            await query.edit_message_text(f"❌ Error: {result['error']}")
        else:
            start_str = result["start"].strftime("%H:%M on %d %b %Y")
            text = f"✅ {t.inline.meeting_created}\n\n"
            text += f"**{result['title']}**\n"
            text += f"🕐 {start_str}\n"

            # Show reminder info
            reminders = result.get("reminders")
            if reminders:
                reminder_text = _format_reminders(reminders, t)
                text += f"{t.inline.reminder_label.format(reminder=reminder_text)}\n"

            # Show invitations sent (both email and resolved usernames)
            original_usernames = m.get("usernames", [])
            resolved_usernames = [u for u in original_usernames if u not in unresolved_usernames]

            if result["attendees"] or resolved_usernames:
                text += f"\n{t.inline.invitations_sent}\n"
                # Show resolved usernames
                for username in resolved_usernames:
                    text += f"  • @{username} ({t.inline.username_registered})\n"
                # Show manual email addresses
                for email in m["attendees"]:  # Original emails only
                    text += f"  • {email}\n"
                text += f"\n{t.inline.attendees_will_receive}\n"

            # Show pending invites for unresolved usernames
            if pending_invites_created:
                text += f"\n{t.inline.pending_invites_note}\n"
                for username in pending_invites_created:
                    text += f"  • @{username}\n"

            # Build universal "Add to Calendar" link that works for anyone
            add_to_cal_url = build_add_to_calendar_url(
                title=result["title"],
                start=result["start"],
                end=result["end"],
                timezone=user.timezone,
            )

            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton(t.inline.add_to_calendar_button, url=add_to_cal_url)]]
            )

            if result["attendees"] or resolved_usernames:
                text += f"\n{t.inline.not_listed_add_calendar}"
            else:
                text += f"\n{t.inline.click_to_add_calendar}"

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

    # Get user's language
    async with async_session_factory() as session:
        user_service = UserService(session)
        user = (
            await user_service.get_user(update.effective_user.id) if update.effective_user else None
        )
        t = get_text(user.language if user else "en")

    await query.answer(t.common.cancelled)

    result_id = query.data.replace("discard_", "")

    # Clean up stored data
    if context.bot_data:
        context.bot_data.pop(f"meeting_{result_id}", None)

    await query.edit_message_text(t.inline.meeting_cancelled)


def setup_inline_handlers(app: Application) -> None:
    """Register inline query handlers."""
    app.add_handler(InlineQueryHandler(inline_query))
    app.add_handler(CallbackQueryHandler(create_meeting_callback, pattern=r"^create_"))
    app.add_handler(CallbackQueryHandler(discard_meeting_callback, pattern=r"^discard_"))
