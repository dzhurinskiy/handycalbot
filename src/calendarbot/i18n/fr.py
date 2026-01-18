"""French translations for CalendarBot."""

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
        please_start_first="Veuillez d'abord executer /start.",
        cancelled="Annule.",
        aborted="Abandonne.",
        error_user_not_found="Erreur : Utilisateur non trouve.",
    ),
    start=StartTranslations(
        welcome_message="""
Bienvenue sur *HandyCalBot*! 📅

Je vous aide a planifier des reunions directement depuis Telegram.

*Demarrage Rapide:*
1. Connectez votre Google Calendar avec /connect
2. Creez des reunions en tapant @handycalbot dans n'importe quel chat

*Utilisation Inline:*
`@handycalbot 14:30 "Titre de Reunion" email@exemple.com`
`@handycalbot 10:00 25-01-2026 "Synchronisation"`
`@handycalbot 14:30 "Reunion" r 10m` (avec rappel)

*Toutes les Commandes:*
/start - Message de bienvenue
/help - Afficher l'aide et l'utilisation
/connect - Connecter Google Calendar
/disconnect - Deconnecter le calendrier
/meetings - Lister les prochaines reunions
/cancel - Annuler une reunion
/settings - Voir vos parametres
/timezone - Changer le fuseau horaire
/duration - Definir la duree par defaut
/reminder - Definir le rappel par defaut
/notifications - Activer/desactiver les rappels
/language - Changer la langue
/feedback - Envoyer des commentaires ou signaler des bugs
/donate - Soutenir le bot

_Les rapports de bugs et suggestions d'amelioration sont les bienvenus!_
""",
        help_message="""
*Aide HandyCalBot* 📅

*Creer des Reunions (Inline):*
Tapez `@handycalbot` dans n'importe quel chat suivi de:
- Heure (requise): `HH:MM` (format 24 heures)
- Date (optionnelle): `JJ-MM-AAAA`
- Titre (requis): `"Votre Titre de Reunion"`
- Participants (optionnel): `email@exemple.com`
- Rappel (optionnel): `r 10m` ou `r 10m/30m` ou juste `r`

*Format de Rappel:*
- `r 10m` - rappeler 10 minutes avant
- `r 1h` - rappeler 1 heure avant
- `r 1d` - rappeler 1 jour avant
- `r 10m/30m` - rappels multiples
- `r` - utiliser le rappel par defaut
- (sans r) - pas de rappel

*Exemples:*
`@handycalbot 14:30 "Reunion d'Equipe"`
`@handycalbot 10:00 25-01-2026 "Revue" jean@co.com`
`@handycalbot 16:00 "Appel Rapide" r 15m`
`@handycalbot 14:00 "Reunion" alice@co.com r 10m/1h`

*Toutes les Commandes:*
/start - Message de bienvenue
/help - Ce message d'aide
/connect - Connecter Google Calendar
/disconnect - Deconnecter le calendrier
/meetings - Afficher les prochaines reunions
/cancel - Annuler une reunion
/settings - Voir vos parametres
/timezone - Definir votre fuseau horaire
/duration - Definir la duree par defaut
/reminder - Definir le rappel par defaut
/notifications - Activer/desactiver les notifications
/language - Changer la langue
/feedback - Envoyer des commentaires ou signaler des bugs
/donate - Soutenir le bot avec des Stars
""",
        timezone_detected="J'ai defini votre fuseau horaire sur `{timezone}` en fonction de votre langue Telegram. Utilisez /timezone pour le modifier si necessaire.",
        support_button="⭐ Soutenir HandyCalBot",
        pending_invites_found="🎉 Vous avez des invitations de réunion en attente!",
        pending_invite_notification="📅 **{title}**\n🕐 {time}\nInvité par: {inviter}",
    ),
    settings=SettingsTranslations(
        your_settings="**Vos Parametres** ⚙️",
        timezone_label="Fuseau Horaire",
        duration_label="Duree par Defaut",
        reminder_label="Rappel par Defaut",
        notifications_label="Notifications",
        google_calendar_label="Google Calendar",
        change_settings="**Modifier les Parametres:**",
        connected="✅ Connecté",
        not_connected="Non connecte",
        enabled="Active",
        disabled="Desactive",
        no_reminder="Pas de rappel",
        before="avant",
        day="jour",
        days="jours",
        hour="heure",
        hours="heures",
        minutes="min",
        calendar_already_connected="Google Calendar est deja connecte!\nUtilisez /disconnect pour le deconnecter d'abord.",
        click_to_connect="Cliquez sur le bouton ci-dessous pour connecter votre Google Calendar.\n\nVous serez redirige vers Google pour autoriser l'acces.",
        connect_button="🔗 Connecter Google Calendar",
        calendar_disconnected="✅ Google Calendar deconnecte avec succes.\nUtilisez /connect pour le reconnecter.",
        no_calendar_connected="Aucun calendrier connecte.",
        select_timezone="Selectionnez votre fuseau horaire ou tapez-le manuellement (ex., `Europe/Paris`):",
        timezone_set="✅ Fuseau horaire defini sur: `{timezone}`",
        timezone_set_ready='Fuseau horaire defini sur: `{timezone}`\n\nVous etes pret! Creez des reunions en utilisant:\n`@handycalbot 14:30 "Titre de Reunion"`',
        invalid_timezone="❌ Fuseau horaire invalide: `{timezone}`\nVeuillez utiliser un fuseau horaire valide comme `Europe/Paris` ou `America/Montreal`.",
        select_duration="Selectionnez la duree de reunion par defaut:",
        duration_set="✅ Duree par defaut definie sur: {duration} minutes",
        select_reminder="Selectionnez le rappel par defaut pour les nouvelles reunions:\n\n_Vous pouvez le remplacer par reunion en utilisant `r 10m` dans votre requete inline._",
        reminder_set="Rappel par defaut defini sur: {reminder}",
        reminder_override_hint="_Utilisez `r` dans votre requete pour appliquer ce defaut, ou `r 10m` pour remplacer avec un temps specifique._",
        notifications_title="**Notifications de Reunions** 🔔",
        notifications_status="Statut: {status}",
        notifications_explanation="Lorsqu'activees, vous recevrez des notifications Telegram avant vos reunions (selon les temps de rappel que vous definissez).",
        select_option="Selectionnez une option:",
        enable_button="Activer",
        disable_button="Desactiver",
        current_suffix="(actuel)",
        notifications_updated="{emoji} Notifications de reunions {status}.",
        will_receive_reminders="Vous recevrez maintenant des rappels avant vos reunions.",
        will_not_receive_reminders="Vous ne recevrez plus de rappels de reunions.",
        select_language="🌍 Selectionnez votre langue preferee:",
        language_updated="✅ Langue mise a jour avec succes!",
        privacy_title="**Paramètres de Confidentialité** 🔒",
        privacy_username_invites="Autoriser les invitations par @nom d'utilisateur",
        privacy_enabled_desc="D'autres peuvent vous inviter aux réunions en utilisant votre @nom d'utilisateur",
        privacy_disabled_desc="Seules les invitations directes par email fonctionneront",
        privacy_updated="{emoji} Invitations par nom d'utilisateur {status}.",
    ),
    meetings=MeetingsTranslations(
        upcoming_meetings="**Prochaines Reunions** 📅",
        no_upcoming_meetings="Aucune reunion a venir trouvee.",
        use_cancel_hint="_Utilisez /cancel pour annuler une reunion_",
        attendees_count="👥 {count} participant(s)",
        select_meeting_to_cancel="**Selectionnez une reunion a annuler:**",
        page_info="Page {current}/{total}",
        total_meetings="{count} reunions au total",
        previous_button="⬅️ Precedent",
        next_button="Suivant ➡️",
        dont_cancel_button="❌ Ne rien annuler",
        no_meeting_cancelled="✅ Aucune reunion annulee.",
        cancelling_meeting="Annulation de la reunion...",
        meeting_cancelled="✅ Reunion annulee: **{title}**",
        attendees_notified="_Les participants seront automatiquement notifies._",
        cancel_not_your_menu="❌ Erreur: Ce n'est pas votre menu d'annulation.",
        session_expired="❌ Erreur: Session expiree. Veuillez utiliser /cancel a nouveau.",
        meeting_not_found="❌ Erreur: Reunion non trouvee. Veuillez utiliser /cancel a nouveau.",
    ),
    inline=InlineTranslations(
        how_to_create="Comment creer une reunion",
        inline_help_description='Tapez: 14:30 "Titre de Reunion" email@exemple.com',
        inline_help_message='Pour creer une reunion, tapez:\n@handycalbot 14:30 "Titre de Reunion" email@exemple.com\n\nFormat: HEURE [DATE] "TITRE" [EMAILS]',
        please_start_first_title="Veuillez d'abord demarrer le bot",
        please_start_first_description="Cliquez pour ouvrir le bot et executer /start",
        please_start_first_message="Veuillez d'abord demarrer @handycalbot en envoyant /start",
        could_not_parse="Impossible d'analyser la reunion",
        parse_error_description='Utilisez le format: 14:30 "Titre de Reunion" emails...',
        parse_error_message="Impossible d'analyser la reunion. Utilisez le format:\n14:30 \"Titre de Reunion\" email@exemple.com\n\nL'heure et le titre entre guillemets sont requis.\nAjoutez r 10m pour un rappel, ou juste r pour le defaut.",
        calendar_not_connected_warning="⚠️ Calendrier non connecte - /connect d'abord",
        attendees_label="👥 {count} participant(s)",
        today="aujourd'hui",
        create_meeting_button="Creer Reunion",
        cancel_button="Annuler",
        creating_meeting="Creation de la reunion...",
        meeting_data_expired="❌ Erreur: Donnees de reunion expirees. Veuillez reessayer.",
        not_your_meeting="❌ Ce n'est pas votre reunion!",
        meeting_created="Reunion creee!",
        reminder_label="🔔 Rappel: {reminder} avant",
        invitations_sent="📧 Invitations envoyees a:",
        attendees_will_receive="_Ces participants recevront automatiquement une invitation de calendrier._",
        add_to_calendar_button="📅 Ajouter a Mon Calendrier",
        not_listed_add_calendar="_Pas dans la liste? Cliquez ci-dessous pour ajouter a votre calendrier:_",
        click_to_add_calendar="_Cliquez ci-dessous pour ajouter a votre calendrier:_",
        meeting_cancelled="✅ Reunion annulee.",
        username_registered="enregistré",
        username_privacy_disabled="confidentialité désactivée",
        username_not_found="non trouvé",
        pending_invites_note="⏳ Pas encore inscrit:",
        rate_limit_warning="⚠️ Trop de recherches de nom d'utilisateur. Réessayez plus tard.",
        no_calendar_users_note="⚠️ Inscrit mais calendrier non connecté:",
        privacy_disabled_users_note="🔒 Confidentialité désactivée (invitation non envoyée):",
        register_link_text="S'inscrire",
        # Edit menu
        edit_button="Modifier",
        edit_menu_title="✏️ *Modifier la Reunion*\n\nQue souhaitez-vous modifier?",
        edit_title_button="📝 Titre",
        edit_time_button="🕐 Heure",
        edit_date_button="📅 Date",
        edit_duration_button="⏱️ Duree",
        edit_reminder_button="🔔 Rappel",
        edit_attendees_button="👥 Participants",
        edit_link_button="🔗 Ajouter Lien",
        back_button="↩️ Retour",
        done_editing_button="✅ Termine",
        # Edit prompts
        enter_new_title='📝 *Entrez le nouveau titre*\n\nActuel: "{current}"\n\nTapez le nouveau titre et envoyez.',
        enter_new_time="🕐 *Entrez la nouvelle heure*\n\nActuelle: {current}\n\nTapez la nouvelle heure (HH:MM) et envoyez.",
        enter_new_date="📅 *Entrez la nouvelle date*\n\nActuelle: {current}\n\nTapez la nouvelle date (JJ-MM-AAAA) et envoyez.",
        select_duration="⏱️ *Selectionnez la Duree*",
        select_reminder="🔔 *Selectionnez le Rappel*",
        # Attendees
        current_attendees="*Participants actuels:*",
        add_attendee_prompt="👥 *Ajouter Participant*\n\nTapez une adresse email ou @nomutilisateur et envoyez.",
        recent_contacts_title="*Contacts recents:*",
        no_recent_contacts="Pas de contacts recents",
        type_manually_button="✍️ Taper email/@nomutilisateur",
        remove_attendee_button="🗑️",
        attendee_added="✅ Participant ajoute: {attendee}",
        attendee_removed="✅ Participant supprime: {attendee}",
        invalid_email_format="❌ Format invalide. Utilisez email@exemple.com ou @nomutilisateur",
        no_attendees="Aucun participant pour le moment",
        # Link
        add_link_title="🔗 *Lien de Reunion*",
        invalid_link_format="❌ Lien invalide. Veuillez entrer une URL commençant par http:// ou https://",
        invalid_time_format="❌ Format d'heure invalide. Essayez 14:00, 2pm ou 14.30",
        invalid_date_format="❌ Format de date invalide. Essayez demain, Jan 20 ou 20-01",
        auto_google_meet="🎥 Auto Google Meet",
        auto_zoom_meeting="📹 Réunion Zoom automatique",
        paste_custom_link="📋 Coller Lien Personnalise",
        enter_link_prompt="🔗 *Entrez le lien de reunion*\n\nCollez l'URL de votre reunion.",
        link_added="✅ Lien ajoute",
        link_removed="✅ Lien supprime",
        remove_link_button="🗑️ Supprimer Lien",
        google_meet_label="🎥 Google Meet",
        zoom_meeting_label="📹 Réunion Zoom",
        zoom_not_connected="Zoom non connecté. Utilisez d'abord /connectzoom.",
        custom_link_label="🔗 Lien de Reunion",
        # Updates
        field_updated="✅ {field} mis a jour",
        meeting_updated="Reunion mise a jour",
        # Duration options
        duration_15_min="15 min",
        duration_30_min="30 min",
        duration_45_min="45 min",
        duration_1_hour="1 heure",
        duration_1_5_hours="1,5 heures",
        duration_2_hours="2 heures",
        # Reminder options
        reminder_none="Aucun",
        reminder_5_min="5 min",
        reminder_10_min="10 min",
        reminder_15_min="15 min",
        reminder_30_min="30 min",
        reminder_1_hour="1 heure",
        reminder_1_day="1 jour",
        # Cancel edit
        cancel_edit_button="❌ Annuler",
        edit_cancelled="Modification annulee",
        # Private chat prompts (for text input redirect)
        continue_in_private="Pour modifier ceci, continuez en chat privé:",
        open_private_chat="💬 Ouvrir Chat Privé",
        session_expired_restart="Session expirée. Veuillez recommencer l'édition depuis le message original.",
        edit_complete_return="✅ Terminé! Le message a été mis à jour.",
        back_to_chat_button="↩️ Retour au Chat",
        # Time selection grid
        select_time_title="🕐 *Sélectionner l'Heure*",
        time_morning="Matin",
        time_afternoon="Après-midi",
        custom_time_button="⌨️ Personnalisé",
        # Date selection grid
        select_date_title="📅 *Sélectionner la Date*",
        date_today="Aujourd'hui",
        date_tomorrow="Demain",
        date_day_after="Après-demain",
        date_in_3_days="Dans 3 jours",
        date_in_a_week="Dans une semaine",
        custom_date_button="⌨️ Personnalisé",
    ),
    donation=DonationTranslations(
        support_title="**Soutenez HandyCalBot** ⭐",
        support_description="Si vous trouvez ce bot utile, considerez soutenir son developpement avec des Telegram Stars!",
        support_helps="Votre soutien aide a maintenir le bot en fonctionnement et permet de nouvelles fonctionnalites.",
        select_amount="Selectionnez un montant:",
        custom_amount_button="💫 Montant Personnalise",
        custom_amount_prompt="**Don Personnalise** 💫\n\nVeuillez entrer le nombre de Stars que vous souhaitez donner (1-10000):",
        invalid_amount="Veuillez entrer un montant valide entre 1 et 10000 Stars.",
        invalid_number="Veuillez entrer un nombre valide (1-10000).",
        donation_error="Desole, une erreur s'est produite lors du traitement de votre don. Veuillez reessayer plus tard.",
        thank_you="**Merci pour votre don!** 🙏",
        you_donated="Vous avez donne {amount} Telegram Stars. Votre soutien compte beaucoup!",
        thank_you_running="Merci d'aider a maintenir HandyCalBot en fonctionnement! ⭐",
    ),
    reminder=ReminderTranslations(
        meeting_reminder="🔔 *Rappel de Reunion*",
        starting_in="Commence dans {time}",
    ),
    feedback=FeedbackTranslations(
        feedback_title="📝 **Commentaires**",
        feedback_prompt="Veuillez decrire vos commentaires, rapport de bug ou suggestion.",
        feedback_abort_hint="Tapez /abort pour annuler.",
        feedback_received="✅ Merci pour vos commentaires!",
        feedback_thank_you="Votre message a ete recu et sera examine.",
    ),
    commands=CommandTranslations(
        start="Demarrer le bot et voir bienvenue",
        help="Afficher l'aide et les instructions",
        meetings="Lister les prochaines reunions",
        cancel="Annuler une reunion",
        connect="Connecter Google Calendar",
        disconnect="Deconnecter Google Calendar",
        settings="Voir vos parametres",
        timezone="Changer le fuseau horaire",
        duration="Definir la duree par defaut",
        reminder="Definir le rappel par defaut",
        notifications="Activer/desactiver notifications",
        privacy="Paramètres de confidentialité pour les invitations",
        language="Changer la langue",
        donate="Soutenir le bot avec des Stars",
        feedback="Envoyer un commentaire ou signaler un bug",
    ),
)
