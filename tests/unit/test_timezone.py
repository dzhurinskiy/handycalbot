"""Tests for timezone utilities."""

from datetime import datetime
from zoneinfo import ZoneInfo

from calendarbot.utils.timezone import TimezoneHelper


class TestTimezoneHelper:
    """Tests for TimezoneHelper."""

    def test_get_timezone_valid(self):
        """Test getting valid timezone."""
        tz = TimezoneHelper.get_timezone("Europe/London")
        assert tz == ZoneInfo("Europe/London")

    def test_get_timezone_alias(self):
        """Test timezone aliases."""
        tz = TimezoneHelper.get_timezone("PST")
        assert tz == ZoneInfo("America/Los_Angeles")

    def test_is_valid_timezone(self):
        """Test timezone validation."""
        assert TimezoneHelper.is_valid_timezone("UTC")
        assert TimezoneHelper.is_valid_timezone("Europe/Berlin")
        assert not TimezoneHelper.is_valid_timezone("Invalid/Zone")

    def test_to_utc(self):
        """Test conversion to UTC."""
        dt = datetime(2026, 6, 15, 12, 0)  # Noon in Berlin (CEST = UTC+2)
        utc_dt = TimezoneHelper.to_utc(dt, "Europe/Berlin")

        assert utc_dt.hour == 10  # Should be 10:00 UTC

    def test_from_utc(self):
        """Test conversion from UTC."""
        dt = datetime(2026, 6, 15, 10, 0, tzinfo=ZoneInfo("UTC"))
        berlin_dt = TimezoneHelper.from_utc(dt, "Europe/Berlin")

        assert berlin_dt.hour == 12  # Should be 12:00 in Berlin

    def test_now_in_tz(self):
        """Test getting current time in timezone."""
        now_utc = TimezoneHelper.now_in_tz("UTC")
        now_tokyo = TimezoneHelper.now_in_tz("Asia/Tokyo")

        # Tokyo is ahead of UTC
        assert now_tokyo.utcoffset() > now_utc.utcoffset()

    def test_common_timezones(self):
        """Test common timezones list."""
        timezones = TimezoneHelper.get_common_timezones()

        assert "UTC" in timezones
        assert "Europe/London" in timezones
        assert "America/New_York" in timezones
        assert len(timezones) > 10
