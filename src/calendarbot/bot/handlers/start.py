"""Start and help command handlers."""

import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes

from calendarbot.bot.commands import set_user_commands
from calendarbot.db.repository import OAuthTokenRepository, PendingInviteRepository
from calendarbot.db.session import async_session_factory
from calendarbot.i18n import detect_language, get_text
from calendarbot.integrations.google import GoogleCalendarClient
from calendarbot.services.user import UserService
from calendarbot.utils.encryption import TokenEncryption
from calendarbot.utils.timezone import guess_timezone_from_language

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    if not update.effective_user or not update.message:
        return

    # Guess timezone from Telegram language setting
    guessed_timezone = guess_timezone_from_language(update.effective_user.language_code)
    # Detect language from Telegram settings
    detected_language = detect_language(update.effective_user.language_code)

    pending_invites_processed = []

    async with async_session_factory() as session:
        user_service = UserService(session)
        user, is_new = await user_service.get_or_create_user(
            telegram_id=update.effective_user.id,
            telegram_username=update.effective_user.username,
            timezone=guessed_timezone,
            language=detected_language,
        )
        await session.commit()

        # Get translations based on user's language
        user_lang = user.language if user else "en"
        t = get_text(user_lang)

        if is_new:
            logger.info(
                f"New user registered: {update.effective_user.id} "
                f"(lang={update.effective_user.language_code}, tz={guessed_timezone})"
            )
            # Inform user about detected timezone
            timezone_msg = f"\n\n{t.start.timezone_detected.format(timezone=guessed_timezone)}"
        else:
            timezone_msg = ""

        # Check for pending invites if user has a username
        if update.effective_user.username:
            pending_invites_processed = await _process_pending_invites(
                session, user.id, update.effective_user.username, t
            )
            await session.commit()

    # Set localized commands for this user
    await set_user_commands(context.bot, update.effective_user.id, user_lang)

    # Add Donate button
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(t.start.support_button, callback_data="donate_menu")]]
    )

    await update.message.reply_text(
        t.start.welcome_message + timezone_msg,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )

    # Notify user about processed pending invites
    if pending_invites_processed:
        invite_text = f"\n\n{t.start.pending_invites_found}\n\n"
        for invite_info in pending_invites_processed:
            invite_text += f"{t.start.pending_invite_notification.format(**invite_info)}\n\n"
        await update.message.reply_text(invite_text, parse_mode="Markdown")


async def _process_pending_invites(
    session, user_id: int, username: str, _t
) -> list[dict]:
    """Process pending invites for a user and send calendar invitations.

    Returns list of processed invite info for notification.
    """
    pending_repo = PendingInviteRepository(session)
    token_repo = OAuthTokenRepository(session)
    encryption = TokenEncryption()

    # Get pending invites for this username
    invites = await pending_repo.get_by_username(username)
    if not invites:
        return []

    # Get user's OAuth token to send invites
    token = await token_repo.get_token(user_id, "google")
    if not token:
        logger.info(f"User {user_id} has pending invites but no calendar connected")
        return []

    # Get user's email
    try:
        access_token = encryption.decrypt(token.access_token_encrypted)
        refresh_token = encryption.decrypt(token.refresh_token_encrypted)
        client = GoogleCalendarClient(
            access_token=access_token,
            refresh_token=refresh_token,
        )
        user_email = await client.get_user_email()
        if not user_email:
            logger.error(f"Could not get email for user {user_id}")
            return []
    except Exception as e:
        logger.error(f"Error getting email for user {user_id}: {e}")
        return []

    processed = []
    for invite in invites:
        try:
            # Add user as attendee to the existing meeting
            # Note: We can't directly add attendees to someone else's event,
            # but we can notify the user about the invitation
            processed.append({
                "title": invite.meeting_title,
                "time": invite.meeting_time.strftime("%H:%M on %d %b %Y"),
                "inviter": f"User #{invite.inviter_telegram_id}",
            })

            # Delete the processed invite
            await pending_repo.delete(invite)
            logger.info(
                f"Processed pending invite for @{username}: {invite.meeting_title}"
            )
        except Exception as e:
            logger.error(f"Error processing invite {invite.id}: {e}")

    return processed


async def help_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    if not update.message:
        return

    # Get user's language preference
    async with async_session_factory() as session:
        user_service = UserService(session)
        user = (
            await user_service.get_user(update.effective_user.id) if update.effective_user else None
        )
        user_lang = user.language if user else "en"

    t = get_text(user_lang)

    await update.message.reply_text(
        t.start.help_message,
        parse_mode="Markdown",
    )


def setup_start_handlers(app: Application) -> None:
    """Register start/help handlers."""
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
