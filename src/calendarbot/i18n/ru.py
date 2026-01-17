"""Russian translations for CalendarBot."""

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
        please_start_first="Pожалуйста, сначала выполните /start.",
        cancelled="Отменено.",
        aborted="Прервано.",
        error_user_not_found="Ошибка: Пользователь не найден.",
    ),
    start=StartTranslations(
        welcome_message="""
Добро пожаловать в *HandyCalBot*!

Я помогаю планировать встречи прямо из Telegram.

*Быстрый старт:*
1. Подключите Google Календарь с помощью /connect
2. Создавайте встречи, набирая @handycalbot в любом чате

*Использование inline:*
`@handycalbot 14:30 "Название встречи" email@example.com`
`@handycalbot 10:00 25-01-2026 "Синхронизация"`
`@handycalbot 14:30 "Встреча" r 10m` (с напоминанием)

*Все команды:*
/start - Приветственное сообщение
/help - Показать справку и использование
/connect - Подключить Google Календарь
/disconnect - Отключить календарь
/meetings - Список предстоящих встреч
/cancel - Отменить встречу
/settings - Посмотреть настройки
/timezone - Изменить часовой пояс
/duration - Установить длительность по умолчанию
/reminder - Установить напоминание по умолчанию
/notifications - Включить/выключить напоминания
/language - Изменить язык
/feedback - Отправить отзыв или сообщить об ошибке
/donate - Поддержать бота

_Сообщения об ошибках и предложения по улучшению приветствуются!_
""",
        help_message="""
*Справка HandyCalBot*

*Создание встреч (Inline):*
Введите `@handycalbot` в любом чате, затем:
- Время (обязательно): `ЧЧ:ММ` (24-часовой формат)
- Дата (опционально): `ДД-ММ-ГГГГ`
- Название (обязательно): `"Название вашей встречи"`
- Участники (опционально): `email@example.com`
- Напоминание (опционально): `r 10m` или `r 10m/30m` или просто `r`

*Формат напоминаний:*
- `r 10m` - напомнить за 10 минут
- `r 1h` - напомнить за 1 час
- `r 1d` - напомнить за 1 день
- `r 10m/30m` - несколько напоминаний
- `r` - использовать напоминание по умолчанию
- (без r) - без напоминания

*Примеры:*
`@handycalbot 14:30 "Стендап команды"`
`@handycalbot 10:00 25-01-2026 "Обзор" ivan@co.com`
`@handycalbot 16:00 "Быстрый звонок" r 15m`
`@handycalbot 14:00 "Встреча" anna@co.com r 10m/1h`

*Все команды:*
/start - Приветственное сообщение
/help - Эта справка
/connect - Подключить Google Календарь
/disconnect - Отключить календарь
/meetings - Показать предстоящие встречи
/cancel - Отменить встречу
/settings - Посмотреть настройки
/timezone - Установить часовой пояс
/duration - Установить длительность по умолчанию
/reminder - Установить напоминание по умолчанию
/notifications - Переключить уведомления
/language - Изменить язык
/feedback - Отправить отзыв или сообщить об ошибке
/donate - Поддержать бота Stars
""",
        timezone_detected="Я установил ваш часовой пояс как `{timezone}` на основе языка Telegram. Используйте /timezone для изменения.",
        support_button="⭐ Поддержать HandyCalBot",
        pending_invites_found="🎉 У вас есть ожидающие приглашения на встречи!",
        pending_invite_notification="📅 **{title}**\n🕐 {time}\nПриглашен: {inviter}",
    ),
    settings=SettingsTranslations(
        your_settings="**Ваши настройки**",
        timezone_label="Часовой пояс",
        duration_label="Длительность по умолчанию",
        reminder_label="Напоминание по умолчанию",
        notifications_label="Уведомления",
        google_calendar_label="Google Календарь",
        change_settings="**Изменить настройки:**",
        connected="Подключен",
        not_connected="Не подключен",
        enabled="Включено",
        disabled="Выключено",
        no_reminder="Без напоминания",
        before="до",
        day="день",
        days="дней",
        hour="час",
        hours="часов",
        minutes="мин",
        calendar_already_connected="Google Календарь уже подключен!\nИспользуйте /disconnect, чтобы сначала отключить.",
        click_to_connect="Нажмите кнопку ниже, чтобы подключить Google Календарь.\n\nВы будете перенаправлены в Google для авторизации.",
        connect_button="Подключить Google Календарь",
        calendar_disconnected="✅ Google Календарь успешно отключен.\nИспользуйте /connect для повторного подключения.",
        no_calendar_connected="Календарь не подключен.",
        select_timezone="Выберите часовой пояс или введите вручную (напр., `Europe/Moscow`):",
        timezone_set="✅ Часовой пояс установлен: `{timezone}`",
        timezone_set_ready='Часовой пояс установлен: `{timezone}`\n\nВсе готово! Создавайте встречи:\n`@handycalbot 14:30 "Название встречи"`',
        invalid_timezone="❌ Неверный часовой пояс: `{timezone}`\nИспользуйте корректный часовой пояс, например `Europe/Moscow` или `Europe/Kiev`.",
        select_duration="Выберите длительность встречи по умолчанию:",
        duration_set="✅ Длительность по умолчанию: {duration} минут",
        select_reminder="Выберите напоминание по умолчанию для новых встреч:\n\n_Вы можете переопределить это для каждой встречи, используя `r 10m` в inline-запросе._",
        reminder_set="Напоминание по умолчанию: {reminder}",
        reminder_override_hint="_Используйте `r` в запросе для применения по умолчанию, или `r 10m` для конкретного времени._",
        notifications_title="**Уведомления о встречах**",
        notifications_status="Статус: {status}",
        notifications_explanation="При включении вы будете получать уведомления Telegram перед встречами (на основе установленных напоминаний).",
        select_option="Выберите опцию:",
        enable_button="Включить",
        disable_button="Выключить",
        current_suffix="(текущее)",
        notifications_updated="{emoji} Уведомления о встречах {status}.",
        will_receive_reminders="Теперь вы будете получать напоминания перед встречами.",
        will_not_receive_reminders="Вы больше не будете получать напоминания о встречах.",
        select_language="Выберите предпочитаемый язык:",
        language_updated="✅ Язык успешно обновлен!",
        privacy_title="**Настройки Конфиденциальности** 🔒",
        privacy_username_invites="Разрешить приглашения по @имени пользователя",
        privacy_enabled_desc="Другие могут приглашать вас на встречи по вашему @имени пользователя",
        privacy_disabled_desc="Будут работать только прямые приглашения по email",
        privacy_updated="{emoji} Приглашения по имени пользователя {status}.",
    ),
    meetings=MeetingsTranslations(
        upcoming_meetings="**Предстоящие встречи**",
        no_upcoming_meetings="Предстоящих встреч не найдено.",
        use_cancel_hint="_Используйте /cancel для отмены встречи_",
        attendees_count="{count} участник(ов)",
        select_meeting_to_cancel="**Выберите встречу для отмены:**",
        page_info="Страница {current}/{total}",
        total_meetings="{count} всего встреч",
        previous_button="Назад",
        next_button="Далее",
        dont_cancel_button="Не отменять",
        no_meeting_cancelled="✅ Встреча не отменена.",
        cancelling_meeting="Отмена встречи...",
        meeting_cancelled="✅ Встреча отменена: **{title}**",
        attendees_notified="_Участники будут уведомлены автоматически._",
        cancel_not_your_menu="❌ Ошибка: Это не ваше меню отмены.",
        session_expired="❌ Ошибка: Сессия истекла. Используйте /cancel снова.",
        meeting_not_found="❌ Ошибка: Встреча не найдена. Используйте /cancel снова.",
    ),
    inline=InlineTranslations(
        how_to_create="Как создать встречу",
        inline_help_description='Введите: 14:30 "Название встречи" email@example.com',
        inline_help_message='Чтобы создать встречу, введите:\n@handycalbot 14:30 "Название встречи" email@example.com\n\nФормат: ВРЕМЯ [ДАТА] "НАЗВАНИЕ" [EMAIL]',
        please_start_first_title="Сначала запустите бота",
        please_start_first_description="Нажмите, чтобы открыть бота и выполнить /start",
        please_start_first_message="Сначала запустите @handycalbot, отправив /start",
        could_not_parse="Не удалось разобрать встречу",
        parse_error_description='Используйте формат: 14:30 "Название" emails...',
        parse_error_message='Не удалось разобрать встречу. Используйте формат:\n14:30 "Название встречи" email@example.com\n\nВремя и название в кавычках обязательны.\nДобавьте r 10m для напоминания или просто r для значения по умолчанию.',
        calendar_not_connected_warning="⚠️ Календарь не подключен - сначала /connect",
        attendees_label="{count} участник(ов)",
        today="сегодня",
        create_meeting_button="Создать встречу",
        cancel_button="Отмена",
        creating_meeting="Создание встречи...",
        meeting_data_expired="❌ Ошибка: Данные встречи устарели. Попробуйте снова.",
        not_your_meeting="❌ Это не ваша встреча!",
        meeting_created="Встреча создана!",
        reminder_label="Напоминание: за {reminder}",
        invitations_sent="Приглашения отправлены:",
        attendees_will_receive="_Эти участники автоматически получат приглашение в календарь._",
        add_to_calendar_button="📅 Добавить в мой календарь",
        not_listed_add_calendar="_Не в списке? Нажмите ниже, чтобы добавить в свой календарь:_",
        click_to_add_calendar="_Нажмите ниже, чтобы добавить в свой календарь:_",
        meeting_cancelled="✅ Встреча отменена.",
        username_registered="зарегистрирован",
        username_privacy_disabled="конфиденциальность отключена",
        username_not_found="не найден",
        pending_invites_note="⏳ Ещё не зарегистрированы:",
        rate_limit_warning="⚠️ Слишком много поисков пользователей. Попробуйте позже.",
        no_calendar_users_note="⚠️ Зарегистрированы, но календарь не подключён:",
        privacy_disabled_users_note="🔒 Конфиденциальность отключена (приглашение не отправлено):",
        register_link_text="Зарегистрироваться",
    ),
    donation=DonationTranslations(
        support_title="**Поддержите HandyCalBot**",
        support_description="Если бот полезен, поддержите его развитие с помощью Telegram Stars!",
        support_helps="Ваша поддержка помогает поддерживать бота и добавлять новые функции.",
        select_amount="Выберите сумму:",
        custom_amount_button="Другая сумма",
        custom_amount_prompt="**Произвольный донат**\n\nВведите количество Stars для пожертвования (1-10000):",
        invalid_amount="Введите корректную сумму от 1 до 10000 Stars.",
        invalid_number="Введите корректное число (1-10000).",
        donation_error="Извините, произошла ошибка при обработке пожертвования. Попробуйте позже.",
        thank_you="**Спасибо за пожертвование!**",
        you_donated="Вы пожертвовали {amount} Telegram Stars. Ваша поддержка очень важна!",
        thank_you_running="Спасибо за поддержку HandyCalBot!",
    ),
    reminder=ReminderTranslations(
        meeting_reminder="*Напоминание о встрече*",
        starting_in="Начало через {time}",
    ),
    feedback=FeedbackTranslations(
        feedback_title="📝 **Обратная связь**",
        feedback_prompt="Пожалуйста, опишите ваш отзыв, отчет об ошибке или предложение.",
        feedback_abort_hint="Введите /abort для отмены.",
        feedback_received="✅ Спасибо за ваш отзыв!",
        feedback_thank_you="Ваше сообщение получено и будет рассмотрено.",
    ),
    commands=CommandTranslations(
        start="Запустить бота и приветствие",
        help="Показать справку и инструкции",
        meetings="Список предстоящих встреч",
        cancel="Отменить встречу",
        connect="Подключить Google Календарь",
        disconnect="Отключить Google Календарь",
        settings="Посмотреть настройки",
        timezone="Изменить часовой пояс",
        duration="Установить длительность по умолчанию",
        reminder="Установить напоминание по умолчанию",
        notifications="Вкл/выкл уведомления",
        privacy="Настройки конфиденциальности для приглашений",
        language="Изменить язык",
        donate="Поддержать бота Stars",
        feedback="Отправить отзыв или сообщить об ошибке",
    ),
)
