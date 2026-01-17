"""Internationalization module for CalendarBot."""

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from calendarbot.i18n.base import Translations


class Language(Enum):
    """Supported languages."""

    EN = "en"  # English
    ES = "es"  # Spanish
    FR = "fr"  # French
    DE = "de"  # German
    RU = "ru"  # Russian
    KO = "ko"  # Korean
    JA = "ja"  # Japanese
    ZH = "zh"  # Chinese


# Language display names (in their native language for UI)
LANGUAGE_NAMES = {
    "en": "English",
    "es": "Espanol",
    "fr": "Francais",
    "de": "Deutsch",
    "ru": "Russkij",
    "ko": "Hangugeo",
    "ja": "Nihongo",
    "zh": "Zhongwen",
}

# Mapping from Telegram language codes to our supported languages
TELEGRAM_LANGUAGE_MAP = {
    # English variants
    "en": "en",
    "en-US": "en",
    "en-GB": "en",
    # Spanish variants
    "es": "es",
    "es-ES": "es",
    "es-MX": "es",
    "es-AR": "es",
    # French variants
    "fr": "fr",
    "fr-FR": "fr",
    "fr-CA": "fr",
    # German variants
    "de": "de",
    "de-DE": "de",
    "de-AT": "de",
    "de-CH": "de",
    # Russian
    "ru": "ru",
    "ru-RU": "ru",
    # Korean
    "ko": "ko",
    "ko-KR": "ko",
    # Japanese
    "ja": "ja",
    "ja-JP": "ja",
    # Chinese variants
    "zh": "zh",
    "zh-CN": "zh",
    "zh-TW": "zh",
    "zh-HK": "zh",
}


def detect_language(telegram_language_code: str | None) -> str:
    """Detect user's preferred language from Telegram language code.

    Args:
        telegram_language_code: Language code from Telegram user object

    Returns:
        Supported language code (defaults to 'en' if not recognized)
    """
    if not telegram_language_code:
        return "en"

    # Direct match
    if telegram_language_code in TELEGRAM_LANGUAGE_MAP:
        return TELEGRAM_LANGUAGE_MAP[telegram_language_code]

    # Try base language (e.g., "pt-BR" -> "pt")
    base_lang = telegram_language_code.split("-")[0]
    if base_lang in TELEGRAM_LANGUAGE_MAP:
        return TELEGRAM_LANGUAGE_MAP[base_lang]

    # Default to English
    return "en"


def get_text(language: str = "en") -> "Translations":
    """Get translations for the specified language.

    Args:
        language: Language code (en, es, fr, de, ru, ko, ja, zh)

    Returns:
        Translations dataclass for the specified language
    """
    # Import translations lazily to avoid circular imports
    from calendarbot.i18n import de, en, es, fr, ja, ko, ru, zh

    translations = {
        "en": en.translations,
        "es": es.translations,
        "fr": fr.translations,
        "de": de.translations,
        "ru": ru.translations,
        "ko": ko.translations,
        "ja": ja.translations,
        "zh": zh.translations,
    }

    return translations.get(language, en.translations)


__all__ = [
    "Language",
    "LANGUAGE_NAMES",
    "detect_language",
    "get_text",
]
