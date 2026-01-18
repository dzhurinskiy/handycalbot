"""Persian (Farsi) translations for CalendarBot."""

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
        please_start_first="لطفا ابتدا /start را اجرا کنید.",
        cancelled="لغو شد.",
        aborted="متوقف شد.",
        error_user_not_found="خطا: کاربر یافت نشد.",
    ),
    start=StartTranslations(
        welcome_message="""
به *HandyCalBot* خوش آمدید! 📅

من به شما کمک می‌کنم جلسات را مستقیماً از تلگرام برنامه‌ریزی کنید.

*شروع سریع:*
1️⃣ تقویم گوگل خود را با /connect متصل کنید
2️⃣ با تایپ @handycalbot در هر چت، جلسه بسازید

*استفاده اینلاین:*
`@handycalbot 14:30 "عنوان جلسه" email@example.com`
`@handycalbot 10:00 25-01-2026 "همگام‌سازی پروژه"`
`@handycalbot 14:30 "جلسه" r 10m` (با یادآوری)

*همه دستورات:*
/start - پیام خوش‌آمدگویی
/help - نمایش راهنما
/connect - اتصال تقویم گوگل
/disconnect - قطع اتصال تقویم
/meetings - لیست جلسات آینده
/cancel - لغو جلسه
/settings - مشاهده تنظیمات
/timezone - تغییر منطقه زمانی
/duration - تنظیم مدت پیش‌فرض
/reminder - تنظیم یادآوری پیش‌فرض
/notifications - فعال/غیرفعال کردن یادآوری
/language - تغییر زبان
/feedback - ارسال بازخورد یا گزارش خطا
/donate - حمایت از بات ⭐

_گزارش خطاها و پیشنهادات بهبود رابط کاربری استقبال می‌شود!_
""",
        help_message="""
*راهنمای HandyCalBot* 📅

*ایجاد جلسات (اینلاین):*
`@handycalbot` را در هر چت تایپ کنید و ادامه دهید با:
• زمان (اجباری): `HH:MM` (فرمت ۲۴ ساعته)
• تاریخ (اختیاری): `DD-MM-YYYY`
• عنوان (اجباری): `"عنوان جلسه شما"`
• شرکت‌کنندگان (اختیاری): `email@example.com`
• یادآوری (اختیاری): `r 10m` یا `r 10m/30m` یا فقط `r`

*فرمت یادآوری:*
• `r 10m` - یادآوری ۱۰ دقیقه قبل
• `r 1h` - یادآوری ۱ ساعت قبل
• `r 1d` - یادآوری ۱ روز قبل
• `r 10m/30m` - چند یادآوری
• `r` - استفاده از یادآوری پیش‌فرض
• (بدون r) - بدون یادآوری

*مثال‌ها:*
`@handycalbot 14:30 "جلسه تیمی"`
`@handycalbot 10:00 25-01-2026 "بررسی" john@co.com`
`@handycalbot 16:00 "تماس سریع" r 15m`
`@handycalbot 14:00 "جلسه" alice@co.com r 10m/1h`

*همه دستورات:*
/start - پیام خوش‌آمدگویی
/help - این پیام راهنما
/connect - اتصال تقویم گوگل
/disconnect - قطع اتصال تقویم
/meetings - نمایش جلسات آینده
/cancel - لغو جلسه
/settings - مشاهده تنظیمات
/timezone - تنظیم منطقه زمانی
/duration - تنظیم مدت پیش‌فرض جلسه
/reminder - تنظیم یادآوری پیش‌فرض
/notifications - فعال/غیرفعال کردن اعلان
/language - تغییر زبان
/feedback - ارسال بازخورد یا گزارش خطا
/donate - حمایت از بات با Stars ⭐
""",
        timezone_detected="منطقه زمانی شما به `{timezone}` تنظیم شد بر اساس زبان تلگرام. از /timezone برای تغییر استفاده کنید.",
        support_button="⭐ حمایت از HandyCalBot",
        pending_invites_found="🎉 شما دعوت‌نامه‌های جلسه در انتظار دارید!",
        pending_invite_notification="📅 **{title}**\n🕐 {time}\nدعوت‌کننده: {inviter}",
    ),
    settings=SettingsTranslations(
        your_settings="**تنظیمات شما** ⚙️",
        timezone_label="منطقه زمانی",
        duration_label="مدت پیش‌فرض",
        reminder_label="یادآوری پیش‌فرض",
        notifications_label="اعلان‌ها",
        google_calendar_label="تقویم گوگل",
        change_settings="**تغییر تنظیمات:**",
        connected="✅ متصل",
        not_connected="متصل نیست",
        enabled="فعال",
        disabled="غیرفعال",
        no_reminder="بدون یادآوری",
        before="قبل",
        day="روز",
        days="روز",
        hour="ساعت",
        hours="ساعت",
        minutes="دقیقه",
        calendar_already_connected="تقویم گوگل قبلاً متصل است!\nابتدا از /disconnect استفاده کنید.",
        click_to_connect="روی دکمه زیر کلیک کنید تا تقویم گوگل خود را متصل کنید.\n\nبه گوگل هدایت می‌شوید تا دسترسی بدهید.",
        connect_button="🔗 اتصال تقویم گوگل",
        calendar_disconnected="✅ تقویم گوگل با موفقیت قطع شد.\nاز /connect برای اتصال مجدد استفاده کنید.",
        no_calendar_connected="تقویمی متصل نیست.",
        select_timezone="منطقه زمانی خود را انتخاب کنید یا دستی وارد کنید (مثلاً `Asia/Tehran`):",
        timezone_set="✅ منطقه زمانی تنظیم شد: `{timezone}`",
        timezone_set_ready='✅ منطقه زمانی تنظیم شد: `{timezone}`\n\nآماده‌اید! جلسات بسازید با:\n`@handycalbot 14:30 "عنوان جلسه"`',
        invalid_timezone="❌ منطقه زمانی نامعتبر: `{timezone}`\nلطفاً از منطقه زمانی معتبر مثل `Asia/Tehran` استفاده کنید.",
        select_duration="مدت پیش‌فرض جلسه را انتخاب کنید:",
        duration_set="✅ مدت پیش‌فرض تنظیم شد: {duration} دقیقه",
        select_reminder="یادآوری پیش‌فرض برای جلسات جدید را انتخاب کنید:\n\n_می‌توانید برای هر جلسه با `r 10m` تغییر دهید._",
        reminder_set="یادآوری پیش‌فرض تنظیم شد: {reminder}",
        reminder_override_hint="_از `r` برای اعمال پیش‌فرض یا `r 10m` برای زمان خاص استفاده کنید._",
        notifications_title="**اعلان‌های جلسه** 🔔",
        notifications_status="وضعیت: {status}",
        notifications_explanation="وقتی فعال است، قبل از جلسات اعلان تلگرامی دریافت می‌کنید.",
        select_option="یک گزینه انتخاب کنید:",
        enable_button="فعال",
        disable_button="غیرفعال",
        current_suffix="(فعلی)",
        notifications_updated="{emoji} اعلان‌های جلسه {status}.",
        will_receive_reminders="حالا قبل از جلسات یادآوری دریافت خواهید کرد.",
        will_not_receive_reminders="دیگر یادآوری جلسه دریافت نخواهید کرد.",
        select_language="🌍 زبان مورد نظر خود را انتخاب کنید:",
        language_updated="✅ زبان با موفقیت تغییر کرد!",
        privacy_title="**تنظیمات حریم خصوصی** 🔒",
        privacy_username_invites="اجازه دعوت با @نام کاربری",
        privacy_enabled_desc="دیگران می‌توانند با @نام کاربری شما را به جلسات دعوت کنند",
        privacy_disabled_desc="فقط دعوت‌نامه‌های مستقیم ایمیلی کار خواهند کرد",
        privacy_updated="{emoji} دعوت‌نامه‌های نام کاربری {status}.",
    ),
    meetings=MeetingsTranslations(
        upcoming_meetings="**جلسات آینده** 📅",
        no_upcoming_meetings="جلسه آینده‌ای یافت نشد.",
        use_cancel_hint="_از /cancel برای لغو جلسه استفاده کنید_",
        attendees_count="👥 {count} شرکت‌کننده",
        select_meeting_to_cancel="**جلسه‌ای برای لغو انتخاب کنید:**",
        page_info="صفحه {current}/{total}",
        total_meetings="{count} جلسه در کل",
        previous_button="⬅️ قبلی",
        next_button="بعدی ➡️",
        dont_cancel_button="❌ لغو نکن",
        no_meeting_cancelled="هیچ جلسه‌ای لغو نشد.",
        cancelling_meeting="در حال لغو جلسه...",
        meeting_cancelled="✅ جلسه لغو شد: **{title}**",
        attendees_notified="_شرکت‌کنندگان به طور خودکار مطلع خواهند شد._",
        cancel_not_your_menu="❌ خطا: این منوی لغو شما نیست.",
        session_expired="❌ خطا: نشست منقضی شده. لطفاً دوباره از /cancel استفاده کنید.",
        meeting_not_found="❌ خطا: جلسه یافت نشد. لطفاً دوباره از /cancel استفاده کنید.",
    ),
    inline=InlineTranslations(
        how_to_create="نحوه ایجاد جلسه",
        inline_help_description='تایپ کنید: 14:30 "عنوان جلسه" email@example.com',
        inline_help_message='برای ایجاد جلسه تایپ کنید:\n@handycalbot 14:30 "عنوان جلسه" email@example.com\n\nفرمت: زمان [تاریخ] "عنوان" [ایمیل‌ها]',
        please_start_first_title="لطفا ابتدا بات را شروع کنید",
        please_start_first_description="کلیک کنید تا بات را باز کنید و /start بزنید",
        please_start_first_message="لطفا ابتدا @handycalbot را با ارسال /start شروع کنید",
        could_not_parse="نتوانستم جلسه را تجزیه کنم",
        parse_error_description='از فرمت استفاده کنید: 14:30 "عنوان جلسه" ایمیل‌ها...',
        parse_error_message='نتوانستم جلسه را تجزیه کنم. از فرمت استفاده کنید:\n14:30 "عنوان جلسه" email@example.com\n\nزمان و عنوان در گیومه اجباری است.\nبرای یادآوری r 10m یا فقط r اضافه کنید.',
        calendar_not_connected_warning="⚠️ تقویم متصل نیست - ابتدا /connect",
        attendees_label="👥 {count} شرکت‌کننده",
        today="امروز",
        create_meeting_button="ایجاد جلسه",
        cancel_button="لغو",
        creating_meeting="در حال ایجاد جلسه...",
        meeting_data_expired="❌ خطا: داده‌های جلسه منقضی شده. دوباره تلاش کنید.",
        not_your_meeting="❌ این جلسه شما نیست!",
        meeting_created="جلسه ایجاد شد!",
        reminder_label="🔔 یادآوری: {reminder} قبل",
        invitations_sent="📧 دعوت‌نامه‌ها ارسال شد به:",
        attendees_will_receive="_این شرکت‌کنندگان دعوت‌نامه تقویم دریافت خواهند کرد._",
        add_to_calendar_button="📅 افزودن به تقویم من",
        not_listed_add_calendar="_در لیست نیستید؟ برای افزودن به تقویم کلیک کنید:_",
        click_to_add_calendar="_برای افزودن به تقویم کلیک کنید:_",
        meeting_cancelled="جلسه لغو شد.",
        username_registered="ثبت‌شده",
        username_privacy_disabled="حریم خصوصی غیرفعال",
        username_not_found="یافت نشد",
        pending_invites_note="⏳ هنوز ثبت‌نام نشده:",
        rate_limit_warning="⚠️ جستجوی کاربران زیاد است. بعداً امتحان کنید.",
        no_calendar_users_note="⚠️ ثبت‌نام شده اما تقویم متصل نیست:",
        privacy_disabled_users_note="🔒 حریم خصوصی غیرفعال (دعوتنامه ارسال نشد):",
        register_link_text="ثبت‌نام",
        # Edit menu
        edit_button="ویرایش",
        edit_menu_title="✏️ *ویرایش جلسه*\n\nچه چیزی را می‌خواهید تغییر دهید؟",
        edit_title_button="📝 عنوان",
        edit_time_button="🕐 زمان",
        edit_date_button="📅 تاریخ",
        edit_duration_button="⏱️ مدت",
        edit_reminder_button="🔔 یادآوری",
        edit_attendees_button="👥 شرکت‌کنندگان",
        edit_link_button="🔗 افزودن لینک",
        back_button="↩️ برگشت",
        done_editing_button="✅ تمام",
        # Edit prompts
        enter_new_title="📝 *عنوان جدید را وارد کنید*\n\nفعلی: \"{current}\"\n\nعنوان جدید را تایپ و ارسال کنید.",
        enter_new_time="🕐 *زمان جدید را وارد کنید*\n\nفعلی: {current}\n\nزمان جدید (HH:MM) را تایپ و ارسال کنید.",
        enter_new_date="📅 *تاریخ جدید را وارد کنید*\n\nفعلی: {current}\n\nتاریخ جدید (DD-MM-YYYY) را تایپ و ارسال کنید.",
        select_duration="⏱️ *مدت را انتخاب کنید*",
        select_reminder="🔔 *یادآوری را انتخاب کنید*",
        # Attendees
        current_attendees="*شرکت‌کنندگان فعلی:*",
        add_attendee_prompt="👥 *افزودن شرکت‌کننده*\n\nایمیل یا @نام کاربری را تایپ و ارسال کنید.",
        recent_contacts_title="*مخاطبین اخیر:*",
        no_recent_contacts="مخاطبین اخیر وجود ندارد",
        type_manually_button="✍️ تایپ ایمیل/@نام کاربری",
        remove_attendee_button="🗑️",
        attendee_added="✅ شرکت‌کننده اضافه شد: {attendee}",
        attendee_removed="✅ شرکت‌کننده حذف شد: {attendee}",
        invalid_email_format="❌ فرمت نامعتبر. از email@example.com یا @نام کاربری استفاده کنید",
        # Link
        add_link_title="🔗 *لینک جلسه*",
        auto_google_meet="🎥 Google Meet خودکار",
        paste_custom_link="📋 چسباندن لینک سفارشی",
        enter_link_prompt="🔗 *لینک جلسه را وارد کنید*\n\nURL جلسه خود را بچسبانید.",
        link_added="✅ لینک اضافه شد",
        link_removed="✅ لینک حذف شد",
        remove_link_button="🗑️ حذف لینک",
        google_meet_label="🎥 Google Meet",
        custom_link_label="🔗 لینک جلسه",
        # Updates
        field_updated="✅ {field} به‌روز شد",
        meeting_updated="جلسه به‌روز شد",
        # Duration options
        duration_15_min="۱۵ دقیقه",
        duration_30_min="۳۰ دقیقه",
        duration_45_min="۴۵ دقیقه",
        duration_1_hour="۱ ساعت",
        duration_1_5_hours="۱.۵ ساعت",
        duration_2_hours="۲ ساعت",
        # Reminder options
        reminder_none="هیچ",
        reminder_5_min="۵ دقیقه",
        reminder_10_min="۱۰ دقیقه",
        reminder_15_min="۱۵ دقیقه",
        reminder_30_min="۳۰ دقیقه",
        reminder_1_hour="۱ ساعت",
        reminder_1_day="۱ روز",
        # Cancel edit
        cancel_edit_button="❌ لغو",
        edit_cancelled="ویرایش لغو شد",
    ),
    donation=DonationTranslations(
        support_title="**حمایت از HandyCalBot** ⭐",
        support_description="اگر این بات مفید است، با Telegram Stars از توسعه آن حمایت کنید!",
        support_helps="حمایت شما به اجرای بات و امکانات جدید کمک می‌کند.",
        select_amount="مبلغ انتخاب کنید:",
        custom_amount_button="💫 مبلغ دلخواه",
        custom_amount_prompt="**کمک مالی دلخواه** 💫\n\nتعداد Stars را وارد کنید (۱-۱۰۰۰۰):",
        invalid_amount="لطفا مبلغ معتبر بین ۱ تا ۱۰۰۰۰ Stars وارد کنید.",
        invalid_number="لطفا عدد معتبر وارد کنید (۱-۱۰۰۰۰).",
        donation_error="متأسفم، خطایی در پردازش کمک مالی رخ داد. بعداً تلاش کنید.",
        thank_you="**از کمک مالی شما متشکریم!** 🙏",
        you_donated="شما {amount} Telegram Stars کمک کردید. حمایت شما ارزشمند است!",
        thank_you_running="از کمک شما برای اجرای HandyCalBot متشکریم! ⭐",
    ),
    reminder=ReminderTranslations(
        meeting_reminder="🔔 *یادآوری جلسه*",
        starting_in="شروع در {time}",
    ),
    feedback=FeedbackTranslations(
        feedback_title="📝 **بازخورد**",
        feedback_prompt="لطفا بازخورد، گزارش خطا یا پیشنهاد خود را شرح دهید.",
        feedback_abort_hint="برای لغو /abort را تایپ کنید.",
        feedback_received="✅ از بازخورد شما متشکریم!",
        feedback_thank_you="پیام شما دریافت شد و بررسی خواهد شد.",
    ),
    commands=CommandTranslations(
        start="شروع بات و پیام خوش‌آمدگویی",
        help="نمایش راهنما و دستورالعمل‌ها",
        meetings="لیست جلسات آینده",
        cancel="لغو جلسه",
        connect="اتصال تقویم گوگل",
        disconnect="قطع تقویم گوگل",
        settings="مشاهده تنظیمات",
        timezone="تغییر منطقه زمانی",
        duration="تنظیم مدت پیش‌فرض",
        reminder="تنظیم یادآوری پیش‌فرض",
        notifications="فعال/غیرفعال کردن اعلان",
        privacy="تنظیمات حریم خصوصی برای دعوت‌نامه‌ها",
        language="تغییر زبان",
        donate="حمایت از بات با Stars",
        feedback="ارسال بازخورد یا گزارش خطا",
    ),
)
