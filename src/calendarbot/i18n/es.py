"""Spanish translations for CalendarBot."""

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
        please_start_first="Por favor, ejecuta /start primero.",
        cancelled="Cancelado.",
        aborted="Abortado.",
        error_user_not_found="Error: Usuario no encontrado.",
    ),
    start=StartTranslations(
        welcome_message="""
Bienvenido a *HandyCalBot*! 📅

Te ayudo a programar reuniones directamente desde Telegram.

*Inicio Rapido:*
1️⃣ Conecta tu Google Calendar con /connect
2️⃣ Crea reuniones escribiendo @handycalbot en cualquier chat

*Uso en Linea:*
`@handycalbot 14:30 "Titulo de Reunion" email@ejemplo.com`
`@handycalbot 10:00 25-01-2026 "Sincronizacion"`
`@handycalbot 14:30 "Reunion" r 10m` (con recordatorio)

*Todos los Comandos:*
/start - Mensaje de bienvenida
/help - Mostrar ayuda y uso
/connect - Conectar Google Calendar
/disconnect - Desconectar calendario
/meetings - Listar proximas reuniones
/cancel - Cancelar una reunion
/settings - Ver tu configuracion
/timezone - Cambiar zona horaria
/duration - Establecer duracion predeterminada
/reminder - Establecer recordatorio predeterminado
/notifications - Alternar recordatorios
/language - Cambiar idioma
/feedback - Enviar comentarios o reportar errores
/donate - Apoyar al bot

_¡Los reportes de errores y sugerencias de mejora son bienvenidos!_
""",
        help_message="""
*Ayuda de HandyCalBot* 📅

*Crear Reuniones (En Linea):*
Escribe `@handycalbot` en cualquier chat seguido de:
- Hora (requerida): `HH:MM` (formato 24 horas)
- Fecha (opcional): `DD-MM-YYYY`
- Titulo (requerido): `"Titulo de tu Reunion"`
- Asistentes (opcional): `email@ejemplo.com`
- Recordatorio (opcional): `r 10m` o `r 10m/30m` o solo `r`

*Formato de Recordatorio:*
- `r 10m` - recordar 10 minutos antes
- `r 1h` - recordar 1 hora antes
- `r 1d` - recordar 1 dia antes
- `r 10m/30m` - multiples recordatorios
- `r` - usar recordatorio predeterminado
- (sin r) - sin recordatorio

*Ejemplos:*
`@handycalbot 14:30 "Reunion de Equipo"`
`@handycalbot 10:00 25-01-2026 "Revision" juan@co.com`
`@handycalbot 16:00 "Llamada Rapida" r 15m`
`@handycalbot 14:00 "Reunion" ana@co.com r 10m/1h`

*Todos los Comandos:*
/start - Mensaje de bienvenida
/help - Este mensaje de ayuda
/connect - Conectar Google Calendar
/disconnect - Desconectar calendario
/meetings - Mostrar proximas reuniones
/cancel - Cancelar una reunion
/settings - Ver tu configuracion
/timezone - Establecer zona horaria
/duration - Establecer duracion predeterminada
/reminder - Establecer recordatorio predeterminado
/notifications - Alternar notificaciones
/language - Cambiar idioma
/feedback - Enviar comentarios o reportar errores
/donate - Apoyar al bot con Stars
""",
        timezone_detected="He configurado tu zona horaria como `{timezone}` basandome en tu idioma de Telegram. Usa /timezone para cambiarlo si es necesario.",
        support_button="⭐ Apoyar HandyCalBot",
        pending_invites_found="🎉 Tienes invitaciones de reunion pendientes!",
        pending_invite_notification="📅 **{title}**\n🕐 {time}\nInvitado por: {inviter}",
    ),
    settings=SettingsTranslations(
        your_settings="**Tu Configuracion** ⚙️",
        timezone_label="Zona Horaria",
        duration_label="Duracion Predeterminada",
        reminder_label="Recordatorio Predeterminado",
        notifications_label="Notificaciones",
        google_calendar_label="Google Calendar",
        change_settings="**Cambiar Configuracion:**",
        connected="✅ Conectado",
        not_connected="No conectado",
        enabled="Habilitado",
        disabled="Deshabilitado",
        no_reminder="Sin recordatorio",
        before="antes",
        day="dia",
        days="dias",
        hour="hora",
        hours="horas",
        minutes="min",
        calendar_already_connected="Google Calendar ya esta conectado!\nUsa /disconnect para desvincularlo primero.",
        click_to_connect="Haz clic en el boton de abajo para conectar tu Google Calendar.\n\nSeras redirigido a Google para autorizar el acceso.",
        connect_button="🔗 Conectar Google Calendar",
        calendar_disconnected="✅ Google Calendar desconectado exitosamente.\nUsa /connect para vincularlo de nuevo.",
        no_calendar_connected="No hay calendario conectado.",
        select_timezone="Selecciona tu zona horaria o escribela manualmente (ej., `Europe/Madrid`):",
        timezone_set="✅ Zona horaria establecida: `{timezone}`",
        timezone_set_ready='Zona horaria establecida: `{timezone}`\n\nTodo listo! Crea reuniones usando:\n`@handycalbot 14:30 "Titulo de Reunion"`',
        invalid_timezone="❌ Zona horaria invalida: `{timezone}`\nPor favor usa una zona horaria valida como `Europe/Madrid` o `America/Mexico_City`.",
        select_duration="Selecciona la duracion predeterminada de reuniones:",
        duration_set="✅ Duracion predeterminada establecida: {duration} minutos",
        select_reminder="Selecciona el recordatorio predeterminado para nuevas reuniones:\n\n_Puedes sobrescribirlo por reunion usando `r 10m` en tu consulta en linea._",
        reminder_set="Recordatorio predeterminado establecido: {reminder}",
        reminder_override_hint="_Usa `r` en tu consulta para aplicar este predeterminado, o `r 10m` para sobrescribirlo con un tiempo especifico._",
        notifications_title="**Notificaciones de Reuniones** 🔔",
        notifications_status="Estado: {status}",
        notifications_explanation="Cuando esta habilitado, recibiras notificaciones de Telegram antes de tus reuniones (basado en los tiempos de recordatorio que configures).",
        select_option="Selecciona una opcion:",
        enable_button="Habilitar",
        disable_button="Deshabilitar",
        current_suffix="(actual)",
        notifications_updated="{emoji} Notificaciones de reuniones {status}.",
        will_receive_reminders="Ahora recibiras recordatorios antes de tus reuniones.",
        will_not_receive_reminders="Ya no recibiras recordatorios de reuniones.",
        select_language="🌍 Selecciona tu idioma preferido:",
        language_updated="✅ Idioma actualizado exitosamente!",
        privacy_title="**Configuracion de Privacidad** 🔒",
        privacy_username_invites="Permitir invitaciones por @usuario",
        privacy_enabled_desc="Otros pueden invitarte a reuniones usando tu @usuario",
        privacy_disabled_desc="Solo funcionaran las invitaciones directas por email",
        privacy_updated="{emoji} Invitaciones por usuario {status}.",
    ),
    meetings=MeetingsTranslations(
        upcoming_meetings="**Proximas Reuniones** 📅",
        no_upcoming_meetings="No se encontraron proximas reuniones.",
        use_cancel_hint="_Usa /cancel para cancelar una reunion_",
        attendees_count="👥 {count} asistente(s)",
        select_meeting_to_cancel="**Selecciona una reunion para cancelar:**",
        page_info="Pagina {current}/{total}",
        total_meetings="{count} reuniones en total",
        previous_button="⬅️ Anterior",
        next_button="Siguiente ➡️",
        dont_cancel_button="❌ No cancelar nada",
        no_meeting_cancelled="✅ No se cancelo ninguna reunion.",
        cancelling_meeting="Cancelando reunion...",
        meeting_cancelled="✅ Reunion cancelada: **{title}**",
        attendees_notified="_Los asistentes seran notificados automaticamente._",
        cancel_not_your_menu="❌ Error: Este no es tu menu de cancelacion.",
        session_expired="❌ Error: Sesion expirada. Por favor usa /cancel de nuevo.",
        meeting_not_found="❌ Error: Reunion no encontrada. Por favor usa /cancel de nuevo.",
    ),
    inline=InlineTranslations(
        how_to_create="Como crear una reunion",
        inline_help_description='Escribe: 14:30 "Titulo de Reunion" email@ejemplo.com',
        inline_help_message='Para crear una reunion, escribe:\n@handycalbot 14:30 "Titulo de Reunion" email@ejemplo.com\n\nFormato: HORA [FECHA] "TITULO" [EMAILS]',
        please_start_first_title="Por favor inicia el bot primero",
        please_start_first_description="Haz clic para abrir el bot y ejecutar /start",
        please_start_first_message="Por favor inicia @handycalbot primero enviando /start",
        could_not_parse="No se pudo analizar la reunion",
        parse_error_description='Usa el formato: 14:30 "Titulo de Reunion" emails...',
        parse_error_message='No se pudo analizar la reunion. Usa el formato:\n14:30 "Titulo de Reunion" email@ejemplo.com\n\nLa hora y el titulo entre comillas son requeridos.\nAgrega r 10m para recordatorio, o solo r para el predeterminado.',
        calendar_not_connected_warning="⚠️ Calendario no conectado - /connect primero",
        attendees_label="👥 {count} asistente(s)",
        today="hoy",
        create_meeting_button="Crear Reunion",
        cancel_button="Cancelar",
        creating_meeting="Creando reunion...",
        meeting_data_expired="❌ Error: Datos de reunion expirados. Por favor intenta de nuevo.",
        not_your_meeting="❌ Esta no es tu reunion!",
        meeting_created="Reunion creada!",
        reminder_label="🔔 Recordatorio: {reminder} antes",
        invitations_sent="📧 Invitaciones enviadas a:",
        attendees_will_receive="_Estos asistentes recibiran una invitacion de calendario automaticamente._",
        add_to_calendar_button="📅 Agregar a Mi Calendario",
        not_listed_add_calendar="_No estas en la lista? Haz clic abajo para agregar a tu calendario:_",
        click_to_add_calendar="_Haz clic abajo para agregar a tu calendario:_",
        meeting_cancelled="✅ Reunion cancelada.",
        username_registered="registrado",
        username_privacy_disabled="privacidad deshabilitada",
        username_not_found="no encontrado",
        pending_invites_note="⏳ Aun no registrado:",
        rate_limit_warning="⚠️ Demasiadas busquedas de usuario. Intenta mas tarde.",
        no_calendar_users_note="⚠️ Registrado pero sin calendario conectado:",
        privacy_disabled_users_note="🔒 Privacidad deshabilitada (invitacion no enviada):",
        register_link_text="Registrarse",
        # Edit menu
        edit_button="Editar",
        edit_menu_title="✏️ *Editar Reunion*\n\nQue deseas cambiar?",
        edit_title_button="📝 Titulo",
        edit_time_button="🕐 Hora",
        edit_date_button="📅 Fecha",
        edit_duration_button="⏱️ Duracion",
        edit_reminder_button="🔔 Recordatorio",
        edit_attendees_button="👥 Asistentes",
        edit_link_button="🔗 Agregar Enlace",
        back_button="↩️ Volver",
        done_editing_button="✅ Listo",
        # Edit prompts
        enter_new_title='📝 *Ingresa nuevo titulo*\n\nActual: "{current}"\n\nEscribe el nuevo titulo y envialo.',
        enter_new_time="🕐 *Ingresa nueva hora*\n\nActual: {current}\n\nEscribe la nueva hora (HH:MM) y enviala.",
        enter_new_date="📅 *Ingresa nueva fecha*\n\nActual: {current}\n\nEscribe la nueva fecha (DD-MM-YYYY) y enviala.",
        select_duration="⏱️ *Seleccionar Duracion*",
        select_reminder="🔔 *Seleccionar Recordatorio*",
        # Attendees
        current_attendees="*Asistentes actuales:*",
        add_attendee_prompt="👥 *Agregar Asistente*\n\nEscribe un correo electronico o @usuario y envialo.",
        recent_contacts_title="*Contactos recientes:*",
        no_recent_contacts="Sin contactos recientes",
        type_manually_button="✍️ Escribir correo/@usuario",
        remove_attendee_button="🗑️",
        attendee_added="✅ Asistente agregado: {attendee}",
        attendee_removed="✅ Asistente eliminado: {attendee}",
        invalid_email_format="❌ Formato invalido. Usa correo@ejemplo.com o @usuario",
        no_attendees="Sin participantes aún",
        # Link
        add_link_title="🔗 *Enlace de Reunion*",
        invalid_link_format="❌ Enlace no válido. Ingresa una URL que comience con http:// o https://",
        invalid_time_format="❌ Formato de hora no válido. Prueba 14:00, 2pm o 14.30",
        invalid_date_format="❌ Formato de fecha no válido. Prueba mañana, Jan 20 o 20-01",
        auto_google_meet="🎥 Auto Google Meet",
        paste_custom_link="📋 Pegar Enlace Personalizado",
        enter_link_prompt="🔗 *Ingresa enlace de reunion*\n\nPega la URL de tu reunion.",
        link_added="✅ Enlace agregado",
        link_removed="✅ Enlace eliminado",
        remove_link_button="🗑️ Eliminar Enlace",
        google_meet_label="🎥 Google Meet",
        custom_link_label="🔗 Enlace de Reunion",
        # Updates
        field_updated="✅ {field} actualizado",
        meeting_updated="Reunion actualizada",
        # Duration options
        duration_15_min="15 min",
        duration_30_min="30 min",
        duration_45_min="45 min",
        duration_1_hour="1 hora",
        duration_1_5_hours="1.5 horas",
        duration_2_hours="2 horas",
        # Reminder options
        reminder_none="Ninguno",
        reminder_5_min="5 min",
        reminder_10_min="10 min",
        reminder_15_min="15 min",
        reminder_30_min="30 min",
        reminder_1_hour="1 hora",
        reminder_1_day="1 dia",
        # Cancel edit
        cancel_edit_button="❌ Cancelar",
        edit_cancelled="Edicion cancelada",
    ),
    donation=DonationTranslations(
        support_title="**Apoya a HandyCalBot** ⭐",
        support_description="Si encuentras util este bot, considera apoyar su desarrollo con Telegram Stars!",
        support_helps="Tu apoyo ayuda a mantener el bot funcionando y permite nuevas funciones.",
        select_amount="Selecciona una cantidad:",
        custom_amount_button="💫 Cantidad Personalizada",
        custom_amount_prompt="**Donacion Personalizada** 💫\n\nPor favor ingresa el numero de Stars que deseas donar (1-10000):",
        invalid_amount="Por favor ingresa una cantidad valida entre 1 y 10000 Stars.",
        invalid_number="Por favor ingresa un numero valido (1-10000).",
        donation_error="Lo siento, hubo un error procesando tu donacion. Por favor intenta mas tarde.",
        thank_you="**Gracias por tu donacion!** 🙏",
        you_donated="Donaste {amount} Telegram Stars. Tu apoyo significa mucho!",
        thank_you_running="Gracias por ayudar a mantener HandyCalBot funcionando! ⭐",
    ),
    reminder=ReminderTranslations(
        meeting_reminder="🔔 *Recordatorio de Reunion*",
        starting_in="Comienza en {time}",
    ),
    feedback=FeedbackTranslations(
        feedback_title="📝 **Comentarios**",
        feedback_prompt="Por favor describe tus comentarios, reporte de error o sugerencia.",
        feedback_abort_hint="Escribe /abort para cancelar.",
        feedback_received="✅ Gracias por tus comentarios!",
        feedback_thank_you="Tu mensaje ha sido recibido y sera revisado.",
    ),
    commands=CommandTranslations(
        start="Iniciar el bot y ver bienvenida",
        help="Mostrar ayuda e instrucciones",
        meetings="Listar proximas reuniones",
        cancel="Cancelar una reunion",
        connect="Conectar Google Calendar",
        disconnect="Desconectar Google Calendar",
        settings="Ver tu configuracion",
        timezone="Cambiar zona horaria",
        duration="Establecer duracion predeterminada",
        reminder="Establecer recordatorio predeterminado",
        notifications="Alternar notificaciones",
        privacy="Configuracion de privacidad para invitaciones",
        language="Cambiar idioma",
        donate="Apoyar al bot con Stars",
        feedback="Enviar comentarios o reportar error",
    ),
)
