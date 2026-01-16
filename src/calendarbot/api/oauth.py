"""OAuth callback endpoints."""

import logging

import httpx
from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse

from calendarbot.config import get_settings
from calendarbot.db.repository import OAuthTokenRepository, UserRepository
from calendarbot.db.session import async_session_factory
from calendarbot.integrations.google import GoogleOAuthFlow
from calendarbot.utils.encryption import TokenEncryption

logger = logging.getLogger(__name__)


async def send_telegram_message(chat_id: int, text: str, reply_markup: dict | None = None) -> bool:
    """Send a message to a Telegram user via Bot API."""
    settings = get_settings()
    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10.0)
            return response.status_code == 200
    except Exception as e:
        logger.error(f"Failed to send Telegram message: {e}")
        return False


router = APIRouter(tags=["oauth"])


SUCCESS_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>CalendarBot - Connected!</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .card {
            background: white;
            padding: 3rem;
            border-radius: 1rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            text-align: center;
            max-width: 400px;
        }
        .icon {
            font-size: 4rem;
            margin-bottom: 1rem;
        }
        h1 {
            color: #1a202c;
            margin-bottom: 0.5rem;
        }
        p {
            color: #718096;
            margin-bottom: 1.5rem;
        }
        .close-hint {
            font-size: 0.875rem;
            color: #a0aec0;
        }
    </style>
</head>
<body>
    <div class="card">
        <div class="icon">✅</div>
        <h1>Connected!</h1>
        <p>Your Google Calendar is now linked to HandyCalBot.</p>
        <p class="close-hint">You can close this window and return to Telegram.</p>
    </div>
</body>
</html>
"""

ERROR_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>CalendarBot - Error</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #f56565 0%, #c53030 100%);
        }
        .card {
            background: white;
            padding: 3rem;
            border-radius: 1rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            text-align: center;
            max-width: 400px;
        }
        .icon {
            font-size: 4rem;
            margin-bottom: 1rem;
        }
        h1 {
            color: #1a202c;
            margin-bottom: 0.5rem;
        }
        p {
            color: #718096;
        }
        .error-detail {
            background: #fed7d7;
            color: #c53030;
            padding: 1rem;
            border-radius: 0.5rem;
            margin-top: 1rem;
            font-family: monospace;
            font-size: 0.875rem;
        }
    </style>
</head>
<body>
    <div class="card">
        <div class="icon">❌</div>
        <h1>Connection Failed</h1>
        <p>Could not connect your Google Calendar.</p>
        <div class="error-detail">{error}</div>
        <p style="margin-top: 1.5rem;">Please try again with /connect in Telegram.</p>
    </div>
</body>
</html>
"""


@router.get("/google/callback")
async def google_oauth_callback(
    code: str = Query(None),
    state: str = Query(None),
    error: str = Query(None),
) -> HTMLResponse:
    """Handle Google OAuth callback."""
    # Check for errors from Google
    if error:
        logger.error(f"Google OAuth error: {error}")
        return HTMLResponse(content=ERROR_HTML.format(error=error), status_code=400)

    if not code or not state:
        return HTMLResponse(
            content=ERROR_HTML.format(error="Missing code or state"),
            status_code=400,
        )

    # Parse state to get telegram user ID
    try:
        telegram_id_str, _ = state.split(":", 1)
        telegram_id = int(telegram_id_str)
    except (ValueError, AttributeError):
        return HTMLResponse(
            content=ERROR_HTML.format(error="Invalid state parameter"),
            status_code=400,
        )

    # Exchange code for tokens
    oauth = GoogleOAuthFlow()
    tokens = await oauth.exchange_code(code)

    if not tokens:
        return HTMLResponse(
            content=ERROR_HTML.format(error="Failed to exchange authorization code"),
            status_code=400,
        )

    # Save tokens to database
    try:
        encryption = TokenEncryption()

        async with async_session_factory() as session:
            user_repo = UserRepository(session)
            token_repo = OAuthTokenRepository(session)

            user = await user_repo.get_by_telegram_id(telegram_id)
            if not user:
                return HTMLResponse(
                    content=ERROR_HTML.format(error="User not found. Please /start the bot first."),
                    status_code=400,
                )

            await token_repo.save_token(
                user_id=user.id,
                provider="google",
                access_token_encrypted=encryption.encrypt(tokens["access_token"]),
                refresh_token_encrypted=encryption.encrypt(tokens["refresh_token"]),
                expires_at=tokens["expires_at"],
                calendar_id="primary",
            )
            await session.commit()

            # Get user's current timezone for the message
            user_timezone = user.timezone

        logger.info(f"Google Calendar connected for user {telegram_id}")

        # Send timezone confirmation message to user
        timezone_message = (
            "✅ *Google Calendar connected successfully!*\n\n"
            f"📍 Your current timezone is set to: `{user_timezone}`\n\n"
            "Please confirm this is correct, or choose a different timezone.\n"
            "_Correct timezone is important for scheduling meetings at the right time._"
        )

        # Build inline keyboard with timezone options
        from calendarbot.utils.timezone import TimezoneHelper

        common_tzs = TimezoneHelper.get_common_timezones()[:8]  # Top 8 timezones

        keyboard_rows = []
        row = []
        for tz in common_tzs:
            label = f"✓ {tz}" if tz == user_timezone else tz
            row.append({"text": label, "callback_data": f"tz_{tz}"})
            if len(row) == 2:
                keyboard_rows.append(row)
                row = []
        if row:
            keyboard_rows.append(row)

        # Add "Keep current" button
        keyboard_rows.append(
            [{"text": f"✅ Keep {user_timezone}", "callback_data": f"tz_{user_timezone}"}]
        )

        reply_markup = {"inline_keyboard": keyboard_rows}

        await send_telegram_message(telegram_id, timezone_message, reply_markup)

        return HTMLResponse(content=SUCCESS_HTML)

    except Exception as e:
        logger.exception("Error saving OAuth tokens")
        return HTMLResponse(
            content=ERROR_HTML.format(error=str(e)),
            status_code=500,
        )
