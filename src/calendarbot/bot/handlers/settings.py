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

from calendarbot.bot.commands import set_user_commands
from calendarbot.db.session import async_session_factory
from calendarbot.i18n import LANGUAGE_NAMES, get_text
from calendarbot.integrations.google import GoogleOAuthFlow
from calendarbot.integrations.outlook import OutlookOAuthFlow
from calendarbot.integrations.zoom import ZoomOAuthFlow
from calendarbot.services.user import UserService
from calendarbot.utils.timezone import TimezoneHelper

logger = logging.getLogger(__name__)

# Conversation states
AWAITING_TIMEZONE = 1
AWAITING_DURATION = 2
AWAITING_REMINDER = 3

# Reminder options in minutes
REMINDER_OPTIONS = [
    (None, "no_reminder"),
    (10, "10_min"),
    (15, "15_min"),
    (30, "30_min"),
    (60, "1_hour"),
    (1440, "1_day"),
]


def _format_reminder_setting(reminder: str | None, t) -> str:
    """Format reminder setting for display."""
    if not reminder:
        return t.settings.no_reminder
    minutes_list = [int(x) for x in reminder.split(",")]
    parts = []
    for m in minutes_list:
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
    return ", ".join(parts) + " " + t.settings.before


def _get_reminder_label(minutes: int | None, t) -> str:
    """Get translated label for reminder option."""
    if minutes is None:
        return t.settings.no_reminder
    elif minutes == 10:
        return f"10 {t.settings.minutes}"
    elif minutes == 15:
        return f"15 {t.settings.minutes}"
    elif minutes == 30:
        return f"30 {t.settings.minutes}"
    elif minutes == 60:
        return f"1 {t.settings.hour}"
    elif minutes == 1440:
        return f"1 {t.settings.day}"
    return f"{minutes} {t.settings.minutes}"


async def settings_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /settings command - show current settings."""
    if not update.effective_user or not update.message:
        return

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if not user:
            t = get_text("en")
            await update.message.reply_text(t.common.please_start_first)
            return

        t = get_text(user.language)
        summary = await user_service.get_user_summary(user)

        # Format reminder display
        reminder_display = _format_reminder_setting(user.default_reminder, t)

        # Get privacy setting
        privacy_enabled = user.allow_username_invites

    # Format notifications status
    notifications_status = (
        f"✅ {t.settings.enabled}" if user.notifications_enabled else f"❌ {t.settings.disabled}"
    )

    # Format calendar status
    google_status = (
        t.settings.connected
        if summary["google_calendar"] == "Connected"
        else t.settings.not_connected
    )

    outlook_status = (
        t.settings.connected
        if summary.get("outlook_calendar") == "Connected"
        else t.settings.not_connected
    )

    # Format Zoom status
    zoom_status = (
        t.settings.connected if summary.get("zoom") == "Connected" else t.settings.not_connected
    )

    # Format privacy status
    privacy_status = f"✅ {t.settings.enabled}" if privacy_enabled else f"❌ {t.settings.disabled}"

    # Format default calendar preference (only show if both connected)
    default_calendar_line = ""
    default_calendar_cmd = ""
    google_connected = summary["google_calendar"] == "Connected"
    outlook_connected = summary.get("outlook_calendar") == "Connected"
    if google_connected and outlook_connected:
        if user.default_calendar == "outlook":
            default_cal_display = t.settings.outlook_calendar_label
        elif user.default_calendar == "google":
            default_cal_display = t.settings.google_calendar_label
        else:
            # No preference set, show which one is being used (Google by default)
            default_cal_display = t.settings.google_calendar_label
        default_calendar_line = f"\n🎯 {t.settings.default_calendar_label}: {default_cal_display}"
        default_calendar_cmd = f"\n/defaultcalendar - {t.settings.default_calendar_label}"

    text = f"""
{t.settings.your_settings}

📍 {t.settings.timezone_label}: `{summary['timezone']}`
⏱️ {t.settings.duration_label}: `{summary['default_duration']} {t.settings.minutes}`
🔔 {t.settings.reminder_label}: `{reminder_display}`
📬 {t.settings.notifications_label}: {notifications_status}
🔒 {t.settings.privacy_username_invites}: {privacy_status}
📅 {t.settings.google_calendar_label}: {google_status}
📆 {t.settings.outlook_calendar_label}: {outlook_status}
📹 Zoom: {zoom_status}{default_calendar_line}

