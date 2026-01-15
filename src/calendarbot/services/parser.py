"""Command parser for inline meeting creation."""

import re
from dataclasses import dataclass
from datetime import datetime, timedelta

from calendarbot.utils.timezone import TimezoneHelper


@dataclass
class ParsedMeeting:
    """Parsed meeting data from inline command."""

    time: str  # HH:MM
    date: str | None  # DD-MM-YYYY or None
    title: str
    attendees: list[str]
    start_datetime: datetime  # Combined datetime in user's timezone
    end_datetime: datetime


class MeetingParser:
    """Parse inline meeting commands.

    Expected formats:
        14:30 25-01-2026 "Project Sync" john@example.com, jane@example.com
        10:00 "Daily Standup"
        16:00 "Quick Call"
    """

    # Regex patterns
    TIME_PATTERN = r"(\d{1,2}:\d{2})"
    DATE_PATTERN = r"(\d{1,2}-\d{1,2}-\d{4})"
    TITLE_PATTERN = r'"([^"]+)"'
    EMAIL_PATTERN = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    def __init__(self, user_timezone: str = "UTC", default_duration: int = 60):
        self.user_timezone = user_timezone
        self.default_duration = default_duration

    def parse(self, text: str) -> ParsedMeeting | None:
        """Parse inline command text into MeetingData.

        Returns None if parsing fails.
        """
        text = text.strip()

        # Extract time (required)
        time_match = re.search(self.TIME_PATTERN, text)
        if not time_match:
            return None
        time_str = time_match.group(1)

        # Extract date (optional)
        date_match = re.search(self.DATE_PATTERN, text)
        date_str = date_match.group(1) if date_match else None

        # Extract title (required)
        title_match = re.search(self.TITLE_PATTERN, text)
        if not title_match:
            return None
        title = title_match.group(1)

        # Extract emails (optional)
        # Find all text after the title
        title_end = title_match.end()
        remaining_text = text[title_end:]
        attendees = re.findall(self.EMAIL_PATTERN, remaining_text)

        # Build datetime
        try:
            start_datetime = self._build_datetime(time_str, date_str)
            end_datetime = start_datetime + timedelta(minutes=self.default_duration)
        except ValueError:
            return None

        return ParsedMeeting(
            time=time_str,
            date=date_str,
            title=title,
            attendees=attendees,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )

    def _build_datetime(self, time_str: str, date_str: str | None) -> datetime:
        """Build datetime from time and optional date."""
        # Parse time
        hour, minute = map(int, time_str.split(":"))
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError("Invalid time")

        # Get current date in user's timezone if not provided
        if date_str:
            day, month, year = map(int, date_str.split("-"))
            dt = datetime(year, month, day, hour, minute)
        else:
            now = TimezoneHelper.now_in_tz(self.user_timezone)
            dt = datetime(now.year, now.month, now.day, hour, minute)

        return dt

    def format_preview(self, meeting: ParsedMeeting) -> str:
        """Format meeting for inline preview."""
        date_display = meeting.start_datetime.strftime("%d %b %Y")
        time_display = meeting.start_datetime.strftime("%H:%M")

        text = f"📅 {meeting.title}\n"
        text += f"🕐 {time_display} on {date_display}\n"
        text += f"⏱️ Duration: {self.default_duration} min\n"

        if meeting.attendees:
            text += f"👥 Attendees: {', '.join(meeting.attendees)}"
        else:
            text += "👤 No attendees (private event)"

        return text

    def validate_emails(self, emails: list[str]) -> tuple[list[str], list[str]]:
        """Validate email list. Returns (valid, invalid)."""
        valid = []
        invalid = []

        email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

        for email in emails:
            email = email.strip().lower()
            if email_regex.match(email):
                valid.append(email)
            else:
                invalid.append(email)

        return valid, invalid
