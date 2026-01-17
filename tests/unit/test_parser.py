"""Tests for meeting parser."""

from calendarbot.services.parser import MeetingParser


class TestMeetingParser:
    """Tests for MeetingParser."""

    def test_parse_time_and_title(self):
        """Test parsing with just time and title."""
        parser = MeetingParser(user_timezone="UTC", default_duration=60)
        result = parser.parse('14:30 "Team Meeting"')

        assert result is not None
        assert result.time == "14:30"
        assert result.date is None
        assert result.title == "Team Meeting"
        assert result.attendees == []

    def test_parse_with_date(self):
        """Test parsing with date."""
        parser = MeetingParser(user_timezone="UTC", default_duration=60)
        result = parser.parse('10:00 25-12-2026 "Christmas Planning"')

        assert result is not None
        assert result.time == "10:00"
        assert result.date == "25-12-2026"
        assert result.title == "Christmas Planning"
        assert result.start_datetime.day == 25
        assert result.start_datetime.month == 12

    def test_parse_with_attendees(self):
        """Test parsing with attendees."""
        parser = MeetingParser(user_timezone="UTC", default_duration=60)
        result = parser.parse('14:30 "Sync" john@example.com, jane@test.org')

        assert result is not None
        assert result.title == "Sync"
        assert len(result.attendees) == 2
        assert "john@example.com" in result.attendees
        assert "jane@test.org" in result.attendees

    def test_parse_full_command(self):
        """Test parsing full command with all parts."""
        parser = MeetingParser(user_timezone="UTC", default_duration=30)
        result = parser.parse('09:00 01-06-2026 "Project Review" alice@corp.com')

        assert result is not None
        assert result.time == "09:00"
        assert result.date == "01-06-2026"
        assert result.title == "Project Review"
        assert result.attendees == ["alice@corp.com"]
        # Check duration
        diff = result.end_datetime - result.start_datetime
        assert diff.seconds == 30 * 60

    def test_parse_missing_time_returns_none(self):
        """Test that missing time returns None."""
        parser = MeetingParser()
        result = parser.parse('"Just a title"')

        assert result is None

    def test_parse_missing_title_returns_none(self):
        """Test that missing title returns None."""
        parser = MeetingParser()
        result = parser.parse('14:30 no-quotes-title')

        assert result is None

    def test_parse_invalid_time(self):
        """Test that invalid time is handled."""
        parser = MeetingParser()
        result = parser.parse('25:00 "Invalid time"')

        assert result is None

    def test_validate_emails(self):
        """Test email validation."""
        parser = MeetingParser()

        valid, invalid = parser.validate_emails([
            "good@example.com",
            "also.good@test.org",
            "bad-email",
            "missing@domain",
        ])

        assert len(valid) == 2
        assert len(invalid) == 2
        assert "good@example.com" in valid
        assert "bad-email" in invalid

    def test_format_preview(self):
        """Test preview formatting."""
        parser = MeetingParser(default_duration=60)
        result = parser.parse('14:30 01-01-2026 "Test Meeting" test@example.com')

        assert result is not None
        preview = parser.format_preview(result)

        assert "Test Meeting" in preview
        assert "14:30" in preview
        assert "01 Jan 2026" in preview
        assert "test@example.com" in preview

    def test_parse_curly_quotes(self):
        """Test parsing with curly/smart quotes (common on iPhone)."""
        parser = MeetingParser(user_timezone="UTC", default_duration=60)
        result = parser.parse('14:30 "Team Meeting"')

        assert result is not None
        assert result.title == "Team Meeting"
        assert result.time == "14:30"

    def test_parse_russian_guillemets(self):
        """Test parsing with Russian/French guillemets."""
        parser = MeetingParser(user_timezone="UTC", default_duration=60)
        result = parser.parse('15:00 «Встреча команды»')

        assert result is not None
        assert result.title == "Встреча команды"
        assert result.time == "15:00"

    def test_parse_german_quotes(self):
        """Test parsing with German-style low quotes."""
        parser = MeetingParser(user_timezone="UTC", default_duration=60)
        result = parser.parse('16:00 „German Meeting"')

        assert result is not None
        assert result.title == "German Meeting"
        assert result.time == "16:00"

    def test_parse_single_curly_quotes(self):
        """Test parsing with single curly quotes."""
        parser = MeetingParser(user_timezone="UTC", default_duration=60)
        result = parser.parse("14:30 'Quick Call'")

        assert result is not None
        assert result.title == "Quick Call"

    def test_parse_cjk_quotes(self):
        """Test parsing with CJK corner brackets."""
        parser = MeetingParser(user_timezone="UTC", default_duration=60)
        result = parser.parse('10:00 「会議」')

        assert result is not None
        assert result.title == "会議"

    def test_parse_mixed_quote_styles(self):
        """Test parsing with mismatched quote styles (opening/closing from different sets)."""
        parser = MeetingParser(user_timezone="UTC", default_duration=60)
        # Opening curly, closing straight
        result = parser.parse('14:30 "Meeting Title"')

        assert result is not None
        assert result.title == "Meeting Title"

    def test_parse_fullwidth_quotes(self):
        """Test parsing with fullwidth quotes (common in CJK input)."""
        parser = MeetingParser(user_timezone="UTC", default_duration=60)
        result = parser.parse('14:30 ＂Full Width＂')

        assert result is not None
        assert result.title == "Full Width"

    def test_parse_heavy_quotes(self):
        """Test parsing with heavy ornamental quotes."""
        parser = MeetingParser(user_timezone="UTC", default_duration=60)
        result = parser.parse('14:30 ❝Fancy Meeting❞')

        assert result is not None
        assert result.title == "Fancy Meeting"

    def test_normalize_quotes_method(self):
        """Test the _normalize_quotes method directly."""
        parser = MeetingParser()

        # Test various quote types are normalized to standard double quote
        test_cases = [
            ('"curly"', '"curly"'),
            ('«guillemets»', '"guillemets"'),
            ('„german"', '"german"'),
            ("'single'", '"single"'),
            ('「cjk」', '"cjk"'),
            ('＂fullwidth＂', '"fullwidth"'),
            ('❝heavy❞', '"heavy"'),
        ]

        for input_text, expected in test_cases:
            assert parser._normalize_quotes(input_text) == expected, f"Failed for: {input_text}"
