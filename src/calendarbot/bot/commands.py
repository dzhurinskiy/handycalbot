"""Bot commands utilities for localized command descriptions."""

import logging

from telegram import Bot, BotCommand, BotCommandScopeChat

from calendarbot.i18n import get_text

logger = logging.getLogger(__name__)


def get_bot_commands(language: str = "en") -> list[BotCommand]:
    """Get localized bot commands for a specific language."""
    t = get_text(language)
    return [
        BotCommand("start", t.commands.start),
        BotCommand("help", t.commands.help),
        BotCommand("meetings", t.commands.meetings),
        BotCommand("cancel", t.commands.cancel),
        BotCommand("connect", t.commands.connect),
        BotCommand("disconnect", t.commands.disconnect),
        BotCommand("connectzoom", t.commands.connectzoom),
        BotCommand("disconnectzoom", t.commands.disconnectzoom),
        BotCommand("settings", t.commands.settings),
        BotCommand("timezone", t.commands.timezone),
        BotCommand("duration", t.commands.duration),
        BotCommand("reminder", t.commands.reminder),
        BotCommand("notifications", t.commands.notifications),
        BotCommand("privacy", t.commands.privacy),
        BotCommand("language", t.commands.language),
        BotCommand("donate", t.commands.donate),
        BotCommand("feedback", t.commands.feedback),
    ]


async def set_user_commands(bot: Bot, user_id: int, language: str) -> None:
    """Set localized commands for a specific user."""
    try:
        commands = get_bot_commands(language)
        await bot.set_my_commands(commands, scope=BotCommandScopeChat(chat_id=user_id))
    except Exception as e:
        logger.warning(f"Failed to set commands for user {user_id}: {e}")
