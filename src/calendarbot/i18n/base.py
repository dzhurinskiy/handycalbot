"""Translation dataclass structure for CalendarBot."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CommonTranslations:
    """Common strings used across multiple handlers."""

    please_start_first: str
    cancelled: str
    aborted: str
    error_user_not_found: str


@dataclass(frozen=True)
class StartTranslations:
    """Translations for start.py handler."""

    welcome_message: str
    help_message: str
    timezone_detected: str
    support_button: str
    # Pending invites
    pending_invites_found: str
    pending_invite_notification: str


@dataclass(frozen=True)
class SettingsTranslations:
    """Translations for settings.py handler."""

    # Settings display
    your_settings: str
    timezone_label: str
    duration_label: str
    reminder_label: str
    notifications_label: str
    google_calendar_label: str
    change_settings: str
    connected: str
    not_connected: str
    enabled: str
    disabled: str
    no_reminder: str
    before: str
    day: str
    days: str
    hour: str
    hours: str
    minutes: str

    # Connect/Disconnect
    calendar_already_connected: str
    click_to_connect: str
    connect_button: str
    calendar_disconnected: str
    no_calendar_connected: str

    # Timezone
    select_timezone: str
    timezone_set: str
    timezone_set_ready: str
    invalid_timezone: str

    # Duration
    select_duration: str
    duration_set: str

    # Reminder
    select_reminder: str
    reminder_set: str
    reminder_override_hint: str

    # Notifications
    notifications_title: str
    notifications_status: str
    notifications_explanation: str
    select_option: str
    enable_button: str
    disable_button: str
    current_suffix: str
    notifications_updated: str
    will_receive_reminders: str
    will_not_receive_reminders: str

    # Language
    select_language: str
    language_updated: str

    # Privacy settings
    privacy_title: str
    privacy_username_invites: str
    privacy_enabled_desc: str
    privacy_disabled_desc: str
    privacy_updated: str


@dataclass(frozen=True)
class MeetingsTranslations:
    """Translations for meetings.py handler."""

    upcoming_meetings: str
    no_upcoming_meetings: str
    use_cancel_hint: str
    attendees_count: str

    # Cancel menu
    select_meeting_to_cancel: str
    page_info: str
    total_meetings: str
    previous_button: str
    next_button: str
    dont_cancel_button: str
    no_meeting_cancelled: str
    cancelling_meeting: str
    meeting_cancelled: str
    attendees_notified: str
    cancel_not_your_menu: str
    session_expired: str
    meeting_not_found: str


@dataclass(frozen=True)
class InlineTranslations:
    """Translations for inline.py handler."""

    # Help
    how_to_create: str
    inline_help_description: str
    inline_help_message: str

    # Not registered
    please_start_first_title: str
    please_start_first_description: str
    please_start_first_message: str

    # Parse error
    could_not_parse: str
    parse_error_description: str
    parse_error_message: str

    # Calendar not connected
    calendar_not_connected_warning: str

    # Meeting preview
    attendees_label: str
    today: str

    # Create/Cancel buttons
    create_meeting_button: str
    cancel_button: str

    # Creation results
    creating_meeting: str
    meeting_data_expired: str
    not_your_meeting: str
    meeting_created: str
    reminder_label: str
    invitations_sent: str
    attendees_will_receive: str
    add_to_calendar_button: str
    not_listed_add_calendar: str
    click_to_add_calendar: str
    meeting_cancelled: str

    # Username mentions
    username_registered: str
    username_privacy_disabled: str
    username_not_found: str
    pending_invites_note: str
    rate_limit_warning: str
    no_calendar_users_note: str
    privacy_disabled_users_note: str
    register_link_text: str

    # Edit menu
    edit_button: str
    edit_menu_title: str
    edit_title_button: str
    edit_time_button: str
    edit_date_button: str
    edit_duration_button: str
    edit_reminder_button: str
    edit_attendees_button: str
    edit_link_button: str
    back_button: str
    done_editing_button: str

    # Edit prompts
    enter_new_title: str
    enter_new_time: str
    enter_new_date: str
    select_duration: str
    select_reminder: str

    # Attendees
    current_attendees: str
    add_attendee_prompt: str
    recent_contacts_title: str
    no_recent_contacts: str
    type_manually_button: str
    remove_attendee_button: str
    attendee_added: str
    attendee_removed: str
    invalid_email_format: str

    # Link
    add_link_title: str
    auto_google_meet: str
    paste_custom_link: str
    enter_link_prompt: str
    link_added: str
    link_removed: str
    remove_link_button: str
    google_meet_label: str
    custom_link_label: str

    # Updates
    field_updated: str
    meeting_updated: str

    # Duration options
    duration_15_min: str
    duration_30_min: str
    duration_45_min: str
    duration_1_hour: str
    duration_1_5_hours: str
    duration_2_hours: str

    # Reminder options
    reminder_none: str
    reminder_5_min: str
    reminder_10_min: str
    reminder_15_min: str
    reminder_30_min: str
    reminder_1_hour: str
    reminder_1_day: str

    # Cancel edit
    cancel_edit_button: str
    edit_cancelled: str


@dataclass(frozen=True)
class DonationTranslations:
    """Translations for donation.py handler."""

    support_title: str
    support_description: str
    support_helps: str
    select_amount: str
    custom_amount_button: str
    custom_amount_prompt: str
    invalid_amount: str
    invalid_number: str
    donation_error: str
    thank_you: str
    you_donated: str
    thank_you_running: str


@dataclass(frozen=True)
class ReminderTranslations:
    """Translations for reminder.py service."""

    meeting_reminder: str
    starting_in: str


@dataclass(frozen=True)
class FeedbackTranslations:
    """Translations for feedback.py handler."""

    feedback_title: str
    feedback_prompt: str
    feedback_abort_hint: str
    feedback_received: str
    feedback_thank_you: str


@dataclass(frozen=True)
class CommandTranslations:
    """Translations for bot command descriptions shown in Telegram UI."""

    start: str
    help: str
    meetings: str
    cancel: str
    connect: str
    disconnect: str
    settings: str
    timezone: str
    duration: str
    reminder: str
    notifications: str
    privacy: str
    language: str
    donate: str
    feedback: str


@dataclass(frozen=True)
class Translations:
    """Root translations container."""

    common: CommonTranslations
    start: StartTranslations
    settings: SettingsTranslations
    meetings: MeetingsTranslations
    inline: InlineTranslations
    donation: DonationTranslations
    reminder: ReminderTranslations
    feedback: FeedbackTranslations
    commands: CommandTranslations
