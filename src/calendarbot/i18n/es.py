"""Spanish translations for CalendarBot."""

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
        please_start_first="Por favor, ejecuta /start primero.",
        cancelled="Cancelado.",
        error_user_not_found="Error: Usuario no encontrado.",
    ),
    start=StartTranslations(
        welcome_message="""
Bienvenido a *HandyCalBot*!

Te ayudo a programar reuniones directamente desde Telegram.

*Inicio Rapido:*
1. Conecta tu Google Calendar con /connect
2. Crea reuniones escribiendo @handycalbot en cualquier chat

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
/donate - Apoyar al bot
""",
        help_message="""
*Ayuda de HandyCalBot*

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
/donate - Apoyar al bot con Stars
""",
        timezone_detected="He configurado tu zona horaria como `{timezone}` basandome en tu idioma de Telegram. Usa /timezone para cambiarlo si es necesario.",
        support_button="Apoyar HandyCalBot",
    ),
    settings=SettingsTranslations(
        your_settings="**Tu Configuracion**",
        timezone_label="Zona Horaria",
        duration_label="Duracion Predeterminada",
        reminder_label="Recordatorio Predeterminado",
        notifications_label="Notificaciones",
        google_calendar_label="Google Calendar",
        change_settings="**Cambiar Configuracion:**",
        connected="Conectado",
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
        connect_button="Conectar Google Calendar",
        calendar_disconnected="Google Calendar desconectado exitosamente.\nUsa /connect para vincularlo de nuevo.",
        no_calendar_connected="No hay calendario conectado.",
        select_timezone="Selecciona tu zona horaria o escribela manualmente (ej., `Europe/Madrid`):",
        timezone_set="Zona horaria establecida: `{timezone}`",
        timezone_set_ready='Zona horaria establecida: `{timezone}`\n\nTodo listo! Crea reuniones usando:\n`@handycalbot 14:30 "Titulo de Reunion"`',
        invalid_timezone="Zona horaria invalida: `{timezone}`\nPor favor usa una zona horaria valida como `Europe/Madrid` o `America/Mexico_City`.",
        select_duration="Selecciona la duracion predeterminada de reuniones:",
        duration_set="Duracion predeterminada establecida: {duration} minutos",
        select_reminder="Selecciona el recordatorio predeterminado para nuevas reuniones:\n\n_Puedes sobrescribirlo por reunion usando `r 10m` en tu consulta en linea._",
        reminder_set="Recordatorio predeterminado establecido: {reminder}",
        reminder_override_hint="_Usa `r` en tu consulta para aplicar este predeterminado, o `r 10m` para sobrescribirlo con un tiempo especifico._",
        notifications_title="**Notificaciones de Reuniones**",
        notifications_status="Estado: {status}",
        notifications_explanation="Cuando esta habilitado, recibiras notificaciones de Telegram antes de tus reuniones (basado en los tiempos de recordatorio que configures).",
        select_option="Selecciona una opcion:",
        enable_button="Habilitar",
        disable_button="Deshabilitar",
        current_suffix="(actual)",
        notifications_updated="{emoji} Notificaciones de reuniones {status}.",
        will_receive_reminders="Ahora recibiras recordatorios antes de tus reuniones.",
        will_not_receive_reminders="Ya no recibiras recordatorios de reuniones.",
        select_language="Selecciona tu idioma preferido:",
        language_updated="Idioma actualizado exitosamente!",
    ),
    meetings=MeetingsTranslations(
        upcoming_meetings="**Proximas Reuniones**",
        no_upcoming_meetings="No se encontraron proximas reuniones.",
        use_cancel_hint="_Usa /cancel para cancelar una reunion_",
        attendees_count="{count} asistente(s)",
        select_meeting_to_cancel="**Selecciona una reunion para cancelar:**",
        page_info="Pagina {current}/{total}",
        total_meetings="{count} reuniones en total",
        previous_button="Anterior",
        next_button="Siguiente",
        dont_cancel_button="No cancelar nada",
        no_meeting_cancelled="No se cancelo ninguna reunion.",
        cancelling_meeting="Cancelando reunion...",
        meeting_cancelled="Reunion cancelada: **{title}**",
        attendees_notified="_Los asistentes seran notificados automaticamente._",
        cancel_not_your_menu="Error: Este no es tu menu de cancelacion.",
        session_expired="Error: Sesion expirada. Por favor usa /cancel de nuevo.",
        meeting_not_found="Error: Reunion no encontrada. Por favor usa /cancel de nuevo.",
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
        calendar_not_connected_warning="Calendario no conectado - /connect primero",
        attendees_label="{count} asistente(s)",
        today="hoy",
        create_meeting_button="Crear Reunion",
        cancel_button="Cancelar",
        creating_meeting="Creando reunion...",
        meeting_data_expired="Error: Datos de reunion expirados. Por favor intenta de nuevo.",
        not_your_meeting="Esta no es tu reunion!",
        meeting_created="Reunion creada!",
        reminder_label="Recordatorio: {reminder} antes",
        invitations_sent="Invitaciones enviadas a:",
        attendees_will_receive="_Estos asistentes recibiran una invitacion de calendario automaticamente._",
        add_to_calendar_button="Agregar a Mi Calendario",
        not_listed_add_calendar="_No estas en la lista? Haz clic abajo para agregar a tu calendario:_",
        click_to_add_calendar="_Haz clic abajo para agregar a tu calendario:_",
        meeting_cancelled="Reunion cancelada.",
    ),
    donation=DonationTranslations(
        support_title="**Apoya a HandyCalBot**",
        support_description="Si encuentras util este bot, considera apoyar su desarrollo con Telegram Stars!",
        support_helps="Tu apoyo ayuda a mantener el bot funcionando y permite nuevas funciones.",
        select_amount="Selecciona una cantidad:",
        custom_amount_button="Cantidad Personalizada",
        custom_amount_prompt="**Donacion Personalizada**\n\nPor favor ingresa el numero de Stars que deseas donar (1-10000):",
        invalid_amount="Por favor ingresa una cantidad valida entre 1 y 10000 Stars.",
        invalid_number="Por favor ingresa un numero valido (1-10000).",
        donation_error="Lo siento, hubo un error procesando tu donacion. Por favor intenta mas tarde.",
        thank_you="**Gracias por tu donacion!**",
        you_donated="Donaste {amount} Telegram Stars. Tu apoyo significa mucho!",
        thank_you_running="Gracias por ayudar a mantener HandyCalBot funcionando!",
    ),
    reminder=ReminderTranslations(
        meeting_reminder="*Recordatorio de Reunion*",
        starting_in="Comienza en {time}",
    ),
)