{t.settings.change_settings}
/connect - Connect services
/disconnect - Disconnect services
/timezone - {t.settings.timezone_label}
/duration - {t.settings.duration_label}
/reminder - {t.settings.reminder_label}
/notifications - {t.settings.notifications_label}
/privacy - {t.settings.privacy_username_invites}
/language - Language{default_calendar_cmd}
"""

    await update.message.reply_text(text, parse_mode="Markdown")


async def connect_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /connect command - unified connection for all services."""
    if not update.effective_user or not update.message:
        return

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if not user:
            t = get_text("en")
            await update.message.reply_text(t.common.please_start_first)
            return

        t = get_text(user.language)

        # Check connection status
        google_connected = await user_service.is_calendar_connected(user)
        outlook_connected = await user_service.is_outlook_connected(user)
        zoom_connected = await user_service.is_zoom_connected(user)

    # Build keyboard based on what's connected
    buttons = []

    # Connected services section
    connected_text = ""
    if google_connected or outlook_connected or zoom_connected:
        connected_text = f"{t.settings.connected_services_title}:\n"
        if google_connected:
            connected_text += "📅 Google Calendar ✅\n"
            buttons.append(
                [
                    InlineKeyboardButton(
                        f"📅 {t.settings.manage_button} Google Calendar",
                        callback_data="manage_google",
                    )
                ]
            )
        if outlook_connected:
            connected_text += "📆 Outlook Calendar ✅\n"
            buttons.append(
                [
                    InlineKeyboardButton(
                        f"📆 {t.settings.manage_button} Outlook Calendar",
                        callback_data="manage_outlook",
                    )
                ]
            )
        if zoom_connected:
            connected_text += "📹 Zoom ✅\n"
            buttons.append(
                [
                    InlineKeyboardButton(
                        f"📹 {t.settings.manage_button} Zoom",
                        callback_data="manage_zoom",
                    )
                ]
            )
        connected_text += "\n"

    # Services to connect
    connect_text = ""
    available_services = []
    if not google_connected:
        available_services.append(("📅 Google Calendar", "connect_google"))
    if not outlook_connected:
        available_services.append(("📆 Outlook Calendar", "connect_outlook"))
    if not zoom_connected:
        available_services.append(("📹 Zoom", "connect_zoom"))

    if available_services:
        if connected_text:
            connect_text = f"{t.settings.connect_another_service}\n"
        else:
            connect_text = f"{t.settings.connect_select_service}\n"
        for label, callback in available_services:
            buttons.append([InlineKeyboardButton(label, callback_data=callback)])

    # Build final message
    message = f"{t.settings.connect_services_title}\n\n"
    if connected_text:
        message += connected_text
    if connect_text:
        message += connect_text

    if not buttons:
        message += "All services are already connected!"

    await update.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
        parse_mode="Markdown",
    )


