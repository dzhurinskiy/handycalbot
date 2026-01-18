"""Bot command handlers."""

from calendarbot.bot.handlers.donation import setup_donation_handlers
from calendarbot.bot.handlers.edit_session import setup_edit_session_handlers
from calendarbot.bot.handlers.feedback import setup_feedback_handlers
from calendarbot.bot.handlers.inline import setup_inline_handlers
from calendarbot.bot.handlers.meetings import setup_meeting_handlers
from calendarbot.bot.handlers.settings import setup_settings_handlers
from calendarbot.bot.handlers.start import setup_start_handlers

__all__ = [
    "setup_start_handlers",
    "setup_settings_handlers",
    "setup_meeting_handlers",
    "setup_inline_handlers",
    "setup_edit_session_handlers",
    "setup_donation_handlers",
    "setup_feedback_handlers",
]
