"""Japanese translations for CalendarBot."""

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
        please_start_first="まず /start を実行してください。",
        cancelled="キャンセルしました。",
        aborted="中止しました。",
        error_user_not_found="エラー: ユーザーが見つかりません。",
    ),
    start=StartTranslations(
        welcome_message="""
*HandyCalBot*へようこそ!

Telegramから直接ミーティングをスケジュールできます。

*クイックスタート:*
1. /connect でGoogleカレンダーを接続
2. 任意のチャットで @handycalbot と入力してミーティングを作成

*インライン使用方法:*
`@handycalbot 14:30 "ミーティングタイトル" email@example.com`
`@handycalbot 10:00 25-01-2026 "プロジェクト同期"`
`@handycalbot 14:30 "ミーティング" r 10m` (リマインダー付き)

*すべてのコマンド:*
/start - ウェルカムメッセージ
/help - ヘルプと使用方法
/connect - Googleカレンダーを接続
/disconnect - カレンダーを切断
/meetings - 今後のミーティング一覧
/cancel - ミーティングをキャンセル
/settings - 設定を表示
/timezone - タイムゾーンを変更
/duration - デフォルト時間を設定
/reminder - デフォルトリマインダーを設定
/notifications - リマインダーのオン/オフ
/language - 言語を変更
/donate - ボットをサポート
""",
        help_message="""
*HandyCalBot ヘルプ*

*ミーティング作成 (インライン):*
任意のチャットで `@handycalbot` と入力後:
- 時間 (必須): `HH:MM` (24時間形式)
- 日付 (任意): `DD-MM-YYYY`
- タイトル (必須): `"ミーティングタイトル"`
- 参加者 (任意): `email@example.com`
- リマインダー (任意): `r 10m` または `r 10m/30m` または `r`

*リマインダー形式:*
- `r 10m` - 10分前にリマインド
- `r 1h` - 1時間前にリマインド
- `r 1d` - 1日前にリマインド
- `r 10m/30m` - 複数のリマインダー
- `r` - デフォルトリマインダーを使用
- (rなし) - リマインダーなし

*例:*
`@handycalbot 14:30 "チームスタンドアップ"`
`@handycalbot 10:00 25-01-2026 "レビュー" tanaka@co.com`
`@handycalbot 16:00 "クイックコール" r 15m`
`@handycalbot 14:00 "ミーティング" sato@co.com r 10m/1h`

*すべてのコマンド:*
/start - ウェルカムメッセージ
/help - このヘルプメッセージ
/connect - Googleカレンダーを接続
/disconnect - カレンダーを切断
/meetings - 今後のミーティングを表示
/cancel - ミーティングをキャンセル
/settings - 設定を表示
/timezone - タイムゾーンを設定
/duration - デフォルトミーティング時間を設定
/reminder - デフォルトリマインダーを設定
/notifications - リマインダー通知のオン/オフ
/language - 言語を変更
/donate - Starsでボットをサポート
""",
        timezone_detected="Telegramの言語設定に基づいてタイムゾーンを`{timezone}`に設定しました。変更するには /timezone を使用してください。",
        support_button="⭐ HandyCalBotをサポート",
    ),
    settings=SettingsTranslations(
        your_settings="**設定**",
        timezone_label="タイムゾーン",
        duration_label="デフォルト時間",
        reminder_label="デフォルトリマインダー",
        notifications_label="通知",
        google_calendar_label="Googleカレンダー",
        change_settings="**設定変更:**",
        connected="✅ 接続済み",
        not_connected="未接続",
        enabled="有効",
        disabled="無効",
        no_reminder="リマインダーなし",
        before="前",
        day="日",
        days="日",
        hour="時間",
        hours="時間",
        minutes="分",
        calendar_already_connected="Googleカレンダーは既に接続されています!\n最初に /disconnect で切断してください。",
        click_to_connect="下のボタンをクリックしてGoogleカレンダーを接続してください。\n\nGoogleにリダイレクトされ、アクセスを承認します。",
        connect_button="Googleカレンダーを接続",
        calendar_disconnected="✅ Googleカレンダーが切断されました。\n再接続するには /connect を使用してください。",
        no_calendar_connected="接続されたカレンダーはありません。",
        select_timezone="タイムゾーンを選択するか、手動で入力してください (例: `Asia/Tokyo`):",
        timezone_set="✅ タイムゾーン設定: `{timezone}`",
        timezone_set_ready='タイムゾーン設定: `{timezone}`\n\n準備完了! ミーティング作成:\n`@handycalbot 14:30 "ミーティングタイトル"`',
        invalid_timezone="❌ 無効なタイムゾーン: `{timezone}`\n`Asia/Tokyo` や `Asia/Seoul` などの有効なタイムゾーンを使用してください。",
        select_duration="デフォルトミーティング時間を選択:",
        duration_set="✅ デフォルト時間設定: {duration}分",
        select_reminder="新しいミーティングのデフォルトリマインダーを選択:\n\n_インラインクエリで `r 10m` を使用してミーティングごとに上書きできます。_",
        reminder_set="デフォルトリマインダー設定: {reminder}",
        reminder_override_hint="_クエリで `r` を使用してデフォルトを適用するか、`r 10m` で特定の時間を指定してください。_",
        notifications_title="**ミーティング通知**",
        notifications_status="ステータス: {status}",
        notifications_explanation="有効にすると、設定したリマインダー時間に基づいてミーティング前にTelegram通知を受け取ります。",
        select_option="オプションを選択:",
        enable_button="有効にする",
        disable_button="無効にする",
        current_suffix="(現在)",
        notifications_updated="{emoji} ミーティング通知 {status}。",
        will_receive_reminders="ミーティング前にリマインダーを受け取るようになりました。",
        will_not_receive_reminders="ミーティングリマインダーを受け取らなくなりました。",
        select_language="お好みの言語を選択:",
        language_updated="✅ 言語が正常に更新されました!",
    ),
    meetings=MeetingsTranslations(
        upcoming_meetings="**今後のミーティング**",
        no_upcoming_meetings="今後のミーティングはありません。",
        use_cancel_hint="_ミーティングをキャンセルするには /cancel を使用_",
        attendees_count="{count}名の参加者",
        select_meeting_to_cancel="**キャンセルするミーティングを選択:**",
        page_info="ページ {current}/{total}",
        total_meetings="合計 {count} ミーティング",
        previous_button="前へ",
        next_button="次へ",
        dont_cancel_button="キャンセルしない",
        no_meeting_cancelled="✅ キャンセルされたミーティングはありません。",
        cancelling_meeting="ミーティングをキャンセル中...",
        meeting_cancelled="✅ ミーティングがキャンセルされました: **{title}**",
        attendees_notified="_参加者に自動的に通知されます。_",
        cancel_not_your_menu="❌ エラー: これはあなたのキャンセルメニューではありません。",
        session_expired="❌ エラー: セッションが期限切れです。/cancel を再度使用してください。",
        meeting_not_found="❌ エラー: ミーティングが見つかりません。/cancel を再度使用してください。",
    ),
    inline=InlineTranslations(
        how_to_create="ミーティングの作成方法",
        inline_help_description='入力: 14:30 "ミーティングタイトル" email@example.com',
        inline_help_message='ミーティングを作成するには:\n@handycalbot 14:30 "ミーティングタイトル" email@example.com\n\n形式: 時間 [日付] "タイトル" [メール]',
        please_start_first_title="まずボットを開始してください",
        please_start_first_description="クリックしてボットを開き /start を実行",
        please_start_first_message="まず /start を送信して @handycalbot を開始してください",
        could_not_parse="ミーティングを解析できません",
        parse_error_description='形式を使用: 14:30 "ミーティングタイトル" emails...',
        parse_error_message='ミーティングを解析できませんでした。形式を使用:\n14:30 "ミーティングタイトル" email@example.com\n\n時間と引用符内のタイトルは必須です。\nリマインダーには r 10m、デフォルトには r のみを追加。',
        calendar_not_connected_warning="⚠️ カレンダー未接続 - 先に /connect",
        attendees_label="{count}名の参加者",
        today="今日",
        create_meeting_button="ミーティングを作成",
        cancel_button="キャンセル",
        creating_meeting="ミーティングを作成中...",
        meeting_data_expired="❌ エラー: ミーティングデータが期限切れです。もう一度お試しください。",
        not_your_meeting="❌ これはあなたのミーティングではありません!",
        meeting_created="ミーティングが作成されました!",
        reminder_label="リマインダー: {reminder}前",
        invitations_sent="招待状を送信:",
        attendees_will_receive="_これらの参加者はカレンダー招待を自動的に受け取ります。_",
        add_to_calendar_button="マイカレンダーに追加",
        not_listed_add_calendar="_リストにない場合は下をクリックしてカレンダーに追加:_",
        click_to_add_calendar="_下をクリックしてカレンダーに追加:_",
        meeting_cancelled="✅ ミーティングがキャンセルされました。",
    ),
    donation=DonationTranslations(
        support_title="**HandyCalBotをサポート**",
        support_description="このボットが役立つと思ったら、Telegram Starsで開発をサポートしてください!",
        support_helps="あなたのサポートはボットの運営と新機能の開発に役立ちます。",
        select_amount="金額を選択:",
        custom_amount_button="カスタム金額",
        custom_amount_prompt="**カスタム寄付**\n\n寄付するStarsの数を入力してください (1-10000):",
        invalid_amount="1から10000の間の有効な金額を入力してください。",
        invalid_number="有効な数字を入力してください (1-10000)。",
        donation_error="申し訳ありませんが、寄付の処理中にエラーが発生しました。後でもう一度お試しください。",
        thank_you="**ご寄付ありがとうございます!**",
        you_donated="{amount} Telegram Starsを寄付していただきました。あなたのサポートに感謝します!",
        thank_you_running="HandyCalBotの運営をサポートしていただきありがとうございます!",
    ),
    reminder=ReminderTranslations(
        meeting_reminder="*ミーティングリマインダー*",
        starting_in="{time}後に開始",
    ),
    feedback=FeedbackTranslations(
        feedback_title="📝 **フィードバック**",
        feedback_prompt="フィードバック、バグ報告、または提案を入力してください。",
        feedback_abort_hint="キャンセルするには /abort と入力してください。",
        feedback_received="✅ フィードバックありがとうございます!",
        feedback_thank_you="メッセージを受け取りました。確認させていただきます。",
    ),
    commands=CommandTranslations(
        start="ボットを起動してウェルカム表示",
        help="ヘルプと使い方を表示",
        meetings="今後のミーティング一覧",
        cancel="ミーティングをキャンセル",
        connect="Googleカレンダーを接続",
        disconnect="Googleカレンダーを切断",
        settings="設定を表示",
        timezone="タイムゾーンを変更",
        duration="デフォルト時間を設定",
        reminder="デフォルトリマインダーを設定",
        notifications="通知のオン/オフ",
        language="言語を変更",
        donate="Starsでボットをサポート",
        feedback="フィードバックまたはバグ報告",
    ),
)
