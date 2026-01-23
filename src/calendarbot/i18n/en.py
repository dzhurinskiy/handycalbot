"""English translations for CalendarBot."""

from calendarbot.i18n.base import (
    CommandTranslations,
    CommonTranslations,
    DonationTranslations,
    FeedbackTranslations,
    InlineTranslations,
    MeetingsTranslations,
    ReminderTranslations,
    SettingsTranslations,
    StartTranslations,
    Translations,
)

translations = Translations(
    common=CommonTranslations(
        please_start_first="Please run /start first.",
        cancelled="Cancelled.",
        aborted="Aborted.",
        error_user_not_found="Error: User not found.",
    ),
    start=StartTranslations(
        welcome_message="""
Welcome to *HandyCalBot*! 📅

I help you schedule meetings directly from Telegram.

*Quick Start:*
1️⃣ Connect your Google Calendar with /connect
2️⃣ Create meetings by typing @handycalbot in any chat

*Inline Usage:*
`@handycalbot 14:30 "Meeting Title" email@example.com`
`@handycalbot 10:00 25-01-2026 "Project Sync"`
`@handycalbot 14:30 "Meeting" r 10m` (with reminder)
`@handycalbot 14:30 "Meeting" @alice @bob` (invite by username)

*All Commands:*
/start - Welcome message
/help - Show help and usage
/connect - Connect Google Calendar
/disconnect - Disconnect calendar
/connectzoom - Connect Zoom for meeting links
/disconnectzoom - Disconnect Zoom
/meetings - View and manage meetings
/settings - View your settings
/timezone - Change timezone
/duration - Set default duration
/reminder - Set default reminder
/notifications - Toggle reminders
/privacy - Username invite settings
/language - Change language
/feedback - Send feedback or report bugs
/donate - Support the bot ⭐

_Bug reports and UI improvement suggestions are welcome!_
""",
        help_message="""
*HandyCalBot Help* 📅

*Creating Meetings (Inline):*
Type `@handycalbot` in any chat followed by:
• Time (required): `HH:MM` (24-hour format)
• Date (optional): `DD-MM-YYYY`
• Title (required): `"Your Meeting Title"`
• Attendees (optional): `email@example.com` or `@username`
• Reminder (optional): `r 10m` or `r 10m/30m` or just `r`

*Reminder Format:*
• `r 10m` - remind 10 minutes before
• `r 1h` - remind 1 hour before
• `r 1d` - remind 1 day before
• `r 10m/30m` - multiple reminders
• `r` - use your default reminder
• (no r) - no reminder

*Examples:*
`@handycalbot 14:30 "Team Standup"`
`@handycalbot 10:00 25-01-2026 "Review" john@co.com`
`@handycalbot 16:00 "Quick Call" r 15m`
`@handycalbot 14:00 "Meeting" @alice @bob r 10m`

*All Commands:*
/start - Welcome message
/help - This help message
/connect - Connect Google Calendar
/disconnect - Disconnect calendar
/connectzoom - Connect Zoom for meeting links
/disconnectzoom - Disconnect Zoom
/meetings - View and manage meetings
/settings - View your settings
/timezone - Set your timezone
/duration - Set default meeting duration
/reminder - Set default reminder
/notifications - Toggle reminder notifications
/privacy - Username invite settings
/language - Change language
/feedback - Send feedback or report bugs
/donate - Support the bot with Stars ⭐
""",
        timezone_detected="I've set your timezone to `{timezone}` based on your Telegram language. Use /timezone to change it if needed.",
        support_button="⭐ Support HandyCalBot",
        pending_invites_found="🎉 You have pending meeting invitations!",
        pending_invite_notification="📅 **{title}**\n🕐 {time}\nInvited by: {inviter}",
    ),
    settings=SettingsTranslations(
        # Settings display
        your_settings="**Your Settings** ⚙️",
        timezone_label="Timezone",
        duration_label="Default Duration",
        reminder_label="Default Reminder",
        notifications_label="Notifications",
        google_calendar_label="Google Calendar",
        outlook_calendar_label="Outlook Calendar",
        change_settings="**Change Settings:**",
        connected="✅ Connected",
        not_connected="Not connected",
        enabled="Enabled",
        disabled="Disabled",
        no_reminder="No reminder",
        before="before",
        day="day",
        days="days",
        hour="hour",
        hours="hours",
        minutes="min",
        # Connect/Disconnect
        calendar_already_connected="Google Calendar is already connected!\nUse /disconnect to unlink it first.",
        click_to_connect="Click the button below to connect your Google Calendar.\n\nYou'll be redirected to Google to authorize access.",
        connect_button="🔗 Connect Google Calendar",
        calendar_disconnected="✅ Google Calendar disconnected successfully.\nUse /connect to link it again.",
        no_calendar_connected="No calendar connected.",
        # Zoom Connect/Disconnect
        zoom_already_connected="Zoom is already connected!\nUse /disconnectzoom to unlink it first.",
        click_to_connect_zoom="Click the button below to connect your Zoom account.\n\nYou'll be redirected to Zoom to authorize access.",
        connect_zoom_button="📹 Connect Zoom",
        zoom_disconnected="✅ Zoom disconnected successfully.\nUse /connectzoom to link it again.",
        no_zoom_connected="No Zoom account connected.",
        # Outlook Connect/Disconnect
        outlook_already_connected="Outlook Calendar is already connected!\nUse /disconnectoutlook to unlink it first.",
        click_to_connect_outlook="Click the button below to connect your Microsoft Outlook Calendar.\n\nYou'll be redirected to Microsoft to authorize access.",
        connect_outlook_button="🔗 Connect Outlook Calendar",
        outlook_disconnected="✅ Outlook Calendar disconnected successfully.\nUse /connectoutlook to link it again.",
        no_outlook_connected="No Outlook calendar connected.",
        connect_outlook_mode_title="**Connect Outlook Calendar**\n\nChoose connection mode:",
        outlook_connected_status="**Outlook Calendar Connected** ✅\n\nCurrent mode: {mode}\n\nYou can switch modes or disconnect below:",
        # Privacy mode selection
        connect_mode_title="**Connect Google Calendar**\n\nChoose connection mode:",
        connect_full_access_button="📅 Full Access",
        connect_privacy_mode_button="🔒 Privacy Mode",
        connect_full_access_desc="_Full Access: Create meetings and view your calendar (/meetings shows all events)_",
        connect_privacy_mode_desc="_Privacy Mode: Create meetings only, no calendar reading (/meetings shows only bot-created events)_",
        # Calendar connected status (mode switching)
        calendar_connected_status="**Google Calendar Connected** ✅\n\nCurrent mode: {mode}\n\nYou can switch modes or disconnect below:",
        current_mode_full="📅 Full Access",
        current_mode_privacy="🔒 Privacy Mode",
        switch_to_full_button="📅 Switch to Full Access",
        switch_to_privacy_button="🔒 Switch to Privacy Mode",
        disconnect_button="❌ Disconnect",
        # Timezone
        select_timezone="Select your timezone or type it manually (e.g., `Europe/Berlin`):",
        timezone_set="✅ Timezone set to: `{timezone}`",
        timezone_set_ready='✅ Timezone set to: `{timezone}`\n\nYou\'re all set! Create meetings using:\n`@handycalbot 14:30 "Meeting Title"`',
        invalid_timezone="❌ Invalid timezone: `{timezone}`\nPlease use a valid timezone like `Europe/London` or `America/New_York`.",
        # Duration
        select_duration="Select default meeting duration:",
        duration_set="✅ Default duration set to: {duration} minutes",
        # Reminder
        select_reminder="Select default reminder for new meetings:\n\n_You can override this per-meeting using `r 10m` in your inline query._",
        reminder_set="Default reminder set to: {reminder}",
        reminder_override_hint="_Use `r` in your inline query to apply this default, or `r 10m` to override with a specific time._",
        # Notifications
        notifications_title="**Meeting Notifications** 🔔",
        notifications_status="Status: {status}",
        notifications_explanation="When enabled, you'll receive Telegram notifications before your meetings (based on the reminder times you set).",
        select_option="Select an option:",
        enable_button="Enable",
        disable_button="Disable",
        current_suffix="(current)",
        notifications_updated="{emoji} Meeting notifications {status}.",
        will_receive_reminders="You will now receive reminders before your meetings.",
        will_not_receive_reminders="You will no longer receive meeting reminders.",
        # Language
        select_language="🌍 Select your preferred language:",
        language_updated="✅ Language updated successfully!",
        # Privacy settings
        privacy_title="**Privacy Settings** 🔒",
        privacy_username_invites="Allow @username invites",
        privacy_enabled_desc="Others can invite you to meetings using your @username",
        privacy_disabled_desc="Only direct email invites will work",
        privacy_updated="{emoji} Username invites {status}.",
        # Default calendar preference
        default_calendar_label="Default Calendar",
        default_calendar_requires_both="You need both Google and Outlook calendars connected to set a preference.\n\nUse /connect and /connectoutlook to connect both.",
        default_calendar_title="**Default Calendar** 🎯",
        default_calendar_desc="Choose which calendar to use by default when creating meetings.\n\nYou can switch calendars for individual meetings from the Edit menu.",
        default_calendar_updated="✅ Default calendar set to {calendar}.\n\nNew meetings will be created there.",
    ),
    meetings=MeetingsTranslations(
        upcoming_meetings="**Upcoming Meetings** 📅",
        no_upcoming_meetings="No upcoming meetings found.",
        use_cancel_hint="_Use /cancel to cancel a meeting_",
        attendees_count="👥 {count} attendee(s)",
        privacy_mode_note="_🔒 Privacy mode: Showing only bot-created meetings_",
        # Meeting list and detail view
        close_button="✖️ Close",
        edit_button="✏️ Edit",
        cancel_meeting_button="🗑️ Cancel",
        back_to_list_button="↩️ Back to List",
        closed="Meeting list closed.",
        # Edit menu
        edit_menu_title="✏️ **Edit Meeting**\n\nSelect a field to edit:",
        edit_title_btn="📝 Title",
        edit_time_btn="🕐 Time",
        edit_date_btn="📅 Date",
        edit_duration_btn="⏱️ Duration",
        edit_attendees_btn="👥 Attendees",
        edit_link_btn="🔗 Link",
        switch_to_calendar="Move to {calendar}",
        calendar_switched="✅ Meeting moved to {calendar}.",
        field_updated="✅ {field} updated",
        # Cancel menu
        select_meeting_to_cancel="**Select a meeting to cancel:**",
        page_info="Page {current}/{total}",
        total_meetings="{count} total meetings",
        previous_button="⬅️ Previous",
        next_button="Next ➡️",
        dont_cancel_button="❌ Don't cancel anything",
        no_meeting_cancelled="No meeting cancelled.",
        cancelling_meeting="Cancelling meeting...",
        meeting_cancelled="✅ Meeting cancelled: **{title}**",
        attendees_notified="_Attendees will be notified automatically._",
        cancel_not_your_menu="❌ Error: This is not your cancel menu.",
        session_expired="❌ Error: Session expired. Please use /cancel again.",
        meeting_not_found="❌ Error: Meeting not found. Please use /cancel again.",
    ),
    inline=InlineTranslations(
        # Help
        how_to_create="How to create a meeting",
        inline_help_description='Type: 14:30 "Meeting Title" email@example.com',
        inline_help_message='To create a meeting, type:\n@handycalbot 14:30 "Meeting Title" email@example.com\n\nFormat: TIME [DATE] "TITLE" [EMAILS]',
        # Not registered
        please_start_first_title="Please start the bot first",
        please_start_first_description="Click to open bot and run /start",
        please_start_first_message="Please start @handycalbot first by sending /start",
        # Parse error
        could_not_parse="Could not parse meeting",
        parse_error_description='Use format: 14:30 "Meeting Title" emails...',
        parse_error_message='Could not parse meeting. Use format:\n14:30 "Meeting Title" email@example.com\n\nTime and title in quotes are required.\nAdd r 10m for reminder, or just r for default.',
        # Calendar not connected
        calendar_not_connected_warning="⚠️ Calendar not connected - /connect first",
        # Meeting preview
        attendees_label="👥 {count} attendee(s)",
        today="today",
        # Create/Cancel buttons
        create_meeting_button="Create Meeting",
        cancel_button="Cancel",
        # Creation results
        creating_meeting="Creating meeting...",
        meeting_data_expired="❌ Error: Meeting data expired. Please try again.",
        not_your_meeting="❌ This is not your meeting!",
        meeting_created="Meeting created!",
        reminder_label="🔔 Reminder: {reminder} before",
        invitations_sent="📧 Invitations sent to:",
        attendees_will_receive="_These attendees will receive a calendar invitation automatically._",
        add_to_calendar_button="📅 Add to My Calendar",
        not_listed_add_calendar="_Not listed above? Click below to add to your calendar:_",
        click_to_add_calendar="_Click below to add to your calendar:_",
        meeting_cancelled="Meeting cancelled.",
        # Username mentions
        username_registered="registered",
        username_privacy_disabled="privacy disabled",
        username_not_found="not found",
        pending_invites_note="⏳ Not registered yet:",
        rate_limit_warning="⚠️ Too many username lookups. Try again later.",
        no_calendar_users_note="⚠️ Registered but no calendar connected:",
        privacy_disabled_users_note="🔒 Privacy disabled (no invite sent):",
        register_link_text="Register",
        # Edit menu
        edit_button="Edit",
        edit_menu_title="✏️ *Edit Meeting*\n\nWhat would you like to change?",
        edit_title_button="📝 Title",
        edit_time_button="🕐 Time",
        edit_date_button="📅 Date",
        edit_duration_button="⏱️ Duration",
        edit_reminder_button="🔔 Reminder",
        edit_attendees_button="👥 Attendees",
        edit_link_button="🔗 Add Link",
        back_button="↩️ Back",
        done_editing_button="✅ Done",
        # Edit prompts
        enter_new_title='📝 *Enter new title*\n\nCurrent: "{current}"\n\nType the new title and send it.',
        enter_new_time="🕐 *Enter new time*\n\nCurrent: {current}\n\nType the new time (HH:MM) and send it.",
        enter_new_date="📅 *Enter new date*\n\nCurrent: {current}\n\nType the new date (DD-MM-YYYY) and send it.",
        select_duration="⏱️ *Select Duration*",
        select_reminder="🔔 *Select Reminder*",
        # Attendees
        current_attendees="*Current attendees:*",
        add_attendee_prompt="👥 *Add Attendee*\n\nType an email address or @username and send it.",
        recent_contacts_title="*Recent contacts:*",
        no_recent_contacts="No recent contacts",
        type_manually_button="✍️ Type email/@username",
        remove_attendee_button="🗑️",
        attendee_added="✅ Attendee added",
        attendee_removed="✅ Attendee removed",
        invalid_email_format="❌ Invalid format. Use email@example.com or @username",
        no_attendees="No attendees yet",
        # Link
        add_link_title="🔗 *Meeting Link*",
        invalid_link_format="❌ Invalid link. Please enter a URL starting with http:// or https://",
        invalid_time_format="❌ Invalid time format. Try 14:00, 2pm, or 14.30",
        invalid_date_format="❌ Invalid date format. Try tomorrow, Jan 20, or 20-01",
        auto_google_meet="🎥 Auto Google Meet",
        auto_teams_meeting="📹 Auto Microsoft Teams",
        auto_zoom_meeting="📹 Auto Zoom Meeting",
        paste_custom_link="📋 Paste Custom Link",
        enter_link_prompt="🔗 *Enter meeting link*\n\nPaste your meeting URL and send it.",
        link_added="✅ Link added",
        link_removed="✅ Link removed",
        remove_link_button="🗑️ Remove Link",
        google_meet_label="🎥 Google Meet",
        teams_meeting_label="📹 Microsoft Teams",
        zoom_meeting_label="📹 Zoom Meeting",
        zoom_not_connected="Zoom not connected. Use /connectzoom first.",
        outlook_not_connected="Outlook not connected. Use /connectoutlook first.",
        custom_link_label="🔗 Meeting Link",
        # Updates
        field_updated="✅ {field} updated",
        meeting_updated="Meeting updated",
        # Duration options
        duration_15_min="15 min",
        duration_30_min="30 min",
        duration_45_min="45 min",
        duration_1_hour="1 hour",
        duration_1_5_hours="1.5 hours",
        duration_2_hours="2 hours",
        # Reminder options
        reminder_none="None",
        reminder_5_min="5 min",
        reminder_10_min="10 min",
        reminder_15_min="15 min",
        reminder_30_min="30 min",
        reminder_1_hour="1 hour",
        reminder_1_day="1 day",
        # Cancel edit
        cancel_edit_button="❌ Cancel",
        edit_cancelled="Edit cancelled",
        # Private chat prompts (for text input redirect)
        continue_in_private="To edit this, continue in private chat:",
        open_private_chat="💬 Open Private Chat",
        session_expired_restart="Session expired. Please start editing again from the original message.",
        edit_complete_return="✅ Done! The message has been updated.",
        back_to_chat_button="↩️ Back to Chat",
        # Time selection grid
        select_time_title="🕐 *Select Time*",
        time_morning="Morning",
        time_afternoon="Afternoon",
        custom_time_button="⌨️ Custom",
        # Date selection grid
        select_date_title="📅 *Select Date*",
        date_today="Today",
        date_tomorrow="Tomorrow",
        date_day_after="Day after tomorrow",
        date_in_3_days="In 3 days",
        date_in_a_week="In a week",
        custom_date_button="⌨️ Custom",
    ),
    donation=DonationTranslations(
        support_title="**Support HandyCalBot** ⭐",
        support_description="If you find this bot useful, consider supporting its development with Telegram Stars!",
        support_helps="Your support helps keep the bot running and enables new features.",
        select_amount="Select an amount:",
        custom_amount_button="💫 Custom Amount",
        custom_amount_prompt="**Custom Donation** 💫\n\nPlease enter the number of Stars you'd like to donate (1-10000):",
        invalid_amount="Please enter a valid amount between 1 and 10000 Stars.",
        invalid_number="Please enter a valid number (1-10000).",
        donation_error="Sorry, there was an error processing your donation. Please try again later.",
        thank_you="**Thank you for your donation!** 🙏",
        you_donated="You donated {amount} Telegram Stars. Your support means a lot!",
        thank_you_running="Thank you for helping keep HandyCalBot running! ⭐",
    ),
    reminder=ReminderTranslations(
        meeting_reminder="🔔 *Meeting Reminder*",
        starting_in="Starting in {time}",
    ),
    feedback=FeedbackTranslations(
        feedback_title="📝 **Feedback**",
        feedback_prompt="Please describe your feedback, bug report, or suggestion.",
        feedback_abort_hint="Type /abort to cancel.",
        feedback_received="✅ Thank you for your feedback!",
        feedback_thank_you="Your message has been received and will be reviewed.",
    ),
    commands=CommandTranslations(
        start="Start the bot and see welcome message",
        help="Show help and usage instructions",
        meetings="List your upcoming meetings",
        cancel="Cancel a meeting",
        connect="Connect Google Calendar",
        disconnect="Disconnect Google Calendar",
        connectoutlook="Connect Outlook Calendar",
        disconnectoutlook="Disconnect Outlook Calendar",
        connectzoom="Connect Zoom for meeting links",
        disconnectzoom="Disconnect Zoom account",
        settings="View your current settings",
        timezone="Change your timezone",
        duration="Set default meeting duration",
        reminder="Set default reminder",
        notifications="Toggle meeting notifications",
        privacy="Privacy settings for @username invites",
        language="Change language",
        donate="Support the bot with Telegram Stars",
        feedback="Send feedback or report a bug",
    ),
)
