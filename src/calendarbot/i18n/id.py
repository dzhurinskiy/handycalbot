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
        language="Ubah bahasa",
        donate="Dukung bot dengan Stars",
        feedback="Kirim masukan atau laporkan bug",
    ),
)
