"""Utility for generating shareable Google Calendar links."""

from datetime import datetime
from urllib.parse import quote


def generate_google_calendar_link(
    title: str,
    start_time: datetime,
    end_time: datetime,
    timezone: str,
    attendees: list[str] | None = None,
) -> str:
    """Generate a universal Google Calendar link that anyone can use.

    This creates an "Add to Calendar" link that allows any user to add
    the event to their own Google Calendar, unlike the htmlLink which
    only works for the calendar owner.

    Args:
        title: Event title
        start_time: Event start time (in user's local timezone)
        end_time: Event end time (in user's local timezone)
        timezone: IANA timezone string (e.g., 'America/New_York')
        attendees: Optional list of attendee email addresses

    Returns:
        A Google Calendar URL that anyone can click to add the event
    """
    # Format dates as YYYYMMDDTHHMMSS (local time with timezone parameter)
    date_format = "%Y%m%dT%H%M%S"
    start_str = start_time.strftime(date_format)
    end_str = end_time.strftime(date_format)

    # Build the URL
    base_url = "https://calendar.google.com/calendar/render"
    params = [
        "action=TEMPLATE",
        f"text={quote(title)}",
        f"dates={start_str}/{end_str}",
        f"ctz={quote(timezone)}",
    ]

    # Add attendees if present
    if attendees:
        params.append(f"add={quote(','.join(attendees))}")

    return f"{base_url}?{'&'.join(params)}"
