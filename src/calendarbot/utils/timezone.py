"""Timezone utilities."""

from datetime import datetime
from zoneinfo import ZoneInfo

import pytz


# Map Telegram language codes to likely timezones
LANGUAGE_TO_TIMEZONE: dict[str, str] = {
    "ru": "Europe/Moscow",
    "uk": "Europe/Kiev",
    "be": "Europe/Minsk",
    "kk": "Asia/Almaty",
    "uz": "Asia/Tashkent",
    "en": "America/New_York",  # Default for English
    "de": "Europe/Berlin",
    "fr": "Europe/Paris",
    "es": "Europe/Madrid",
    "it": "Europe/Rome",
    "pt": "Europe/Lisbon",
    "pl": "Europe/Warsaw",
    "nl": "Europe/Amsterdam",
    "tr": "Europe/Istanbul",
    "ar": "Asia/Riyadh",
    "fa": "Asia/Tehran",
    "he": "Asia/Jerusalem",
    "ja": "Asia/Tokyo",
    "ko": "Asia/Seoul",
    "zh": "Asia/Shanghai",
    "hi": "Asia/Kolkata",
    "th": "Asia/Bangkok",
    "vi": "Asia/Ho_Chi_Minh",
    "id": "Asia/Jakarta",
}


def guess_timezone_from_language(language_code: str | None) -> str:
    """Guess timezone from Telegram language code.

    Returns best guess timezone or 'UTC' if unknown.
    """
    if not language_code:
        return "UTC"

    # Handle language codes like "en-US", "ru-RU"
    lang = language_code.split("-")[0].lower()

    return LANGUAGE_TO_TIMEZONE.get(lang, "UTC")


class TimezoneHelper:
    """Helper for timezone conversions."""

    # Common timezone aliases
    TIMEZONE_ALIASES: dict[str, str] = {
        "PST": "America/Los_Angeles",
        "PDT": "America/Los_Angeles",
        "MST": "America/Denver",
        "MDT": "America/Denver",
        "CST": "America/Chicago",
        "CDT": "America/Chicago",
        "EST": "America/New_York",
        "EDT": "America/New_York",
        "GMT": "Europe/London",
        "BST": "Europe/London",
        "CET": "Europe/Paris",
        "CEST": "Europe/Paris",
        "MSK": "Europe/Moscow",
    }

    @classmethod
    def get_timezone(cls, tz_name: str) -> ZoneInfo:
        """Get timezone by name or alias."""
        # Check aliases first
        tz_name = cls.TIMEZONE_ALIASES.get(tz_name.upper(), tz_name)
        return ZoneInfo(tz_name)

    @classmethod
    def is_valid_timezone(cls, tz_name: str) -> bool:
        """Check if timezone name is valid."""
        try:
            cls.get_timezone(tz_name)
            return True
        except Exception:
            return False

    @classmethod
    def to_utc(cls, dt: datetime, from_tz: str) -> datetime:
        """Convert datetime from given timezone to UTC."""
        tz = cls.get_timezone(from_tz)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=tz)
        return dt.astimezone(ZoneInfo("UTC"))

    @classmethod
    def from_utc(cls, dt: datetime, to_tz: str) -> datetime:
        """Convert datetime from UTC to given timezone."""
        tz = cls.get_timezone(to_tz)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo("UTC"))
        return dt.astimezone(tz)

    @classmethod
    def now_in_tz(cls, tz_name: str) -> datetime:
        """Get current time in specified timezone."""
        tz = cls.get_timezone(tz_name)
        return datetime.now(tz)

    @classmethod
    def get_common_timezones(cls) -> list[str]:
        """Get list of common timezones for user selection."""
        return [
            "UTC",
            "Europe/London",
            "Europe/Paris",
            "Europe/Berlin",
            "Europe/Moscow",
            "Asia/Dubai",
            "Asia/Kolkata",
            "Asia/Singapore",
            "Asia/Tokyo",
            "Australia/Sydney",
            "Pacific/Auckland",
            "America/New_York",
            "America/Chicago",
            "America/Denver",
            "America/Los_Angeles",
        ]