async def connect_google_callback(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle Google Calendar connection - show mode selection."""
    query = update.callback_query
    if not query or not update.effective_user:
        return

    await query.answer()

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

    keyboard = [
        [InlineKeyboardButton(t.settings.connect_full_access_button, callback_data="goog_full")],
        [
            InlineKeyboardButton(
                t.settings.connect_privacy_mode_button, callback_data="goog_privacy"
            )
        ],
        [InlineKeyboardButton(t.inline.back_button, callback_data="connect_back")],
    ]

    await query.edit_message_text(
        f"{t.settings.connect_mode_title}\n\n"
        f"{t.settings.connect_full_access_desc}\n\n"
        f"{t.settings.connect_privacy_mode_desc}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


async def connect_outlook_callback(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle Outlook Calendar connection - show mode selection."""
    query = update.callback_query
    if not query or not update.effective_user:
        return

    await query.answer()

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

    keyboard = [
        [InlineKeyboardButton(t.settings.connect_full_access_button, callback_data="outl_full")],
        [
            InlineKeyboardButton(
                t.settings.connect_privacy_mode_button, callback_data="outl_privacy"
            )
        ],
        [InlineKeyboardButton(t.inline.back_button, callback_data="connect_back")],
    ]

    await query.edit_message_text(
        f"{t.settings.connect_outlook_mode_title}\n\n"
        f"{t.settings.connect_full_access_desc}\n\n"
        f"{t.settings.connect_privacy_mode_desc}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


async def connect_zoom_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle Zoom connection - generate OAuth URL."""
    query = update.callback_query
    if not query or not update.effective_user:
        return

    await query.answer()

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

    # Generate OAuth state
    state = f"{update.effective_user.id}:{secrets.token_urlsafe(16)}"

    # Store state in context for verification
    if context.bot_data is None:
        context.bot_data = {}
    context.bot_data[f"zoom_oauth_state_{update.effective_user.id}"] = state

    # Generate auth URL
    oauth = ZoomOAuthFlow()
    auth_url = oauth.get_authorization_url(state)

    keyboard = [
        [InlineKeyboardButton(t.settings.connect_zoom_button, url=auth_url)],
        [InlineKeyboardButton(t.inline.back_button, callback_data="connect_back")],
    ]

    await query.edit_message_text(
        t.settings.click_to_connect_zoom,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def google_mode_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle Google connection mode selection."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    await query.answer()

    privacy_mode = query.data == "goog_privacy"

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

    # Generate OAuth state with privacy mode flag
    state = f"{update.effective_user.id}:{secrets.token_urlsafe(16)}:{'privacy' if privacy_mode else 'full'}"

    # Store state in context for verification
    if context.bot_data is None:
        context.bot_data = {}
    context.bot_data[f"oauth_state_{update.effective_user.id}"] = state

    # Generate auth URL with appropriate scopes
    oauth = GoogleOAuthFlow()
    auth_url = oauth.get_authorization_url(state, privacy_mode=privacy_mode)

    keyboard = [
        [InlineKeyboardButton(t.settings.connect_button, url=auth_url)],
        [InlineKeyboardButton(t.inline.back_button, callback_data="connect_google")],
    ]

    await query.edit_message_text(
        t.settings.click_to_connect,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def outlook_mode_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle Outlook connection mode selection."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    await query.answer()

    privacy_mode = query.data == "outl_privacy"

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        t = get_text(user.language if user else "en")

    # Generate OAuth state with privacy mode flag
    state = f"{update.effective_user.id}:{secrets.token_urlsafe(16)}:{'privacy' if privacy_mode else 'full'}"

    # Store state in context for verification
    if context.bot_data is None:
        context.bot_data = {}
    context.bot_data[f"outlook_oauth_state_{update.effective_user.id}"] = state

    # Generate auth URL with appropriate scopes
    oauth = OutlookOAuthFlow()
    auth_url = oauth.get_authorization_url(state, privacy_mode=privacy_mode)

    keyboard = [
        [InlineKeyboardButton(t.settings.connect_outlook_button, url=auth_url)],
        [InlineKeyboardButton(t.inline.back_button, callback_data="connect_outlook")],
    ]

    await query.edit_message_text(
        t.settings.click_to_connect_outlook,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def connect_back_callback(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle back button from connect submenus."""
    query = update.callback_query
    if not query or not update.effective_user:
        return

    await query.answer()

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if not user:
            t = get_text("en")
            await query.edit_message_text(t.common.error_user_not_found)
            return

        t = get_text(user.language)

        # Check connection status
        google_connected = await user_service.is_calendar_connected(user)
        outlook_connected = await user_service.is_outlook_connected(user)
        zoom_connected = await user_service.is_zoom_connected(user)

    # Build keyboard based on what's connected
    buttons = []

    # Connected services section
    connected_text = ""
    if google_connected or outlook_connected or zoom_connected:
        connected_text = f"{t.settings.connected_services_title}:\n"
        if google_connected:
            connected_text += "📅 Google Calendar ✅\n"
            buttons.append(
                [
                    InlineKeyboardButton(
                        f"📅 {t.settings.manage_button} Google Calendar",
                        callback_data="manage_google",
                    )
                ]
            )
        if outlook_connected:
            connected_text += "📆 Outlook Calendar ✅\n"
            buttons.append(
                [
                    InlineKeyboardButton(
                        f"📆 {t.settings.manage_button} Outlook Calendar",
                        callback_data="manage_outlook",
                    )
                ]
            )
        if zoom_connected:
            connected_text += "📹 Zoom ✅\n"
            buttons.append(
                [
                    InlineKeyboardButton(
                        f"📹 {t.settings.manage_button} Zoom",
                        callback_data="manage_zoom",
                    )
                ]
            )
        connected_text += "\n"

    # Services to connect
    connect_text = ""
    available_services = []
    if not google_connected:
        available_services.append(("📅 Google Calendar", "connect_google"))
    if not outlook_connected:
        available_services.append(("📆 Outlook Calendar", "connect_outlook"))
    if not zoom_connected:
        available_services.append(("📹 Zoom", "connect_zoom"))

    if available_services:
        if connected_text:
            connect_text = f"{t.settings.connect_another_service}\n"
        else:
            connect_text = f"{t.settings.connect_select_service}\n"
        for label, callback in available_services:
            buttons.append([InlineKeyboardButton(label, callback_data=callback)])

    # Build final message
    message = f"{t.settings.connect_services_title}\n\n"
    if connected_text:
        message += connected_text
    if connect_text:
        message += connect_text

    if not buttons:
        message += "All services are already connected!"

    await query.edit_message_text(
        message,
        reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
        parse_mode="Markdown",
    )


async def manage_google_callback(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle manage Google calendar button."""
    query = update.callback_query
    if not query or not update.effective_user:
        return

    await query.answer()

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if not user:
            t = get_text("en")
            await query.edit_message_text(t.common.error_user_not_found)
            return

        t = get_text(user.language)

        # Get current mode
        from calendarbot.db.repository import OAuthTokenRepository

        token_repo = OAuthTokenRepository(session)
        token = await token_repo.get_token(user.id, "google")
        is_privacy = token.privacy_mode if token else False

    current_mode = t.settings.current_mode_privacy if is_privacy else t.settings.current_mode_full

    keyboard = [
        [
            InlineKeyboardButton(
                (
                    t.settings.switch_to_full_button
                    if is_privacy
                    else t.settings.switch_to_privacy_button
                ),
                callback_data="goog_full" if is_privacy else "goog_privacy",
            )
        ],
        [InlineKeyboardButton(t.settings.disconnect_button, callback_data="disc_google")],
        [InlineKeyboardButton(t.inline.back_button, callback_data="connect_back")],
    ]

    await query.edit_message_text(
        t.settings.calendar_connected_status.format(mode=current_mode),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


async def manage_outlook_callback(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle manage Outlook calendar button."""
    query = update.callback_query
    if not query or not update.effective_user:
        return

    await query.answer()

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if not user:
            t = get_text("en")
            await query.edit_message_text(t.common.error_user_not_found)
            return

        t = get_text(user.language)

        # Get current mode
        from calendarbot.db.repository import OAuthTokenRepository

        token_repo = OAuthTokenRepository(session)
        token = await token_repo.get_token(user.id, "outlook")
        is_privacy = token.privacy_mode if token else False

    current_mode = t.settings.current_mode_privacy if is_privacy else t.settings.current_mode_full

    keyboard = [
        [
            InlineKeyboardButton(
                (
                    t.settings.switch_to_full_button
                    if is_privacy
                    else t.settings.switch_to_privacy_button
                ),
                callback_data="outl_full" if is_privacy else "outl_privacy",
            )
        ],
        [InlineKeyboardButton(t.settings.disconnect_button, callback_data="disc_outlook")],
        [InlineKeyboardButton(t.inline.back_button, callback_data="connect_back")],
    ]

    await query.edit_message_text(
        t.settings.outlook_connected_status.format(mode=current_mode),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


async def manage_zoom_callback(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle manage Zoom button."""
    query = update.callback_query
    if not query or not update.effective_user:
        return

    await query.answer()

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if not user:
            t = get_text("en")
            await query.edit_message_text(t.common.error_user_not_found)
            return

        t = get_text(user.language)

    keyboard = [
        [InlineKeyboardButton(t.settings.disconnect_button, callback_data="disc_zoom")],
        [InlineKeyboardButton(t.inline.back_button, callback_data="connect_back")],
    ]

    await query.edit_message_text(
        t.settings.zoom_connected_status,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


async def disconnect_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /disconnect command - unified disconnection for all services."""
    if not update.effective_user or not update.message:
        return

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if not user:
            t = get_text("en")
            await update.message.reply_text(t.common.please_start_first)
            return

        t = get_text(user.language)

        # Check connection status
        google_connected = await user_service.is_calendar_connected(user)
        outlook_connected = await user_service.is_outlook_connected(user)
        zoom_connected = await user_service.is_zoom_connected(user)

    # If nothing connected
    if not google_connected and not outlook_connected and not zoom_connected:
        await update.message.reply_text(t.settings.no_services_connected)
        return

    # Build keyboard with connected services
    buttons = []
    if google_connected:
        buttons.append([InlineKeyboardButton("📅 Google Calendar", callback_data="disc_google")])
    if outlook_connected:
        buttons.append([InlineKeyboardButton("📆 Outlook Calendar", callback_data="disc_outlook")])
    if zoom_connected:
        buttons.append([InlineKeyboardButton("📹 Zoom", callback_data="disc_zoom")])

    await update.message.reply_text(
        f"{t.settings.disconnect_services_title}\n\n{t.settings.disconnect_select_service}",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="Markdown",
    )


async def disconnect_google_callback(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle Google Calendar disconnection."""
    query = update.callback_query
    if not query or not update.effective_user:
        return

    await query.answer()

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if not user:
            t = get_text("en")
            await query.edit_message_text(t.common.error_user_not_found)
            return

        t = get_text(user.language)

        await user_service.disconnect_calendar(user)
        await session.commit()

    await query.edit_message_text(t.settings.service_disconnected.format(service="Google Calendar"))


async def disconnect_outlook_callback(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle Outlook Calendar disconnection."""
    query = update.callback_query
    if not query or not update.effective_user:
        return

    await query.answer()

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if not user:
            t = get_text("en")
            await query.edit_message_text(t.common.error_user_not_found)
            return

        t = get_text(user.language)

        await user_service.disconnect_outlook(user)
        await session.commit()

    await query.edit_message_text(
        t.settings.service_disconnected.format(service="Outlook Calendar")
    )


async def disconnect_zoom_callback(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle Zoom disconnection."""
    query = update.callback_query
    if not query or not update.effective_user:
        return

    await query.answer()

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if not user:
            t = get_text("en")
            await query.edit_message_text(t.common.error_user_not_found)
            return

        t = get_text(user.language)

        await user_service.disconnect_zoom(user)
        await session.commit()

    await query.edit_message_text(t.settings.service_disconnected.format(service="Zoom"))


async def timezone_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /timezone command - start timezone selection."""
    if not update.message:
        return ConversationHandler.END

    # Get user's language
    async with async_session_factory() as session:
        user_service = UserService(session)
        user = (
            await user_service.get_user(update.effective_user.id) if update.effective_user else None
        )
        user_lang = user.language if user else "en"

    t = get_text(user_lang)

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
        t.settings.select_timezone,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="Markdown",
    )

    return AWAITING_TIMEZONE


async def timezone_callback(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle timezone button selection (within conversation)."""
    await _handle_timezone_selection(update)
    return ConversationHandler.END


async def timezone_callback_standalone(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
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
            t = get_text(user.language)
        else:
            t = get_text("en")

    await query.edit_message_text(
        t.settings.timezone_set_ready.format(timezone=tz),
        parse_mode="Markdown",
    )


async def timezone_text(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle manual timezone input."""
    if not update.message or not update.message.text or not update.effective_user:
        return ConversationHandler.END

    tz = update.message.text.strip()

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)
        user_lang = user.language if user else "en"
        t = get_text(user_lang)

        if not TimezoneHelper.is_valid_timezone(tz):
            await update.message.reply_text(
                t.settings.invalid_timezone.format(timezone=tz),
                parse_mode="Markdown",
            )
            return AWAITING_TIMEZONE

        if user:
            await user_service.update_timezone(user, tz)
            await session.commit()

    await update.message.reply_text(
        t.settings.timezone_set.format(timezone=tz),
        parse_mode="Markdown",
    )
    return ConversationHandler.END


async def duration_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /duration command."""
    if not update.message:
        return ConversationHandler.END

    # Get user's language
    async with async_session_factory() as session:
        user_service = UserService(session)
        user = (
            await user_service.get_user(update.effective_user.id) if update.effective_user else None
        )
        user_lang = user.language if user else "en"

    t = get_text(user_lang)

    buttons = [
        [
            InlineKeyboardButton(f"15 {t.settings.minutes}", callback_data="dur_15"),
            InlineKeyboardButton(f"30 {t.settings.minutes}", callback_data="dur_30"),
        ],
        [
            InlineKeyboardButton(f"45 {t.settings.minutes}", callback_data="dur_45"),
            InlineKeyboardButton(f"60 {t.settings.minutes}", callback_data="dur_60"),
        ],
        [
            InlineKeyboardButton(f"90 {t.settings.minutes}", callback_data="dur_90"),
            InlineKeyboardButton(f"120 {t.settings.minutes}", callback_data="dur_120"),
        ],
    ]

    await update.message.reply_text(
        t.settings.select_duration,
        reply_markup=InlineKeyboardMarkup(buttons),
    )

    return AWAITING_DURATION


async def duration_callback(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> int:
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
            t = get_text(user.language)
        else:
            t = get_text("en")

    await query.edit_message_text(t.settings.duration_set.format(duration=duration))
    return ConversationHandler.END


async def reminder_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /reminder command."""
    if not update.message:
        return ConversationHandler.END

    # Get user's language
    async with async_session_factory() as session:
        user_service = UserService(session)
        user = (
            await user_service.get_user(update.effective_user.id) if update.effective_user else None
        )
        user_lang = user.language if user else "en"

    t = get_text(user_lang)

    buttons = []
    for minutes, _ in REMINDER_OPTIONS:
        label = _get_reminder_label(minutes, t)
        callback_data = f"rem_{minutes}" if minutes is not None else "rem_none"
        buttons.append([InlineKeyboardButton(label, callback_data=callback_data)])

    await update.message.reply_text(
        t.settings.select_reminder,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="Markdown",
    )

    return AWAITING_REMINDER


async def reminder_callback(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle reminder button selection."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return ConversationHandler.END

    await query.answer()

    # Parse the reminder value
    value = query.data.replace("rem_", "")
    reminder = None if value == "none" else value

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if user:
            await user_service.update_reminder(user, reminder)
            await session.commit()
            t = get_text(user.language)
        else:
            t = get_text("en")

    display = _format_reminder_setting(reminder, t)
    await query.edit_message_text(
        f"✅ {t.settings.reminder_set.format(reminder=display)}\n\n{t.settings.reminder_override_hint}",
        parse_mode="Markdown",
    )
    return ConversationHandler.END


async def cancel_conversation(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel any conversation with message."""
    if update.message:
        # Get user's language
        async with async_session_factory() as session:
            user_service = UserService(session)
            user = (
                await user_service.get_user(update.effective_user.id)
                if update.effective_user
                else None
            )
            user_lang = user.language if user else "en"
        t = get_text(user_lang)
        await update.message.reply_text(t.common.cancelled)
    return ConversationHandler.END


async def silent_cancel(_update: Update, _context: ContextTypes.DEFAULT_TYPE) -> int:
    """Silently exit conversation without message (for when user enters another command)."""
    return ConversationHandler.END


async def notifications_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /notifications command - toggle meeting notifications."""
    if not update.effective_user or not update.message:
        return

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if not user:
            t = get_text("en")
            await update.message.reply_text(t.common.please_start_first)
            return

        t = get_text(user.language)

        # Store current state for display
        current_state = user.notifications_enabled

    # Show toggle buttons
    enable_label = f"✅ {t.settings.enable_button}" + (
        f" {t.settings.current_suffix}" if current_state else ""
    )
    disable_label = f"❌ {t.settings.disable_button}" + (
        f" {t.settings.current_suffix}" if not current_state else ""
    )

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(enable_label, callback_data="notif_on"),
                InlineKeyboardButton(disable_label, callback_data="notif_off"),
            ]
        ]
    )

    status = f"✅ {t.settings.enabled}" if current_state else f"❌ {t.settings.disabled}"

    await update.message.reply_text(
        f"{t.settings.notifications_title}\n\n"
        f"{t.settings.notifications_status.format(status=status)}\n\n"
        f"{t.settings.notifications_explanation}\n\n"
        f"{t.settings.select_option}",
        reply_markup=keyboard,
        parse_mode="Markdown",
    )


async def notifications_callback(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle notification toggle button press."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    await query.answer()

    # Determine new state
    new_state = query.data == "notif_on"

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if not user:
            t = get_text("en")
            await query.edit_message_text(t.common.error_user_not_found)
            return

        t = get_text(user.language)

        # Update notifications setting
        await user_service.update_notifications(user, new_state)
        await session.commit()

    status = t.settings.enabled.lower() if new_state else t.settings.disabled.lower()
    emoji = "✅" if new_state else "❌"
    follow_up = (
        t.settings.will_receive_reminders if new_state else t.settings.will_not_receive_reminders
    )

    await query.edit_message_text(
        f"{t.settings.notifications_updated.format(emoji=emoji, status=status)}\n\n{follow_up}",
        parse_mode="Markdown",
    )


async def language_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /language command - show language selection."""
    if not update.effective_user or not update.message:
        return

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if not user:
            t = get_text("en")
            await update.message.reply_text(t.common.please_start_first)
            return

        t = get_text(user.language)

    # Create language buttons (2 columns)
    buttons = []
    languages = list(LANGUAGE_NAMES.items())

    for i in range(0, len(languages), 2):
        row = []
        for j in range(2):
            if i + j < len(languages):
                lang_code, lang_name = languages[i + j]
                row.append(InlineKeyboardButton(lang_name, callback_data=f"lang_{lang_code}"))
        buttons.append(row)

    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        t.settings.select_language,
        reply_markup=keyboard,
    )


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle language selection button press."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    await query.answer()

    lang_code = query.data.replace("lang_", "")

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if not user:
            t = get_text("en")
            await query.edit_message_text(t.common.error_user_not_found)
            return

        await user_service.update_language(user, lang_code)
        await session.commit()

    # Set localized commands for this user
    await set_user_commands(context.bot, update.effective_user.id, lang_code)

    # Get translations in the NEW language
    t = get_text(lang_code)
    await query.edit_message_text(t.settings.language_updated)


async def privacy_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /privacy command - show privacy settings."""
    if not update.effective_user or not update.message:
        return

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if not user:
            t = get_text("en")
            await update.message.reply_text(t.common.please_start_first)
            return

        t = get_text(user.language)
        current_state = user.allow_username_invites

    # Show toggle buttons
    enable_label = f"✅ {t.settings.enable_button}" + (
        f" {t.settings.current_suffix}" if current_state else ""
    )
    disable_label = f"❌ {t.settings.disable_button}" + (
        f" {t.settings.current_suffix}" if not current_state else ""
    )

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(enable_label, callback_data="privacy_on"),
                InlineKeyboardButton(disable_label, callback_data="privacy_off"),
            ]
        ]
    )

    status = f"✅ {t.settings.enabled}" if current_state else f"❌ {t.settings.disabled}"
    description = (
        t.settings.privacy_enabled_desc if current_state else t.settings.privacy_disabled_desc
    )

    await update.message.reply_text(
        f"{t.settings.privacy_title}\n\n"
        f"{t.settings.privacy_username_invites}: {status}\n\n"
        f"_{description}_\n\n"
        f"{t.settings.select_option}",
        reply_markup=keyboard,
        parse_mode="Markdown",
    )


async def privacy_callback(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle privacy toggle button press."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    await query.answer()

    # Determine new state
    new_state = query.data == "privacy_on"

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if not user:
            t = get_text("en")
            await query.edit_message_text(t.common.error_user_not_found)
            return

        t = get_text(user.language)

        # Update privacy setting
        await user_service.update_privacy(user, new_state)
        await session.commit()

    status = t.settings.enabled.lower() if new_state else t.settings.disabled.lower()
    emoji = "✅" if new_state else "❌"
    follow_up = t.settings.privacy_enabled_desc if new_state else t.settings.privacy_disabled_desc

    await query.edit_message_text(
        f"{t.settings.privacy_updated.format(emoji=emoji, status=status)}\n\n_{follow_up}_",
        parse_mode="Markdown",
    )


async def defaultcalendar_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /defaultcalendar command - set preferred calendar provider."""
    if not update.effective_user or not update.message:
        return

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if not user:
            t = get_text("en")
            await update.message.reply_text(t.common.please_start_first)
            return

        t = get_text(user.language)

        # Check if both calendars are connected
        google_connected = await user_service.is_calendar_connected(user)
        outlook_connected = await user_service.is_outlook_connected(user)

        if not (google_connected and outlook_connected):
            await update.message.reply_text(
                t.settings.default_calendar_requires_both,
                parse_mode="Markdown",
            )
            return

        current_pref = user.default_calendar or "google"

    # Show selection buttons
    google_label = "📅 Google Calendar" + (
        f" {t.settings.current_suffix}" if current_pref == "google" else ""
    )
    outlook_label = "📆 Outlook Calendar" + (
        f" {t.settings.current_suffix}" if current_pref == "outlook" else ""
    )

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(google_label, callback_data="defcal_google")],
            [InlineKeyboardButton(outlook_label, callback_data="defcal_outlook")],
        ]
    )

    await update.message.reply_text(
        f"{t.settings.default_calendar_title}\n\n"
        f"{t.settings.default_calendar_desc}\n\n"
        f"{t.settings.select_option}",
        reply_markup=keyboard,
        parse_mode="Markdown",
    )


async def defaultcalendar_callback(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle default calendar selection button press."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user:
        return

    await query.answer()

    # Extract provider from callback data (defcal_google or defcal_outlook)
    new_provider = query.data.replace("defcal_", "")
    if new_provider not in ("google", "outlook"):
        return

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(update.effective_user.id)

        if not user:
            t = get_text("en")
            await query.edit_message_text(t.common.error_user_not_found)
            return

        t = get_text(user.language)

        # Update default calendar preference
        await user_service.update_default_calendar(user, new_provider)
        await session.commit()

    provider_name = (
        t.settings.google_calendar_label
        if new_provider == "google"
        else t.settings.outlook_calendar_label
    )

    await query.edit_message_text(
        t.settings.default_calendar_updated.format(calendar=provider_name),
        parse_mode="Markdown",
    )


def setup_settings_handlers(app: Application) -> None:
    """Register settings handlers."""
    # Simple commands
    app.add_handler(CommandHandler("settings", settings_command))
    app.add_handler(CommandHandler("connect", connect_command))
    app.add_handler(CommandHandler("disconnect", disconnect_command))
    app.add_handler(CommandHandler("notifications", notifications_command))
    app.add_handler(CommandHandler("language", language_command))
    app.add_handler(CommandHandler("privacy", privacy_command))
    app.add_handler(CommandHandler("defaultcalendar", defaultcalendar_command))

    # Unified connect callbacks
    app.add_handler(CallbackQueryHandler(connect_google_callback, pattern=r"^connect_google$"))
    app.add_handler(CallbackQueryHandler(connect_outlook_callback, pattern=r"^connect_outlook$"))
    app.add_handler(CallbackQueryHandler(connect_zoom_callback, pattern=r"^connect_zoom$"))
    app.add_handler(CallbackQueryHandler(connect_back_callback, pattern=r"^connect_back$"))

    # Google mode selection
    app.add_handler(CallbackQueryHandler(google_mode_callback, pattern=r"^goog_(full|privacy)$"))

    # Outlook mode selection
    app.add_handler(CallbackQueryHandler(outlook_mode_callback, pattern=r"^outl_(full|privacy)$"))

    # Manage service callbacks
    app.add_handler(CallbackQueryHandler(manage_google_callback, pattern=r"^manage_google$"))
    app.add_handler(CallbackQueryHandler(manage_outlook_callback, pattern=r"^manage_outlook$"))
    app.add_handler(CallbackQueryHandler(manage_zoom_callback, pattern=r"^manage_zoom$"))

    # Disconnect callbacks
    app.add_handler(CallbackQueryHandler(disconnect_google_callback, pattern=r"^disc_google$"))
    app.add_handler(CallbackQueryHandler(disconnect_outlook_callback, pattern=r"^disc_outlook$"))
    app.add_handler(CallbackQueryHandler(disconnect_zoom_callback, pattern=r"^disc_zoom$"))

    # Notifications callback
    app.add_handler(CallbackQueryHandler(notifications_callback, pattern=r"^notif_"))

    # Language callback
    app.add_handler(CallbackQueryHandler(language_callback, pattern=r"^lang_"))

    # Privacy callback
    app.add_handler(CallbackQueryHandler(privacy_callback, pattern=r"^privacy_"))

    # Default calendar callback
    app.add_handler(CallbackQueryHandler(defaultcalendar_callback, pattern=r"^defcal_"))

    # Standalone timezone callback (handles tz_ buttons from OAuth and other contexts)
    # This must be registered BEFORE the ConversationHandler to catch callbacks
    # that happen outside the /timezone conversation
    app.add_handler(CallbackQueryHandler(timezone_callback_standalone, pattern=r"^tz_"))

    # Timezone conversation (for /timezone command flow)
    # Use MessageHandler(filters.COMMAND) as fallback to silently exit on any command
    tz_handler = ConversationHandler(
        entry_points=[CommandHandler("timezone", timezone_command)],
        states={
            AWAITING_TIMEZONE: [
                CallbackQueryHandler(timezone_callback, pattern=r"^tz_"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, timezone_text),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel_conversation),
            MessageHandler(filters.COMMAND, silent_cancel),
        ],
        allow_reentry=True,  # Allow /timezone to restart the conversation
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
        fallbacks=[
            CommandHandler("cancel", cancel_conversation),
            MessageHandler(filters.COMMAND, silent_cancel),
        ],
        allow_reentry=True,
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
        fallbacks=[
            CommandHandler("cancel", cancel_conversation),
            MessageHandler(filters.COMMAND, silent_cancel),
        ],
        allow_reentry=True,
    )
    app.add_handler(rem_handler)
