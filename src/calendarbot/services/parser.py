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
    # Reminders in minutes before meeting, None means no reminder, empty list means use default
    reminders: list[int] | None = None
    use_default_reminder: bool = False  # True if 'r' was specified without values


class MeetingParser:
    """Parse inline meeting commands.

    Expected formats:
        14:30 25-01-2026 "Project Sync" john@example.com, jane@example.com
        10:00 "Daily Standup"
        16:00 "Quick Call"
        14:30 "Meeting" r 10m          # 10 min reminder
        14:30 "Meeting" r 10m/30m      # 10 and 30 min reminders
        14:30 "Meeting" r              # use default reminder
    """

    # Regex patterns
    TIME_PATTERN = r"(\d{1,2}:\d{2})"
    DATE_PATTERN = r"(\d{1,2}-\d{1,2}-\d{4})"
    TITLE_PATTERN = r'"([^"]+)"'
    EMAIL_PATTERN = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    # Reminder pattern: r followed by optional time values like 10m, 30m/60m, 1d
    REMINDER_PATTERN = r"\br\s*((?:\d+[mhd](?:/\d+[mhd])*)?)\b"

    # Various quote characters to normalize (Russian, curly, single, guillemets, etc.)
    # iPhone and other devices may use any of these instead of standard double quotes
    QUOTE_CHARS = [
        # Curly/smart double quotes (most common on iPhone)
        '"',  # U+201C LEFT DOUBLE QUOTATION MARK
        '"',  # U+201D RIGHT DOUBLE QUOTATION MARK
        # Russian/French guillemets
        "«",  # U+00AB LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
        "»",  # U+00BB RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
        # German-style quotes
        "„",  # U+201E DOUBLE LOW-9 QUOTATION MARK
        "‟",  # U+201F DOUBLE HIGH-REVERSED-9 QUOTATION MARK
        # Curly single quotes (when used for titles)
        "'",  # U+2018 LEFT SINGLE QUOTATION MARK
        "'",  # U+2019 RIGHT SINGLE QUOTATION MARK
        # Single guillemets
        "‹",  # U+2039 SINGLE LEFT-POINTING ANGLE QUOTATION MARK
        "›",  # U+203A SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
        # CJK quotes
        "「",  # U+300C LEFT CORNER BRACKET
        "」",  # U+300D RIGHT CORNER BRACKET
        "『",  # U+300E LEFT WHITE CORNER BRACKET
        "』",  # U+300F RIGHT WHITE CORNER BRACKET
        # Low single quotes
        "‚",  # U+201A SINGLE LOW-9 QUOTATION MARK
        # Straight single quote (ASCII)
        "'",  # U+0027 APOSTROPHE
        # Prime characters (often mistaken for quotes)
        "′",  # U+2032 PRIME
        "″",  # U+2033 DOUBLE PRIME
        # Fullwidth characters (CJK input methods)
        "＂",  # U+FF02 FULLWIDTH QUOTATION MARK
        "＇",  # U+FF07 FULLWIDTH APOSTROPHE
        # Modifier letters sometimes used as quotes
        "ˮ",  # U+02EE MODIFIER LETTER DOUBLE APOSTROPHE
        # Grave accent (backtick) - sometimes used as quote
        "`",  # U+0060 GRAVE ACCENT
        "ˋ",  # U+02CB MODIFIER LETTER GRAVE ACCENT
        "｀",  # U+FF40 FULLWIDTH GRAVE ACCENT
        # Heavy quotes
        "❝",  # U+275D HEAVY DOUBLE TURNED COMMA QUOTATION MARK ORNAMENT
        "❞",  # U+275E HEAVY DOUBLE COMMA QUOTATION MARK ORNAMENT
        "❮",  # U+276E HEAVY LEFT-POINTING ANGLE QUOTATION MARK ORNAMENT
        "❯",  # U+276F HEAVY RIGHT-POINTING ANGLE QUOTATION MARK ORNAMENT
    ]

    def __init__(self, user_timezone: str = "UTC", default_duration: int = 60):
        self.user_timezone = user_timezone
        self.default_duration = default_duration

    def _normalize_quotes(self, text: str) -> str:
        """Normalize various quote characters to standard double quotes."""
        for quote_char in self.QUOTE_CHARS:
            text = text.replace(quote_char, '"')
        return text

    def parse(self, text: str) -> ParsedMeeting | None:
        """Parse inline command text into MeetingData.

        Returns None if parsing fails.
        """
        text = text.strip()

        # Normalize various quote characters to standard double quotes
        text = self._normalize_quotes(text)

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

        # Extract reminder (optional) - parse before emails to avoid confusion
        reminder_match = re.search(self.REMINDER_PATTERN, text)
        reminders = None
        use_default_reminder = False
        if reminder_match:
            reminder_str = reminder_match.group(1).strip()
            if reminder_str:
                # Parse reminder values like "10m", "30m/60m", "1d"
                reminders = self._parse_reminders(reminder_str)
            else:
                # Just "r" without values - use default
                use_default_reminder = True

        # Extract emails (optional)
        # Find all text after the title, excluding the reminder part
        title_end = title_match.end()
        remaining_text = text[title_end:]
        # Remove reminder pattern from remaining text before extracting emails
        remaining_text = re.sub(self.REMINDER_PATTERN, "", remaining_text)
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
            reminders=reminders,
            use_default_reminder=use_default_reminder,
        )

    def _parse_reminders(self, reminder_str: str) -> list[int] | None:
        """Parse reminder string like '10m', '30m/60m', '1d' into minutes."""
        reminders = []
        parts = reminder_str.split("/")
        for part in parts:
            part = part.strip().lower()
            if not part:
                continue
            # Extract number and unit
            match = re.match(r"(\d+)([mhd])", part)
            if match:
                value = int(match.group(1))
                unit = match.group(2)
                if unit == "m":
                    reminders.append(value)
                elif unit == "h":
                    reminders.append(value * 60)
                elif unit == "d":
                    reminders.append(value * 60 * 24)
        return reminders if reminders else None

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

    def format_preview(self, meeting: ParsedMeeting, default_reminder: str | None = None) -> str:
        """Format meeting for inline preview."""
        date_display = meeting.start_datetime.strftime("%d %b %Y")
        time_display = meeting.start_datetime.strftime("%H:%M")

        text = f"📅 {meeting.title}\n"
        text += f"🕐 {time_display} on {date_display}\n"
        text += f"⏱️ Duration: {self.default_duration} min\n"

        # Show reminder info
        reminder_text = self._format_reminder_preview(meeting, default_reminder)
        if reminder_text:
            text += f"🔔 {reminder_text}\n"

        if meeting.attendees:
            text += f"👥 Attendees: {', '.join(meeting.attendees)}"
        else:
            text += "👤 No attendees (private event)"

        return text

    def _format_reminder_preview(self, meeting: ParsedMeeting, default_reminder: str | None) -> str:
        """Format reminder for preview display."""
        if meeting.reminders:
            # Specific reminders requested
            return f"Reminder: {self._format_minutes_list(meeting.reminders)}"
        elif meeting.use_default_reminder:
            # Use default reminder
            if default_reminder:
                mins = [int(x) for x in default_reminder.split(",")]
                return f"Reminder: {self._format_minutes_list(mins)} (default)"
            else:
                return "Reminder: None (no default set)"
        else:
            return ""  # No reminder

    def _format_minutes_list(self, minutes: list[int]) -> str:
        """Format list of minutes into readable string."""
        parts = []
        for m in minutes:
            if m >= 1440:  # 1 day or more
                days = m // 1440
                parts.append(f"{days} day{'s' if days > 1 else ''}")
            elif m >= 60:
                hours = m // 60
                parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
            else:
                parts.append(f"{m} min")
        return ", ".join(parts) + " before"

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
