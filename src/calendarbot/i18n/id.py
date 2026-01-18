"""Indonesian translations for CalendarBot."""

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
        please_start_first="Silakan jalankan /start terlebih dahulu.",
        cancelled="Dibatalkan.",
        aborted="Dibatalkan.",
        error_user_not_found="Error: Pengguna tidak ditemukan.",
    ),
    start=StartTranslations(
        welcome_message="""
Selamat datang di *HandyCalBot*! 📅

Saya membantu Anda menjadwalkan rapat langsung dari Telegram.

*Mulai Cepat:*
1️⃣ Hubungkan Google Calendar Anda dengan /connect
2️⃣ Buat rapat dengan mengetik @handycalbot di chat mana pun

*Penggunaan Inline:*
`@handycalbot 14:30 "Judul Rapat" email@contoh.com`
`@handycalbot 10:00 25-01-2026 "Sinkronisasi Proyek"`
`@handycalbot 14:30 "Rapat" r 10m` (dengan pengingat)

*Semua Perintah:*
/start - Pesan selamat datang
/help - Tampilkan bantuan dan penggunaan
/connect - Hubungkan Google Calendar
/disconnect - Putuskan koneksi kalender
/meetings - Daftar rapat mendatang
/cancel - Batalkan rapat
/settings - Lihat pengaturan Anda
/timezone - Ubah zona waktu
/duration - Atur durasi default
/reminder - Atur pengingat default
/notifications - Aktifkan/nonaktifkan pengingat
/language - Ubah bahasa
/feedback - Kirim masukan atau laporkan bug
/donate - Dukung bot ⭐

_Laporan bug dan saran perbaikan UI sangat diterima!_
""",
        help_message="""
*Bantuan HandyCalBot* 📅

*Membuat Rapat (Inline):*
Ketik `@handycalbot` di chat mana pun diikuti dengan:
• Waktu (wajib): `HH:MM` (format 24 jam)
• Tanggal (opsional): `DD-MM-YYYY`
• Judul (wajib): `"Judul Rapat Anda"`
• Peserta (opsional): `email@contoh.com`
• Pengingat (opsional): `r 10m` atau `r 10m/30m` atau hanya `r`

*Format Pengingat:*
• `r 10m` - ingatkan 10 menit sebelumnya
• `r 1h` - ingatkan 1 jam sebelumnya
• `r 1d` - ingatkan 1 hari sebelumnya
• `r 10m/30m` - beberapa pengingat
• `r` - gunakan pengingat default Anda
• (tanpa r) - tanpa pengingat

*Contoh:*
`@handycalbot 14:30 "Standup Tim"`
`@handycalbot 10:00 25-01-2026 "Review" john@co.com`
`@handycalbot 16:00 "Panggilan Cepat" r 15m`
`@handycalbot 14:00 "Rapat" alice@co.com r 10m/1h`

*Semua Perintah:*
/start - Pesan selamat datang
/help - Pesan bantuan ini
/connect - Hubungkan Google Calendar
/disconnect - Putuskan koneksi kalender
/meetings - Tampilkan rapat mendatang
/cancel - Batalkan rapat
/settings - Lihat pengaturan Anda
/timezone - Atur zona waktu Anda
/duration - Atur durasi rapat default
/reminder - Atur pengingat default
/notifications - Aktifkan/nonaktifkan notifikasi
/language - Ubah bahasa
/feedback - Kirim masukan atau laporkan bug
/donate - Dukung bot dengan Stars ⭐
""",
        timezone_detected="Saya telah mengatur zona waktu Anda ke `{timezone}` berdasarkan bahasa Telegram Anda. Gunakan /timezone untuk mengubahnya jika perlu.",
        support_button="⭐ Dukung HandyCalBot",
        pending_invites_found="🎉 Anda memiliki undangan rapat yang tertunda!",
        pending_invite_notification="📅 **{title}**\n🕐 {time}\nDiundang oleh: {inviter}",
    ),
    settings=SettingsTranslations(
        your_settings="**Pengaturan Anda** ⚙️",
        timezone_label="Zona Waktu",
        duration_label="Durasi Default",
        reminder_label="Pengingat Default",
        notifications_label="Notifikasi",
        google_calendar_label="Google Calendar",
        change_settings="**Ubah Pengaturan:**",
        connected="✅ Terhubung",
        not_connected="Tidak terhubung",
        enabled="Aktif",
        disabled="Nonaktif",
        no_reminder="Tanpa pengingat",
        before="sebelumnya",
        day="hari",
        days="hari",
        hour="jam",
        hours="jam",
        minutes="menit",
        calendar_already_connected="Google Calendar sudah terhubung!\nGunakan /disconnect untuk memutuskan koneksi terlebih dahulu.",
        click_to_connect="Klik tombol di bawah untuk menghubungkan Google Calendar Anda.\n\nAnda akan diarahkan ke Google untuk mengotorisasi akses.",
        connect_button="🔗 Hubungkan Google Calendar",
        calendar_disconnected="✅ Google Calendar berhasil diputuskan.\nGunakan /connect untuk menghubungkannya lagi.",
        no_calendar_connected="Tidak ada kalender yang terhubung.",
        # Zoom Connect/Disconnect
        zoom_already_connected="Zoom sudah terhubung!\nGunakan /disconnectzoom untuk memutuskan koneksi terlebih dahulu.",
        click_to_connect_zoom="Klik tombol di bawah untuk menghubungkan akun Zoom Anda.\n\nAnda akan dialihkan ke Zoom untuk mengotorisasi akses.",
        connect_zoom_button="📹 Hubungkan Zoom",
        zoom_disconnected="✅ Zoom berhasil diputus.\nGunakan /connectzoom untuk menghubungkan kembali.",
        no_zoom_connected="Tidak ada akun Zoom yang terhubung.",
        # Timezone
        select_timezone="Pilih zona waktu Anda atau ketik secara manual (mis., `Asia/Jakarta`):",
        timezone_set="✅ Zona waktu diatur ke: `{timezone}`",
        timezone_set_ready='✅ Zona waktu diatur ke: `{timezone}`\n\nAnda siap! Buat rapat menggunakan:\n`@handycalbot 14:30 "Judul Rapat"`',
        invalid_timezone="❌ Zona waktu tidak valid: `{timezone}`\nSilakan gunakan zona waktu yang valid seperti `Asia/Jakarta` atau `America/New_York`.",
        select_duration="Pilih durasi rapat default:",
        duration_set="✅ Durasi default diatur ke: {duration} menit",
        select_reminder="Pilih pengingat default untuk rapat baru:\n\n_Anda dapat menimpanya per-rapat menggunakan `r 10m` dalam kueri inline Anda._",
        reminder_set="Pengingat default diatur ke: {reminder}",
        reminder_override_hint="_Gunakan `r` dalam kueri inline Anda untuk menerapkan default ini, atau `r 10m` untuk menimpa dengan waktu tertentu._",
        notifications_title="**Notifikasi Rapat** 🔔",
        notifications_status="Status: {status}",
        notifications_explanation="Saat diaktifkan, Anda akan menerima notifikasi Telegram sebelum rapat Anda (berdasarkan waktu pengingat yang Anda atur).",
        select_option="Pilih opsi:",
        enable_button="Aktifkan",
        disable_button="Nonaktifkan",
        current_suffix="(saat ini)",
        notifications_updated="{emoji} Notifikasi rapat {status}.",
        will_receive_reminders="Anda sekarang akan menerima pengingat sebelum rapat Anda.",
        will_not_receive_reminders="Anda tidak akan lagi menerima pengingat rapat.",
        select_language="🌍 Pilih bahasa pilihan Anda:",
        language_updated="✅ Bahasa berhasil diperbarui!",
        privacy_title="**Pengaturan Privasi** 🔒",
        privacy_username_invites="Izinkan undangan @username",
        privacy_enabled_desc="Orang lain dapat mengundang Anda ke rapat menggunakan @username Anda",
        privacy_disabled_desc="Hanya undangan email langsung yang akan berfungsi",
        privacy_updated="{emoji} Undangan username {status}.",
    ),
    meetings=MeetingsTranslations(
        upcoming_meetings="**Rapat Mendatang** 📅",
        no_upcoming_meetings="Tidak ada rapat mendatang ditemukan.",
        use_cancel_hint="_Gunakan /cancel untuk membatalkan rapat_",
        attendees_count="👥 {count} peserta",
        select_meeting_to_cancel="**Pilih rapat untuk dibatalkan:**",
        page_info="Halaman {current}/{total}",
        total_meetings="{count} total rapat",
        previous_button="⬅️ Sebelumnya",
        next_button="Selanjutnya ➡️",
        dont_cancel_button="❌ Jangan batalkan apa pun",
        no_meeting_cancelled="Tidak ada rapat yang dibatalkan.",
        cancelling_meeting="Membatalkan rapat...",
        meeting_cancelled="✅ Rapat dibatalkan: **{title}**",
        attendees_notified="_Peserta akan diberitahu secara otomatis._",
        cancel_not_your_menu="❌ Error: Ini bukan menu pembatalan Anda.",
        session_expired="❌ Error: Sesi kedaluwarsa. Silakan gunakan /cancel lagi.",
        meeting_not_found="❌ Error: Rapat tidak ditemukan. Silakan gunakan /cancel lagi.",
    ),
    inline=InlineTranslations(
        how_to_create="Cara membuat rapat",
        inline_help_description='Ketik: 14:30 "Judul Rapat" email@contoh.com',
        inline_help_message='Untuk membuat rapat, ketik:\n@handycalbot 14:30 "Judul Rapat" email@contoh.com\n\nFormat: WAKTU [TANGGAL] "JUDUL" [EMAIL]',
        please_start_first_title="Silakan mulai bot terlebih dahulu",
        please_start_first_description="Klik untuk membuka bot dan jalankan /start",
        please_start_first_message="Silakan mulai @handycalbot terlebih dahulu dengan mengirim /start",
        could_not_parse="Tidak dapat mengurai rapat",
        parse_error_description='Gunakan format: 14:30 "Judul Rapat" email...',
        parse_error_message='Tidak dapat mengurai rapat. Gunakan format:\n14:30 "Judul Rapat" email@contoh.com\n\nWaktu dan judul dalam tanda kutip diperlukan.\nTambahkan r 10m untuk pengingat, atau hanya r untuk default.',
        calendar_not_connected_warning="⚠️ Kalender tidak terhubung - /connect terlebih dahulu",
        attendees_label="👥 {count} peserta",
        today="hari ini",
        create_meeting_button="Buat Rapat",
        cancel_button="Batal",
        creating_meeting="Membuat rapat...",
        meeting_data_expired="❌ Error: Data rapat kedaluwarsa. Silakan coba lagi.",
        not_your_meeting="❌ Ini bukan rapat Anda!",
        meeting_created="Rapat dibuat!",
        reminder_label="🔔 Pengingat: {reminder} sebelumnya",
        invitations_sent="📧 Undangan terkirim ke:",
        attendees_will_receive="_Peserta ini akan menerima undangan kalender secara otomatis._",
        add_to_calendar_button="📅 Tambahkan ke Kalender Saya",
        not_listed_add_calendar="_Tidak terdaftar di atas? Klik di bawah untuk menambahkan ke kalender Anda:_",
        click_to_add_calendar="_Klik di bawah untuk menambahkan ke kalender Anda:_",
        meeting_cancelled="Rapat dibatalkan.",
        username_registered="terdaftar",
        username_privacy_disabled="privasi dinonaktifkan",
        username_not_found="tidak ditemukan",
        pending_invites_note="⏳ Belum terdaftar:",
        rate_limit_warning="⚠️ Terlalu banyak pencarian pengguna. Coba lagi nanti.",
        no_calendar_users_note="⚠️ Terdaftar tapi kalender belum terhubung:",
        privacy_disabled_users_note="🔒 Privasi dinonaktifkan (undangan tidak terkirim):",
        register_link_text="Daftar",
        # Edit menu
        edit_button="Edit",
        edit_menu_title="✏️ *Edit Rapat*\n\nApa yang ingin Anda ubah?",
        edit_title_button="📝 Judul",
        edit_time_button="🕐 Waktu",
        edit_date_button="📅 Tanggal",
        edit_duration_button="⏱️ Durasi",
        edit_reminder_button="🔔 Pengingat",
        edit_attendees_button="👥 Peserta",
        edit_link_button="🔗 Tambah Link",
        back_button="↩️ Kembali",
        done_editing_button="✅ Selesai",
        # Edit prompts
        enter_new_title='📝 *Masukkan judul baru*\n\nSaat ini: "{current}"\n\nKetik judul baru dan kirim.',
        enter_new_time="🕐 *Masukkan waktu baru*\n\nSaat ini: {current}\n\nKetik waktu baru (HH:MM) dan kirim.",
        enter_new_date="📅 *Masukkan tanggal baru*\n\nSaat ini: {current}\n\nKetik tanggal baru (DD-MM-YYYY) dan kirim.",
        select_duration="⏱️ *Pilih Durasi*",
        select_reminder="🔔 *Pilih Pengingat*",
        # Attendees
        current_attendees="*Peserta saat ini:*",
        add_attendee_prompt="👥 *Tambah Peserta*\n\nKetik alamat email atau @username dan kirim.",
        recent_contacts_title="*Kontak terbaru:*",
        no_recent_contacts="Tidak ada kontak terbaru",
        type_manually_button="✍️ Ketik email/@username",
        remove_attendee_button="🗑️",
        attendee_added="✅ Peserta ditambahkan: {attendee}",
        attendee_removed="✅ Peserta dihapus: {attendee}",
        invalid_email_format="❌ Format tidak valid. Gunakan email@contoh.com atau @username",
        no_attendees="Belum ada peserta",
        # Link
        add_link_title="🔗 *Link Rapat*",
        invalid_link_format="❌ Link tidak valid. Masukkan URL yang dimulai dengan http:// atau https://",
        invalid_time_format="❌ Format waktu tidak valid. Coba 14:00, 2pm, atau 14.30",
        invalid_date_format="❌ Format tanggal tidak valid. Coba besok, Jan 20, atau 20-01",
        auto_google_meet="🎥 Auto Google Meet",
        auto_zoom_meeting="📹 Rapat Zoom Otomatis",
        paste_custom_link="📋 Tempel Link Kustom",
        enter_link_prompt="🔗 *Masukkan link rapat*\n\nTempel URL rapat Anda.",
        link_added="✅ Link ditambahkan",
        link_removed="✅ Link dihapus",
        remove_link_button="🗑️ Hapus Link",
        google_meet_label="🎥 Google Meet",
        zoom_meeting_label="📹 Rapat Zoom",
        zoom_not_connected="Zoom tidak terhubung. Gunakan /connectzoom terlebih dahulu.",
        custom_link_label="🔗 Link Rapat",
        # Updates
        field_updated="✅ {field} diperbarui",
        meeting_updated="Rapat diperbarui",
        # Duration options
        duration_15_min="15 menit",
        duration_30_min="30 menit",
        duration_45_min="45 menit",
        duration_1_hour="1 jam",
        duration_1_5_hours="1,5 jam",
        duration_2_hours="2 jam",
        # Reminder options
        reminder_none="Tidak ada",
        reminder_5_min="5 menit",
        reminder_10_min="10 menit",
        reminder_15_min="15 menit",
        reminder_30_min="30 menit",
        reminder_1_hour="1 jam",
        reminder_1_day="1 hari",
        # Cancel edit
        cancel_edit_button="❌ Batal",
        edit_cancelled="Edit dibatalkan",
        # Private chat prompts (for text input redirect)
        continue_in_private="Untuk mengedit ini, lanjutkan di chat pribadi:",
        open_private_chat="💬 Buka Chat Pribadi",
        session_expired_restart="Sesi kedaluwarsa. Silakan mulai mengedit lagi dari pesan asli.",
        edit_complete_return="✅ Selesai! Pesan telah diperbarui.",
        back_to_chat_button="↩️ Kembali ke Chat",
        # Time selection grid
        select_time_title="🕐 *Pilih Waktu*",
        time_morning="Pagi",
        time_afternoon="Siang",
        custom_time_button="⌨️ Kustom",
        # Date selection grid
        select_date_title="📅 *Pilih Tanggal*",
        date_today="Hari ini",
        date_tomorrow="Besok",
        date_day_after="Lusa",
        date_in_3_days="Dalam 3 hari",
        date_in_a_week="Dalam seminggu",
        custom_date_button="⌨️ Kustom",
    ),
    donation=DonationTranslations(
        support_title="**Dukung HandyCalBot** ⭐",
        support_description="Jika Anda merasa bot ini berguna, pertimbangkan untuk mendukung pengembangannya dengan Telegram Stars!",
        support_helps="Dukungan Anda membantu menjaga bot tetap berjalan dan memungkinkan fitur baru.",
        select_amount="Pilih jumlah:",
        custom_amount_button="💫 Jumlah Kustom",
        custom_amount_prompt="**Donasi Kustom** 💫\n\nSilakan masukkan jumlah Stars yang ingin Anda donasikan (1-10000):",
        invalid_amount="Silakan masukkan jumlah yang valid antara 1 dan 10000 Stars.",
        invalid_number="Silakan masukkan angka yang valid (1-10000).",
        donation_error="Maaf, terjadi kesalahan saat memproses donasi Anda. Silakan coba lagi nanti.",
        thank_you="**Terima kasih atas donasi Anda!** 🙏",
        you_donated="Anda mendonasikan {amount} Telegram Stars. Dukungan Anda sangat berarti!",
        thank_you_running="Terima kasih telah membantu menjaga HandyCalBot tetap berjalan! ⭐",
    ),
    reminder=ReminderTranslations(
        meeting_reminder="🔔 *Pengingat Rapat*",
        starting_in="Dimulai dalam {time}",
    ),
    feedback=FeedbackTranslations(
        feedback_title="📝 **Masukan**",
        feedback_prompt="Silakan jelaskan masukan, laporan bug, atau saran Anda.",
        feedback_abort_hint="Ketik /abort untuk membatalkan.",
        feedback_received="✅ Terima kasih atas masukan Anda!",
        feedback_thank_you="Pesan Anda telah diterima dan akan ditinjau.",
    ),
    commands=CommandTranslations(
        start="Mulai bot dan lihat sambutan",
        help="Tampilkan bantuan dan instruksi",
        meetings="Daftar rapat mendatang",
        cancel="Batalkan rapat",
        connect="Hubungkan Google Calendar",
        disconnect="Putuskan Google Calendar",
        settings="Lihat pengaturan Anda",
        timezone="Ubah zona waktu",
        duration="Atur durasi default",
        reminder="Atur pengingat default",
        notifications="Aktifkan/nonaktifkan notifikasi",
        privacy="Pengaturan privasi untuk undangan",
        language="Ubah bahasa",
        donate="Dukung bot dengan Stars",
        feedback="Kirim masukan atau laporkan bug",
    ),
)
