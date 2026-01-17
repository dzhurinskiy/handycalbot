"""German translations for CalendarBot."""

from calendarbot.i18n.base import (
    CommonTranslations,
    DonationTranslations,
    InlineTranslations,
    MeetingsTranslations,
    ReminderTranslations,
    SettingsTranslations,
    StartTranslations,
    Translations,
)

translations = Translations(
    common=CommonTranslations(
        please_start_first="Bitte fuhre zuerst /start aus.",
        cancelled="Abgebrochen.",
        error_user_not_found="Fehler: Benutzer nicht gefunden.",
    ),
    start=StartTranslations(
        welcome_message="""
Willkommen bei *HandyCalBot*!

Ich helfe dir, Besprechungen direkt von Telegram aus zu planen.

*Schnellstart:*
1. Verbinde deinen Google Kalender mit /connect
2. Erstelle Besprechungen, indem du @handycalbot in einem Chat eingibst

*Inline-Nutzung:*
`@handycalbot 14:30 "Besprechungstitel" email@beispiel.com`
`@handycalbot 10:00 25-01-2026 "Projektsynchronisation"`
`@handycalbot 14:30 "Besprechung" r 10m` (mit Erinnerung)

*Alle Befehle:*
/start - Willkommensnachricht
/help - Hilfe und Nutzung anzeigen
/connect - Google Kalender verbinden
/disconnect - Kalender trennen
/meetings - Kommende Besprechungen auflisten
/cancel - Eine Besprechung absagen
/settings - Deine Einstellungen ansehen
/timezone - Zeitzone andern
/duration - Standarddauer festlegen
/reminder - Standard-Erinnerung festlegen
/notifications - Erinnerungen ein/ausschalten
/language - Sprache andern
/donate - Den Bot unterstutzen
""",
        help_message="""
*HandyCalBot Hilfe*

*Besprechungen erstellen (Inline):*
Gib `@handycalbot` in einem Chat ein, gefolgt von:
- Zeit (erforderlich): `HH:MM` (24-Stunden-Format)
- Datum (optional): `TT-MM-JJJJ`
- Titel (erforderlich): `"Dein Besprechungstitel"`
- Teilnehmer (optional): `email@beispiel.com`
- Erinnerung (optional): `r 10m` oder `r 10m/30m` oder nur `r`

*Erinnerungsformat:*
- `r 10m` - 10 Minuten vorher erinnern
- `r 1h` - 1 Stunde vorher erinnern
- `r 1d` - 1 Tag vorher erinnern
- `r 10m/30m` - mehrere Erinnerungen
- `r` - Standard-Erinnerung verwenden
- (kein r) - keine Erinnerung

*Beispiele:*
`@handycalbot 14:30 "Team-Standup"`
`@handycalbot 10:00 25-01-2026 "Review" hans@co.com`
`@handycalbot 16:00 "Kurzer Anruf" r 15m`
`@handycalbot 14:00 "Besprechung" anna@co.com r 10m/1h`

*Alle Befehle:*
/start - Willkommensnachricht
/help - Diese Hilfenachricht
/connect - Google Kalender verbinden
/disconnect - Kalender trennen
/meetings - Kommende Besprechungen anzeigen
/cancel - Eine Besprechung absagen
/settings - Deine Einstellungen ansehen
/timezone - Deine Zeitzone festlegen
/duration - Standard-Besprechungsdauer festlegen
/reminder - Standard-Erinnerung festlegen
/notifications - Erinnerungsbenachrichtigungen ein/ausschalten
/language - Sprache andern
/donate - Den Bot mit Stars unterstutzen
""",
        timezone_detected="Ich habe deine Zeitzone basierend auf deiner Telegram-Sprache auf `{timezone}` gesetzt. Benutze /timezone, um sie bei Bedarf zu andern.",
        support_button="HandyCalBot unterstutzen",
    ),
    settings=SettingsTranslations(
        your_settings="**Deine Einstellungen**",
        timezone_label="Zeitzone",
        duration_label="Standarddauer",
        reminder_label="Standard-Erinnerung",
        notifications_label="Benachrichtigungen",
        google_calendar_label="Google Kalender",
        change_settings="**Einstellungen andern:**",
        connected="Verbunden",
        not_connected="Nicht verbunden",
        enabled="Aktiviert",
        disabled="Deaktiviert",
        no_reminder="Keine Erinnerung",
        before="vorher",
        day="Tag",
        days="Tage",
        hour="Stunde",
        hours="Stunden",
        minutes="Min",
        calendar_already_connected="Google Kalender ist bereits verbunden!\nBenutze /disconnect, um ihn zuerst zu trennen.",
        click_to_connect="Klicke auf den Button unten, um deinen Google Kalender zu verbinden.\n\nDu wirst zu Google weitergeleitet, um den Zugriff zu autorisieren.",
        connect_button="Google Kalender verbinden",
        calendar_disconnected="Google Kalender erfolgreich getrennt.\nBenutze /connect, um ihn wieder zu verbinden.",
        no_calendar_connected="Kein Kalender verbunden.",
        select_timezone="Wahle deine Zeitzone oder gib sie manuell ein (z.B. `Europe/Berlin`):",
        timezone_set="Zeitzone gesetzt auf: `{timezone}`",
        timezone_set_ready="Zeitzone gesetzt auf: `{timezone}`\n\nDu bist bereit! Erstelle Besprechungen mit:\n`@handycalbot 14:30 \"Besprechungstitel\"`",
        invalid_timezone="Ungultige Zeitzone: `{timezone}`\nBitte benutze eine gultige Zeitzone wie `Europe/Berlin` oder `Europe/Vienna`.",
        select_duration="Wahle die Standard-Besprechungsdauer:",
        duration_set="Standarddauer gesetzt auf: {duration} Minuten",
        select_reminder="Wahle die Standard-Erinnerung fur neue Besprechungen:\n\n_Du kannst dies pro Besprechung mit `r 10m` in deiner Inline-Anfrage uberschreiben._",
        reminder_set="Standard-Erinnerung gesetzt auf: {reminder}",
        reminder_override_hint="_Benutze `r` in deiner Anfrage, um diesen Standard anzuwenden, oder `r 10m`, um mit einer bestimmten Zeit zu uberschreiben._",
        notifications_title="**Besprechungs-Benachrichtigungen**",
        notifications_status="Status: {status}",
        notifications_explanation="Wenn aktiviert, erhaltst du Telegram-Benachrichtigungen vor deinen Besprechungen (basierend auf den eingestellten Erinnerungszeiten).",
        select_option="Wahle eine Option:",
        enable_button="Aktivieren",
        disable_button="Deaktivieren",
        current_suffix="(aktuell)",
        notifications_updated="{emoji} Besprechungs-Benachrichtigungen {status}.",
        will_receive_reminders="Du wirst jetzt Erinnerungen vor deinen Besprechungen erhalten.",
        will_not_receive_reminders="Du wirst keine Besprechungserinnerungen mehr erhalten.",
        select_language="Wahle deine bevorzugte Sprache:",
        language_updated="Sprache erfolgreich aktualisiert!",
    ),
    meetings=MeetingsTranslations(
        upcoming_meetings="**Kommende Besprechungen**",
        no_upcoming_meetings="Keine kommenden Besprechungen gefunden.",
        use_cancel_hint="_Benutze /cancel, um eine Besprechung abzusagen_",
        attendees_count="{count} Teilnehmer",
        select_meeting_to_cancel="**Wahle eine Besprechung zum Absagen:**",
        page_info="Seite {current}/{total}",
        total_meetings="{count} Besprechungen insgesamt",
        previous_button="Zuruck",
        next_button="Weiter",
        dont_cancel_button="Nichts absagen",
        no_meeting_cancelled="Keine Besprechung abgesagt.",
        cancelling_meeting="Besprechung wird abgesagt...",
        meeting_cancelled="Besprechung abgesagt: **{title}**",
        attendees_notified="_Teilnehmer werden automatisch benachrichtigt._",
        cancel_not_your_menu="Fehler: Dies ist nicht dein Absage-Menu.",
        session_expired="Fehler: Sitzung abgelaufen. Bitte benutze /cancel erneut.",
        meeting_not_found="Fehler: Besprechung nicht gefunden. Bitte benutze /cancel erneut.",
    ),
    inline=InlineTranslations(
        how_to_create="Wie man eine Besprechung erstellt",
        inline_help_description='Gib ein: 14:30 "Besprechungstitel" email@beispiel.com',
        inline_help_message='Um eine Besprechung zu erstellen, gib ein:\n@handycalbot 14:30 "Besprechungstitel" email@beispiel.com\n\nFormat: ZEIT [DATUM] "TITEL" [EMAILS]',
        please_start_first_title="Bitte starte zuerst den Bot",
        please_start_first_description="Klicke, um den Bot zu offnen und /start auszufuhren",
        please_start_first_message="Bitte starte zuerst @handycalbot, indem du /start sendest",
        could_not_parse="Besprechung konnte nicht analysiert werden",
        parse_error_description='Benutze das Format: 14:30 "Besprechungstitel" emails...',
        parse_error_message='Besprechung konnte nicht analysiert werden. Benutze das Format:\n14:30 "Besprechungstitel" email@beispiel.com\n\nZeit und Titel in Anfuhrungszeichen sind erforderlich.\nFuge r 10m fur Erinnerung hinzu, oder nur r fur Standard.',
        calendar_not_connected_warning="Kalender nicht verbunden - zuerst /connect",
        attendees_label="{count} Teilnehmer",
        today="heute",
        create_meeting_button="Besprechung erstellen",
        cancel_button="Abbrechen",
        creating_meeting="Besprechung wird erstellt...",
        meeting_data_expired="Fehler: Besprechungsdaten abgelaufen. Bitte versuche es erneut.",
        not_your_meeting="Das ist nicht deine Besprechung!",
        meeting_created="Besprechung erstellt!",
        reminder_label="Erinnerung: {reminder} vorher",
        invitations_sent="Einladungen gesendet an:",
        attendees_will_receive="_Diese Teilnehmer erhalten automatisch eine Kalendereinladung._",
        add_to_calendar_button="Zu meinem Kalender hinzufugen",
        not_listed_add_calendar="_Nicht aufgelistet? Klicke unten, um zu deinem Kalender hinzuzufugen:_",
        click_to_add_calendar="_Klicke unten, um zu deinem Kalender hinzuzufugen:_",
        meeting_cancelled="Besprechung abgesagt.",
    ),
    donation=DonationTranslations(
        support_title="**Unterstutze HandyCalBot**",
        support_description="Wenn du diesen Bot nutzlich findest, erwage, seine Entwicklung mit Telegram Stars zu unterstutzen!",
        support_helps="Deine Unterstutzung hilft, den Bot am Laufen zu halten und ermoglicht neue Funktionen.",
        select_amount="Wahle einen Betrag:",
        custom_amount_button="Benutzerdefinierter Betrag",
        custom_amount_prompt="**Benutzerdefinierte Spende**\n\nBitte gib die Anzahl der Stars ein, die du spenden mochtest (1-10000):",
        invalid_amount="Bitte gib einen gultigen Betrag zwischen 1 und 10000 Stars ein.",
        invalid_number="Bitte gib eine gultige Zahl ein (1-10000).",
        donation_error="Entschuldigung, bei der Verarbeitung deiner Spende ist ein Fehler aufgetreten. Bitte versuche es spater erneut.",
        thank_you="**Danke fur deine Spende!**",
        you_donated="Du hast {amount} Telegram Stars gespendet. Deine Unterstutzung bedeutet uns viel!",
        thank_you_running="Danke, dass du hilfst, HandyCalBot am Laufen zu halten!",
    ),
    reminder=ReminderTranslations(
        meeting_reminder="*Besprechungserinnerung*",
        starting_in="Beginnt in {time}",
    ),
)
