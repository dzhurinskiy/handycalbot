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
Bienvenue sur *HandyCalBot*!

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
*Aide HandyCalBot*

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
    ),
    settings=SettingsTranslations(
        your_settings="**Vos Parametres**",
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
        connect_button="Connecter Google Calendar",
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
        notifications_title="**Notifications de Reunions**",
        notifications_status="Statut: {status}",
        notifications_explanation="Lorsqu'activees, vous recevrez des notifications Telegram avant vos reunions (selon les temps de rappel que vous definissez).",
        select_option="Selectionnez une option:",
        enable_button="Activer",
        disable_button="Desactiver",
        current_suffix="(actuel)",
        notifications_updated="{emoji} Notifications de reunions {status}.",
        will_receive_reminders="Vous recevrez maintenant des rappels avant vos reunions.",
        will_not_receive_reminders="Vous ne recevrez plus de rappels de reunions.",
        select_language="Selectionnez votre langue preferee:",
        language_updated="✅ Langue mise a jour avec succes!",
    ),
    meetings=MeetingsTranslations(
        upcoming_meetings="**Prochaines Reunions**",
        no_upcoming_meetings="Aucune reunion a venir trouvee.",
        use_cancel_hint="_Utilisez /cancel pour annuler une reunion_",
        attendees_count="{count} participant(s)",
        select_meeting_to_cancel="**Selectionnez une reunion a annuler:**",
        page_info="Page {current}/{total}",
        total_meetings="{count} reunions au total",
        previous_button="Precedent",
        next_button="Suivant",
        dont_cancel_button="Ne rien annuler",
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
        attendees_label="{count} participant(s)",
        today="aujourd'hui",
        create_meeting_button="Creer Reunion",
        cancel_button="Annuler",
        creating_meeting="Creation de la reunion...",
        meeting_data_expired="❌ Erreur: Donnees de reunion expirees. Veuillez reessayer.",
        not_your_meeting="❌ Ce n'est pas votre reunion!",
        meeting_created="Reunion creee!",
        reminder_label="Rappel: {reminder} avant",
        invitations_sent="Invitations envoyees a:",
        attendees_will_receive="_Ces participants recevront automatiquement une invitation de calendrier._",
        add_to_calendar_button="Ajouter a Mon Calendrier",
        not_listed_add_calendar="_Pas dans la liste? Cliquez ci-dessous pour ajouter a votre calendrier:_",
        click_to_add_calendar="_Cliquez ci-dessous pour ajouter a votre calendrier:_",
        meeting_cancelled="✅ Reunion annulee.",
    ),
    donation=DonationTranslations(
        support_title="**Soutenez HandyCalBot**",
        support_description="Si vous trouvez ce bot utile, considerez soutenir son developpement avec des Telegram Stars!",
        support_helps="Votre soutien aide a maintenir le bot en fonctionnement et permet de nouvelles fonctionnalites.",
        select_amount="Selectionnez un montant:",
        custom_amount_button="Montant Personnalise",
        custom_amount_prompt="**Don Personnalise**\n\nVeuillez entrer le nombre de Stars que vous souhaitez donner (1-10000):",
        invalid_amount="Veuillez entrer un montant valide entre 1 et 10000 Stars.",
        invalid_number="Veuillez entrer un nombre valide (1-10000).",
        donation_error="Desole, une erreur s'est produite lors du traitement de votre don. Veuillez reessayer plus tard.",
        thank_you="**Merci pour votre don!**",
        you_donated="Vous avez donne {amount} Telegram Stars. Votre soutien compte beaucoup!",
        thank_you_running="Merci d'aider a maintenir HandyCalBot en fonctionnement!",
    ),
    reminder=ReminderTranslations(
        meeting_reminder="*Rappel de Reunion*",
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
        language="Changer la langue",
        donate="Soutenir le bot avec des Stars",
        feedback="Envoyer un commentaire ou signaler un bug",
    ),
)
