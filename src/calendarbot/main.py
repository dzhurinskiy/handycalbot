"""Main application entry point."""

import asyncio
import logging

import uvicorn
from starlette.requests import Request
from telegram import BotCommandScopeAllPrivateChats, MenuButtonCommands
from telegram.ext import Application

from calendarbot.api.app import create_app
from calendarbot.bot.commands import get_bot_commands
from calendarbot.bot.handlers import (
    setup_donation_handlers,
    setup_feedback_handlers,
    setup_inline_handlers,
    setup_meeting_handlers,
    setup_settings_handlers,
    setup_start_handlers,
)
from calendarbot.config import get_settings
from calendarbot.db.session import init_db
from calendarbot.services.reminder import reminder_service

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Reduce noise from httpx
logging.getLogger("httpx").setLevel(logging.WARNING)


async def setup_bot_commands_and_menu(app: Application) -> None:
    """Set up bot commands and menu button for Telegram UI."""
    # Use English as default for global commands
    default_commands = get_bot_commands("en")

    try:
        # First, delete any existing commands to ensure clean state
        await app.bot.delete_my_commands()
        logger.info("Cleared existing bot commands")
    except Exception as e:
        logger.warning(f"Could not clear existing commands: {e}")

    try:
        # Set commands for all private chats (default scope) - English as fallback
        await app.bot.set_my_commands(default_commands)
        logger.info(f"Registered {len(default_commands)} bot commands (default scope)")

        # Also set for private chats scope explicitly
        await app.bot.set_my_commands(default_commands, scope=BotCommandScopeAllPrivateChats())
        logger.info("Registered bot commands for private chats scope")
    except Exception as e:
        logger.error(f"Failed to set bot commands: {e}")

    try:
        # Set menu button to show commands (for all users by default)
        await app.bot.set_chat_menu_button(menu_button=MenuButtonCommands())
        logger.info("Menu button set to show commands")
    except Exception as e:
        logger.error(f"Failed to set menu button: {e}")

    # Verify commands were set
    try:
        commands = await app.bot.get_my_commands()
        logger.info(f"Verified: {len(commands)} commands active")
    except Exception as e:
        logger.error(f"Failed to verify commands: {e}")


def create_bot_application() -> Application:
    """Create and configure the Telegram bot application."""
    settings = get_settings()

    # Create application
    app = Application.builder().token(settings.telegram_bot_token).build()

    # Register handlers
    setup_start_handlers(app)
    setup_settings_handlers(app)
    setup_meeting_handlers(app)
    setup_inline_handlers(app)
    setup_donation_handlers(app)
    setup_feedback_handlers(app)

    return app


async def run_bot_polling(app: Application) -> None:
    """Run bot in polling mode (development)."""
    logger.info("Starting bot in polling mode...")

    await app.initialize()
    await app.start()
    if app.updater:
        await app.updater.start_polling(drop_pending_updates=True)

    # Set bot commands and menu button for Telegram UI
    await setup_bot_commands_and_menu(app)

    logger.info("Bot is running. Press Ctrl+C to stop.")

    # Keep running until interrupted
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass
    finally:
        if app.updater:
            await app.updater.stop()
        await app.stop()
        await app.shutdown()


async def run_with_webhook(app: Application, fastapi_app) -> None:
    """Run bot with webhook (production)."""
    settings = get_settings()

    logger.info("Starting bot in webhook mode...")

    # Set up webhook
    await app.initialize()

    # Add webhook route to FastAPI
    @fastapi_app.post("/webhook")
    async def telegram_webhook(request: Request):
        from telegram import Update

        data = await request.json()
        update = Update.de_json(data, app.bot)
        await app.process_update(update)
        return {"status": "ok"}

    await app.start()
    await app.bot.set_webhook(
        url=f"{settings.webhook_url}",
        allowed_updates=[
            "message",
            "callback_query",
            "inline_query",
            "chosen_inline_result",
            "pre_checkout_query",
        ],
    )

    # Set bot commands and menu button for Telegram UI
    await setup_bot_commands_and_menu(app)

    logger.info(f"Webhook set to: {settings.webhook_url}")


async def main() -> None:
    """Main entry point."""
    settings = get_settings()

    logger.info(f"Starting CalendarBot in {settings.app_env} mode")

    # Initialize database
    await init_db()
    logger.info("Database initialized")

    # Start reminder scheduler (checks every minute)
    reminder_service.start(interval_seconds=60)
    logger.info("Reminder scheduler started")

    # Create applications
    bot_app = create_bot_application()
    fastapi_app = create_app()

    if settings.use_webhook:
        # Production: Run FastAPI with webhook
        await run_with_webhook(bot_app, fastapi_app)

        config = uvicorn.Config(
            fastapi_app,
            host=settings.app_host,
            port=settings.app_port,
            log_level=settings.log_level.lower(),
        )
        server = uvicorn.Server(config)
        await server.serve()
    else:
        # Development: Run polling + FastAPI in parallel
        async def run_api():
            config = uvicorn.Config(
                fastapi_app,
                host=settings.app_host,
                port=settings.app_port,
                log_level=settings.log_level.lower(),
            )
            server = uvicorn.Server(config)
            await server.serve()

        # Run both concurrently
        await asyncio.gather(
            run_bot_polling(bot_app),
            run_api(),
        )


def main_sync() -> None:
    """Synchronous entry point for console script."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...")


if __name__ == "__main__":
    main_sync()
