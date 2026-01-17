"""Reminder notification service."""

import asyncio
import contextlib
import logging
from datetime import datetime, timedelta

import httpx

from calendarbot.config import get_settings
from calendarbot.db.models import Meeting, User
from calendarbot.db.repository import MeetingRepository
from calendarbot.db.session import async_session_factory
from calendarbot.i18n import get_text

logger = logging.getLogger(__name__)


class ReminderService:
    """Service to send meeting reminders via Telegram."""

    def __init__(self):
        self.settings = get_settings()
        self._running = False
        self._task: asyncio.Task | None = None

    async def send_telegram_message(self, chat_id: int, text: str) -> bool:
        """Send a message to a Telegram user."""
        url = f"https://api.telegram.org/bot{self.settings.telegram_bot_token}/sendMessage"

        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown",
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=10.0)
                if response.status_code != 200:
                    logger.error(f"Failed to send reminder: {response.text}")
                    return False
                return True
        except Exception as e:
            logger.error(f"Error sending reminder: {e}")
            return False

    def _escape_markdown(self, text: str) -> str:
        """Escape special Markdown characters in text."""
        # Escape characters that have special meaning in Telegram Markdown
        special_chars = ["*", "_", "`", "["]
        for char in special_chars:
            text = text.replace(char, f"\\{char}")
        return text

    def _format_reminder_message(
        self, meeting: Meeting, minutes_before: int, user_timezone: str, user_language: str
    ) -> str:
        """Format the reminder notification message."""
        # Convert UTC time to user's timezone for display
        # meeting.start_time is stored as naive UTC
        from zoneinfo import ZoneInfo

        from calendarbot.utils.timezone import TimezoneHelper

        t = get_text(user_language)

        start_utc = meeting.start_time.replace(tzinfo=ZoneInfo("UTC"))
        start_local = TimezoneHelper.from_utc(start_utc, user_timezone)

        time_str = start_local.strftime("%H:%M")
        date_str = start_local.strftime("%d %b %Y")

        # Format the "time until" part
        if minutes_before >= 1440:
            days = minutes_before // 1440
            time_until = f"{days} {t.settings.days}" if days > 1 else f"{days} {t.settings.day}"
        elif minutes_before >= 60:
            hours = minutes_before // 60
            time_until = (
                f"{hours} {t.settings.hours}" if hours > 1 else f"{hours} {t.settings.hour}"
            )
        else:
            time_until = f"{minutes_before} {t.settings.minutes}"

        # Escape special characters in meeting title to avoid Markdown parsing errors
        safe_title = self._escape_markdown(meeting.title)

        text = f"{t.reminder.meeting_reminder}\n\n"
        text += f"*{safe_title}*\n"
        text += f"🕐 {time_str} on {date_str}\n"
        text += f"⏰ {t.reminder.starting_in.format(time=time_until)}"

        # Add attendees if any
        if meeting.attendees and meeting.attendees.get("emails"):
            emails = meeting.attendees["emails"]
            if emails:
                text += f"\n\n👥 {', '.join(emails)}"

        return text

    async def check_and_send_reminders(self) -> int:
        """Check for pending reminders and send notifications.

        Returns the number of reminders sent.
        """
        sent_count = 0
        now = datetime.utcnow()

        try:
            async with async_session_factory() as session:
                meeting_repo = MeetingRepository(session)

                # Get all meetings with reminders
                meetings = await meeting_repo.get_meetings_with_pending_reminders(now)

                for meeting in meetings:
                    # Get user to check if notifications are enabled
                    user = await session.get(User, meeting.user_id)
                    if not user or not user.notifications_enabled:
                        continue

                    # Skip meetings without reminders (shouldn't happen but be safe)
                    if not meeting.reminders:
                        continue

                    # Parse reminders
                    reminder_minutes = [int(r) for r in meeting.reminders.split(",")]
                    sent_minutes = set()
                    if meeting.reminders_sent:
                        sent_minutes = {int(r) for r in meeting.reminders_sent.split(",")}

                    # Check each reminder
                    for minutes in reminder_minutes:
                        if minutes in sent_minutes:
                            continue  # Already sent

                        # Calculate when this reminder should fire
                        reminder_time = meeting.start_time - timedelta(minutes=minutes)

                        # If reminder time has passed, send it
                        if now >= reminder_time:
                            logger.info(
                                f"Sending {minutes}min reminder for meeting {meeting.id} "
                                f"to user {user.telegram_id}"
                            )

                            message = self._format_reminder_message(
                                meeting, minutes, user.timezone, user.language
                            )
                            success = await self.send_telegram_message(user.telegram_id, message)

                            if success:
                                await meeting_repo.mark_reminder_sent(meeting.id, minutes)
                                sent_count += 1
                            else:
                                logger.error(f"Failed to send reminder for meeting {meeting.id}")

                await session.commit()

        except Exception as e:
            logger.exception(f"Error in reminder check: {e}")

        return sent_count

    async def _scheduler_loop(self, interval_seconds: int = 60):
        """Background loop that checks for reminders periodically."""
        logger.info(f"Reminder scheduler started (interval: {interval_seconds}s)")

        while self._running:
            try:
                sent = await self.check_and_send_reminders()
                if sent > 0:
                    logger.info(f"Sent {sent} reminder(s)")
            except Exception as e:
                logger.exception(f"Error in reminder scheduler: {e}")

            await asyncio.sleep(interval_seconds)

        logger.info("Reminder scheduler stopped")

    def start(self, interval_seconds: int = 60):
        """Start the reminder scheduler as a background task."""
        if self._running:
            logger.warning("Reminder scheduler already running")
            return

        self._running = True
        self._task = asyncio.create_task(self._scheduler_loop(interval_seconds))
        logger.info("Reminder scheduler task created")

    async def stop(self):
        """Stop the reminder scheduler."""
        if not self._running:
            return

        self._running = False
        if self._task:
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task
            self._task = None
        logger.info("Reminder scheduler stopped")


# Global instance for the application
reminder_service = ReminderService()
