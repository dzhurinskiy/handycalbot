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
1️⃣ Conecta tu calendario con /connect
2️⃣ Crea reuniones escribiendo @handycalbot en cualquier chat

*Uso en Linea:*
`@handycalbot 14:30 "Titulo de Reunion" email@ejemplo.com`
`@handycalbot 10:00 25-01-2026 "Sincronizacion"`
`@handycalbot 14:30 "Reunion" r 10m` (con recordatorio)

*Comandos:*
/connect - Conectar calendario o Zoom
/disconnect - Desconectar servicios
/meetings - Ver y gestionar reuniones
/settings - Ver tu configuracion
/help - Mostrar ayuda completa

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

*Comandos:*
/connect - Conectar calendario o Zoom
/disconnect - Desconectar servicios
/meetings - Ver y gestionar reuniones
/settings - Ver tu configuracion
/timezone - Establecer zona horaria
/duration - Establecer duracion predeterminada
/reminder - Establecer recordatorio predeterminado
/notifications - Alternar notificaciones
/privacy - Configuracion de privacidad
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
        outlook_calendar_label="Outlook Calendar",
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
        # Zoom Connect/Disconnect
        zoom_already_connected="¡Zoom ya está conectado!\nUsa /disconnectzoom para desvincularlo primero.",
        click_to_connect_zoom="Haz clic en el botón de abajo para conectar tu cuenta de Zoom.\n\nSerás redirigido a Zoom para autorizar el acceso.",
        connect_zoom_button="📹 Conectar Zoom",
        zoom_disconnected="✅ Zoom desconectado correctamente.\nUsa /connectzoom para vincularlo de nuevo.",
        no_zoom_connected="No hay cuenta de Zoom conectada.",
        # Outlook Connect/Disconnect
        outlook_already_connected="¡Outlook Calendar ya está conectado!\nUsa /disconnectoutlook para desvincularlo primero.",
        click_to_connect_outlook="Haz clic en el botón de abajo para conectar tu Microsoft Outlook Calendar.\n\nSerás redirigido a Microsoft para autorizar el acceso.",
        connect_outlook_button="🔗 Conectar Outlook Calendar",
        outlook_disconnected="✅ Outlook Calendar desconectado correctamente.\nUsa /connectoutlook para vincularlo de nuevo.",
        no_outlook_connected="No hay calendario Outlook conectado.",
        connect_outlook_mode_title="**Conectar Outlook Calendar**\n\nElige el modo de conexión:",
        outlook_connected_status="**Outlook Calendar Conectado** ✅\n\nModo actual: {mode}\n\nPuedes cambiar de modo o desconectar abajo:",
        # Privacy mode selection
        connect_mode_title="**Conectar Google Calendar**\n\nElige el modo de conexión:",
        connect_full_access_button="📅 Acceso Completo",
        connect_privacy_mode_button="🔒 Modo Privacidad",
        connect_full_access_desc="_Acceso Completo: Crear reuniones y ver tu calendario (/meetings muestra todos los eventos)_",
        connect_privacy_mode_desc="_Modo Privacidad: Solo crear reuniones, sin lectura del calendario (/meetings muestra solo eventos creados por el bot)_",
        # Calendar connected status (mode switching)
        calendar_connected_status="**Google Calendar Conectado** ✅\n\nModo actual: {mode}\n\nPuedes cambiar de modo o desconectar abajo:",
        current_mode_full="📅 Acceso Completo",
        current_mode_privacy="🔒 Modo Privacidad",
        switch_to_full_button="📅 Cambiar a Acceso Completo",
        switch_to_privacy_button="🔒 Cambiar a Modo Privacidad",
        disconnect_button="❌ Desconectar",
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
        # Default calendar preference
        default_calendar_label="Calendario Predeterminado",
        default_calendar_requires_both="Necesitas tener tanto Google como Outlook conectados para establecer una preferencia.\n\nUsa /connect para conectar ambos.",
        default_calendar_title="**Calendario Predeterminado** 🎯",
        default_calendar_desc="Elige qué calendario usar por defecto al crear reuniones.\n\nPuedes cambiar de calendario para reuniones individuales desde el menú Editar.",
        default_calendar_updated="✅ Calendario predeterminado establecido a {calendar}.\n\nLas nuevas reuniones se crearán allí.",
        # Unified connect/disconnect
        connect_services_title="**Conectar servicios** 🔗",
        connect_select_service="Selecciona un servicio para conectar:",
        connect_another_service="Conectar otro servicio:",
        connected_services_title="**Servicios conectados**",
        manage_button="⚙️ Gestionar",
        disconnect_services_title="**Desconectar servicios** 🔌",
        disconnect_select_service="Selecciona un servicio para desconectar:",
        no_services_connected="No hay servicios conectados.\n\nUsa /connect para vincular tu calendario.",
        service_disconnected="✅ {service} desconectado correctamente.",
    ),
    meetings=MeetingsTranslations(
        upcoming_meetings="**Proximas Reuniones** 📅",
        no_upcoming_meetings="No se encontraron proximas reuniones.",
        use_cancel_hint="_Usa /cancel para cancelar una reunion_",
        attendees_count="👥 {count} asistente(s)",
        privacy_mode_note="_🔒 Modo privacidad: Mostrando solo reuniones creadas por el bot_",
        # Meeting list and detail view
        close_button="✖️ Cerrar",
        edit_button="✏️ Editar",
        cancel_meeting_button="🗑️ Cancelar",
        back_to_list_button="↩️ Volver a la Lista",
        closed="Lista de reuniones cerrada.",
        # Edit menu
        edit_menu_title="✏️ **Editar Reunión**\n\nSelecciona un campo para editar:",
        edit_title_btn="📝 Título",
        edit_time_btn="🕐 Hora",
        edit_date_btn="📅 Fecha",
        edit_duration_btn="⏱️ Duración",
        edit_attendees_btn="👥 Asistentes",
        edit_link_btn="🔗 Enlace",
        switch_to_calendar="Mover a {calendar}",
        calendar_switched="✅ Reunión movida a {calendar}.",
        field_updated="✅ {field} actualizado",
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
        auto_teams_meeting="📹 Auto Microsoft Teams",
        auto_zoom_meeting="📹 Reunión de Zoom automática",
        paste_custom_link="📋 Pegar Enlace Personalizado",
        enter_link_prompt="🔗 *Ingresa enlace de reunion*\n\nPega la URL de tu reunion.",
        link_added="✅ Enlace agregado",
        link_removed="✅ Enlace eliminado",
        remove_link_button="🗑️ Eliminar Enlace",
        google_meet_label="🎥 Google Meet",
        teams_meeting_label="📹 Microsoft Teams",
        zoom_meeting_label="📹 Reunión de Zoom",
        zoom_not_connected="Zoom no conectado. Usa /connect primero.",
        outlook_not_connected="Outlook no conectado. Usa /connect primero.",
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
        # Private chat prompts (for text input redirect)
        continue_in_private="Para editar esto, continúa en el chat privado:",
        open_private_chat="💬 Abrir Chat Privado",
        session_expired_restart="Sesión expirada. Por favor, comienza a editar de nuevo desde el mensaje original.",
        edit_complete_return="✅ ¡Listo! El mensaje ha sido actualizado.",
        back_to_chat_button="↩️ Volver al Chat",
        # Time selection grid
        select_time_title="🕐 *Seleccionar Hora*",
        time_morning="Mañana",
        time_afternoon="Tarde",
        custom_time_button="⌨️ Personalizado",
        # Date selection grid
        select_date_title="📅 *Seleccionar Fecha*",
        date_today="Hoy",
        date_tomorrow="Mañana",
        date_day_after="Pasado mañana",
        date_in_3_days="En 3 días",
        date_in_a_week="En una semana",
        custom_date_button="⌨️ Personalizado",
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
        connect="Conectar calendario o Zoom",
        disconnect="Desconectar servicios",
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
