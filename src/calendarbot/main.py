"""Main application entry point."""

import asyncio
import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from telegram.ext import Application

from calendarbot.api.app import create_app
from calendarbot.bot.handlers import (
    setup_inline_handlers,
    setup_meeting_handlers,
    setup_settings_handlers,
    setup_start_handlers,
)
from calendarbot.config import get_settings
from calendarbot.db.session import init_db

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Reduce noise from httpx
logging.getLogger("httpx").setLevel(logging.WARNING)


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

    return app


async def run_bot_polling(app: Application) -> None:
    """Run bot in polling mode (development)."""
    logger.info("Starting bot in polling mode...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)

    logger.info("Bot is running. Press Ctrl+C to stop.")

    # Keep running until interrupted
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass
    finally:
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
    async def telegram_webhook(request):
        from telegram import Update
        import json

        data = await request.json()
        update = Update.de_json(data, app.bot)
        await app.process_update(update)
        return {"status": "ok"}

    await app.start()
    await app.bot.set_webhook(
        url=f"{settings.webhook_url}",
        allowed_updates=["message", "callback_query", "inline_query", "chosen_inline_result"],
    )

    logger.info(f"Webhook set to: {settings.webhook_url}")


async def main() -> None:
    """Main entry point."""
    settings = get_settings()

    logger.info(f"Starting CalendarBot in {settings.app_env} mode")

    # Initialize database
    await init_db()
    logger.info("Database initialized")

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
