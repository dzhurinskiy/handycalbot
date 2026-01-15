"""Application configuration using Pydantic Settings."""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Telegram
    telegram_bot_token: str

    # Database
    database_url: str = (
        "postgresql+asyncpg://calendarbot:calendarbot@localhost:5432/calendarbot"
    )

    # Google OAuth
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "https://164-92-157-14.nip.io/oauth/google/callback"

    # Security
    encryption_key: str = ""

    # Application
    app_env: Literal["development", "staging", "production"] = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    webhook_url: str = ""
    default_meeting_duration: int = 60  # minutes
    log_level: str = "INFO"

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def use_webhook(self) -> bool:
        return bool(self.webhook_url) and self.is_production


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
