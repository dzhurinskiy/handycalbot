"""Proactive token refresh service.

This service runs in the background to keep OAuth tokens fresh for all users,
even if they don't use the bot frequently. This prevents token expiration issues
for inactive users.
"""

import asyncio
import contextlib
import logging

from calendarbot.db.models import User
from calendarbot.db.repository import OAuthTokenRepository
from calendarbot.db.session import async_session_factory
from calendarbot.integrations.google import GoogleCalendarClient
from calendarbot.integrations.zoom import ZoomClient
from calendarbot.utils.encryption import TokenEncryption

logger = logging.getLogger(__name__)


class TokenRefreshService:
    """Service to proactively refresh OAuth tokens before they expire."""

    def __init__(self):
        self._running = False
        self._task: asyncio.Task | None = None
        self.encryption = TokenEncryption()

    async def refresh_google_token(
        self,
        token_repo: OAuthTokenRepository,
        user_id: int,
        access_token: str,
        refresh_token: str,
    ) -> dict | None:
        """Attempt to refresh a Google OAuth token.

        Returns new token data on success, None on failure.
        """
        client = GoogleCalendarClient(
            access_token=access_token,
            refresh_token=refresh_token,
        )

        new_tokens = await client.refresh_access_token()
        if new_tokens:
            # Save the refreshed token
            await token_repo.save_token(
                user_id=user_id,
                provider="google",
                access_token_encrypted=self.encryption.encrypt(new_tokens["access_token"]),
                refresh_token_encrypted=self.encryption.encrypt(
                    new_tokens.get("refresh_token") or refresh_token
                ),
                expires_at=new_tokens["expires_at"],
            )
            return new_tokens

        return None

    async def refresh_zoom_token(
        self,
        token_repo: OAuthTokenRepository,
        user_id: int,
        access_token: str,
        refresh_token: str,
    ) -> dict | None:
        """Attempt to refresh a Zoom OAuth token.

        Returns new token data on success, None on failure.
        """
        client = ZoomClient(
            access_token=access_token,
            refresh_token=refresh_token,
        )

        new_tokens = await client.refresh_access_token()
        if new_tokens:
            # Save the refreshed token
            await token_repo.save_token(
                user_id=user_id,
                provider="zoom",
                access_token_encrypted=self.encryption.encrypt(new_tokens["access_token"]),
                refresh_token_encrypted=self.encryption.encrypt(
                    new_tokens.get("refresh_token") or refresh_token
                ),
                expires_at=new_tokens["expires_at"],
            )
            return new_tokens

        return None

    async def refresh_expiring_tokens(self) -> dict[str, int]:
        """Refresh all tokens that are expiring soon.

        Returns dict with counts: {"google_refreshed": N, "google_failed": N, ...}
        """
        stats = {
            "google_refreshed": 0,
            "google_failed": 0,
            "zoom_refreshed": 0,
            "zoom_failed": 0,
        }

        try:
            async with async_session_factory() as session:
                token_repo = OAuthTokenRepository(session)

                # Refresh tokens expiring within 12 hours
                # (Google tokens last 1 hour, so 12 hours gives plenty of buffer)
                hours_threshold = 12

                # Process Google tokens
                google_tokens = await token_repo.get_tokens_expiring_soon(
                    provider="google", hours_before=hours_threshold
                )

                for token in google_tokens:
                    try:
                        access_token = self.encryption.decrypt(token.access_token_encrypted)
                        refresh_token = self.encryption.decrypt(token.refresh_token_encrypted)

                        # Get user for logging
                        user = await session.get(User, token.user_id)
                        user_info = f"user_id={token.user_id}"
                        if user:
                            user_info = f"telegram_id={user.telegram_id}"

                        result = await self.refresh_google_token(
                            token_repo, token.user_id, access_token, refresh_token
                        )

                        if result:
                            logger.info(f"Proactively refreshed Google token for {user_info}")
                            stats["google_refreshed"] += 1
                        else:
                            logger.warning(
                                f"Failed to refresh Google token for {user_info} - "
                                "token may be revoked"
                            )
                            stats["google_failed"] += 1

                    except Exception as e:
                        logger.error(f"Error refreshing Google token for user {token.user_id}: {e}")
                        stats["google_failed"] += 1

                # Process Zoom tokens
                zoom_tokens = await token_repo.get_tokens_expiring_soon(
                    provider="zoom", hours_before=hours_threshold
                )

                for token in zoom_tokens:
                    try:
                        access_token = self.encryption.decrypt(token.access_token_encrypted)
                        refresh_token = self.encryption.decrypt(token.refresh_token_encrypted)

                        user = await session.get(User, token.user_id)
                        user_info = f"user_id={token.user_id}"
                        if user:
                            user_info = f"telegram_id={user.telegram_id}"

                        result = await self.refresh_zoom_token(
                            token_repo, token.user_id, access_token, refresh_token
                        )

                        if result:
                            logger.info(f"Proactively refreshed Zoom token for {user_info}")
                            stats["zoom_refreshed"] += 1
                        else:
                            logger.warning(
                                f"Failed to refresh Zoom token for {user_info} - "
                                "token may be revoked"
                            )
                            stats["zoom_failed"] += 1

                    except Exception as e:
                        logger.error(f"Error refreshing Zoom token for user {token.user_id}: {e}")
                        stats["zoom_failed"] += 1

                await session.commit()

        except Exception as e:
            logger.exception(f"Error in token refresh cycle: {e}")

        return stats

    async def _scheduler_loop(self, interval_seconds: int = 3600):
        """Background loop that refreshes tokens periodically.

        Default interval is 1 hour (3600 seconds).
        """
        logger.info(f"Token refresh scheduler started (interval: {interval_seconds}s)")

        while self._running:
            try:
                stats = await self.refresh_expiring_tokens()

                # Only log if there was activity
                total_refreshed = stats["google_refreshed"] + stats["zoom_refreshed"]
                total_failed = stats["google_failed"] + stats["zoom_failed"]

                if total_refreshed > 0 or total_failed > 0:
                    logger.info(
                        f"Token refresh cycle: "
                        f"Google ({stats['google_refreshed']} OK, {stats['google_failed']} failed), "
                        f"Zoom ({stats['zoom_refreshed']} OK, {stats['zoom_failed']} failed)"
                    )

            except Exception as e:
                logger.exception(f"Error in token refresh scheduler: {e}")

            await asyncio.sleep(interval_seconds)

        logger.info("Token refresh scheduler stopped")

    def start(self, interval_seconds: int = 3600):
        """Start the token refresh scheduler as a background task.

        Args:
            interval_seconds: How often to check for expiring tokens (default: 1 hour)
        """
        if self._running:
            logger.warning("Token refresh scheduler already running")
            return

        self._running = True
        self._task = asyncio.create_task(self._scheduler_loop(interval_seconds))
        logger.info("Token refresh scheduler task created")

    async def stop(self):
        """Stop the token refresh scheduler."""
        if not self._running:
            return

        self._running = False
        if self._task:
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task
            self._task = None
        logger.info("Token refresh scheduler stopped")


# Global instance for the application
token_refresh_service = TokenRefreshService()
