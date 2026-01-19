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
*HandyCalBot*へようこそ! 📅

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
/connectzoom - ミーティングリンク用にZoomを接続
/meetings - 今後のミーティング一覧
/cancel - ミーティングをキャンセル
/settings - 設定を表示
/timezone - タイムゾーンを変更
/duration - デフォルト時間を設定
/reminder - デフォルトリマインダーを設定
/notifications - リマインダーのオン/オフ
/language - 言語を変更
/feedback - フィードバックまたはバグ報告
/donate - ボットをサポート

_バグ報告やUI改善のご提案をお待ちしております！_
""",
        help_message="""
*HandyCalBot ヘルプ* 📅

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
/connectzoom - ミーティングリンク用にZoomを接続
/meetings - 今後のミーティングを表示
/cancel - ミーティングをキャンセル
/settings - 設定を表示
/timezone - タイムゾーンを設定
/duration - デフォルトミーティング時間を設定
/reminder - デフォルトリマインダーを設定
/notifications - リマインダー通知のオン/オフ
/language - 言語を変更
/feedback - フィードバックまたはバグ報告
/donate - Starsでボットをサポート
""",
        timezone_detected="Telegramの言語設定に基づいてタイムゾーンを`{timezone}`に設定しました。変更するには /timezone を使用してください。",
        support_button="⭐ HandyCalBotをサポート",
        pending_invites_found="🎉 保留中の会議招待があります！",
        pending_invite_notification="📅 **{title}**\n🕐 {time}\n招待者: {inviter}",
    ),
    settings=SettingsTranslations(
        your_settings="**設定** ⚙️",
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
        connect_button="🔗 Googleカレンダーを接続",
        calendar_disconnected="✅ Googleカレンダーが切断されました。\n再接続するには /connect を使用してください。",
        no_calendar_connected="接続されたカレンダーはありません。",
        # Zoom Connect/Disconnect
        zoom_already_connected="Zoomは既に接続されています！\n先に /disconnectzoom で解除してください。",
        click_to_connect_zoom="下のボタンをクリックしてZoomアカウントを接続してください。\n\nZoomにリダイレクトされ、アクセスを許可します。",
        connect_zoom_button="📹 Zoomを接続",
        zoom_disconnected="✅ Zoomの接続が解除されました。\n再度接続するには /connectzoom を使用してください。",
        no_zoom_connected="Zoomアカウントが接続されていません。",
        # Privacy mode selection
        connect_mode_title="**Googleカレンダーを接続**\n\n接続モードを選択してください：",
        connect_full_access_button="📅 フルアクセス",
        connect_privacy_mode_button="🔒 プライバシーモード",
        connect_full_access_desc="_フルアクセス：予定の作成とカレンダーの閲覧が可能（/meetingsですべての予定を表示）_",
        connect_privacy_mode_desc="_プライバシーモード：予定の作成のみ、カレンダーの読み取り不可（/meetingsではボットが作成した予定のみ表示）_",
        select_timezone="タイムゾーンを選択するか、手動で入力してください (例: `Asia/Tokyo`):",
        timezone_set="✅ タイムゾーン設定: `{timezone}`",
        timezone_set_ready='タイムゾーン設定: `{timezone}`\n\n準備完了! ミーティング作成:\n`@handycalbot 14:30 "ミーティングタイトル"`',
        invalid_timezone="❌ 無効なタイムゾーン: `{timezone}`\n`Asia/Tokyo` や `Asia/Seoul` などの有効なタイムゾーンを使用してください。",
        select_duration="デフォルトミーティング時間を選択:",
        duration_set="✅ デフォルト時間設定: {duration}分",
        select_reminder="新しいミーティングのデフォルトリマインダーを選択:\n\n_インラインクエリで `r 10m` を使用してミーティングごとに上書きできます。_",
        reminder_set="デフォルトリマインダー設定: {reminder}",
        reminder_override_hint="_クエリで `r` を使用してデフォルトを適用するか、`r 10m` で特定の時間を指定してください。_",
        notifications_title="**ミーティング通知** 🔔",
        notifications_status="ステータス: {status}",
        notifications_explanation="有効にすると、設定したリマインダー時間に基づいてミーティング前にTelegram通知を受け取ります。",
        select_option="オプションを選択:",
        enable_button="有効にする",
        disable_button="無効にする",
        current_suffix="(現在)",
        notifications_updated="{emoji} ミーティング通知 {status}。",
        will_receive_reminders="ミーティング前にリマインダーを受け取るようになりました。",
        will_not_receive_reminders="ミーティングリマインダーを受け取らなくなりました。",
        select_language="🌍 お好みの言語を選択:",
        language_updated="✅ 言語が正常に更新されました!",
        privacy_title="**プライバシー設定** 🔒",
        privacy_username_invites="@ユーザー名での招待を許可",
        privacy_enabled_desc="他のユーザーが@ユーザー名で会議に招待できます",
        privacy_disabled_desc="直接のメール招待のみ機能します",
        privacy_updated="{emoji} ユーザー名招待が{status}になりました。",
    ),
    meetings=MeetingsTranslations(
        upcoming_meetings="**今後のミーティング** 📅",
        no_upcoming_meetings="今後のミーティングはありません。",
        use_cancel_hint="_ミーティングをキャンセルするには /cancel を使用_",
        attendees_count="👥 {count}名の参加者",
        privacy_mode_note="_🔒 プライバシーモード：ボットが作成した予定のみ表示_",
        # Meeting list and detail view
        close_button="✖️ 閉じる",
        edit_button="✏️ 編集",
        cancel_meeting_button="🗑️ キャンセル",
        back_to_list_button="↩️ リストに戻る",
        closed="予定リストを閉じました。",
        # Edit menu
        edit_menu_title="✏️ **予定を編集**\n\n編集する項目を選択してください：",
        edit_title_btn="📝 タイトル",
        edit_time_btn="🕐 時間",
        edit_date_btn="📅 日付",
        edit_duration_btn="⏱️ 所要時間",
        edit_attendees_btn="👥 参加者",
        edit_link_btn="🔗 リンク",
        field_updated="✅ {field} を更新しました",
        select_meeting_to_cancel="**キャンセルするミーティングを選択:**",
        page_info="ページ {current}/{total}",
        total_meetings="合計 {count} ミーティング",
        previous_button="⬅️ 前へ",
        next_button="次へ ➡️",
        dont_cancel_button="❌ キャンセルしない",
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
        attendees_label="👥 {count}名の参加者",
        today="今日",
        create_meeting_button="ミーティングを作成",
        cancel_button="キャンセル",
        creating_meeting="ミーティングを作成中...",
        meeting_data_expired="❌ エラー: ミーティングデータが期限切れです。もう一度お試しください。",
        not_your_meeting="❌ これはあなたのミーティングではありません!",
        meeting_created="ミーティングが作成されました!",
        reminder_label="🔔 リマインダー: {reminder}前",
        invitations_sent="📧 招待状を送信:",
        attendees_will_receive="_これらの参加者はカレンダー招待を自動的に受け取ります。_",
        add_to_calendar_button="📅 マイカレンダーに追加",
        not_listed_add_calendar="_リストにない場合は下をクリックしてカレンダーに追加:_",
        click_to_add_calendar="_下をクリックしてカレンダーに追加:_",
        meeting_cancelled="✅ ミーティングがキャンセルされました。",
        username_registered="登録済み",
        username_privacy_disabled="プライバシー無効",
        username_not_found="見つかりません",
        pending_invites_note="⏳ 未登録:",
        rate_limit_warning="⚠️ ユーザー検索が多すぎます。後でもう一度お試しください。",
        no_calendar_users_note="⚠️ 登録済みですがカレンダー未接続:",
        privacy_disabled_users_note="🔒 プライバシー無効（招待未送信）:",
        register_link_text="登録する",
        # Edit menu
        edit_button="編集",
        edit_menu_title="✏️ *ミーティングを編集*\n\n何を変更しますか？",
        edit_title_button="📝 タイトル",
        edit_time_button="🕐 時間",
        edit_date_button="📅 日付",
        edit_duration_button="⏱️ 長さ",
        edit_reminder_button="🔔 リマインダー",
        edit_attendees_button="👥 参加者",
        edit_link_button="🔗 リンク追加",
        back_button="↩️ 戻る",
        done_editing_button="✅ 完了",
        # Edit prompts
        enter_new_title='📝 *新しいタイトルを入力*\n\n現在: "{current}"\n\n新しいタイトルを入力して送信してください。',
        enter_new_time="🕐 *新しい時間を入力*\n\n現在: {current}\n\n新しい時間（HH:MM）を入力して送信してください。",
        enter_new_date="📅 *新しい日付を入力*\n\n現在: {current}\n\n新しい日付（DD-MM-YYYY）を入力して送信してください。",
        select_duration="⏱️ *長さを選択*",
        select_reminder="🔔 *リマインダーを選択*",
        # Attendees
        current_attendees="*現在の参加者:*",
        add_attendee_prompt="👥 *参加者を追加*\n\nメールアドレスまたは@ユーザー名を入力して送信してください。",
        recent_contacts_title="*最近の連絡先:*",
        no_recent_contacts="最近の連絡先なし",
        type_manually_button="✍️ メール/@ユーザー名を入力",
        remove_attendee_button="🗑️",
        attendee_added="✅ 参加者を追加: {attendee}",
        attendee_removed="✅ 参加者を削除: {attendee}",
        invalid_email_format="❌ 無効な形式です。email@example.com または @ユーザー名を使用してください",
        no_attendees="参加者はまだいません",
        # Link
        add_link_title="🔗 *ミーティングリンク*",
        invalid_link_format="❌ 無効なリンクです。http:// または https:// で始まるURLを入力してください",
        invalid_time_format="❌ 無効な時刻形式です。14:00、2pm、または14.30を試してください",
        invalid_date_format="❌ 無効な日付形式です。明日、Jan 20、または20-01を試してください",
        auto_google_meet="🎥 自動Google Meet",
        auto_zoom_meeting="📹 自動Zoomミーティング",
        paste_custom_link="📋 カスタムリンクを貼り付け",
        enter_link_prompt="🔗 *ミーティングリンクを入力*\n\nミーティングのURLを貼り付けてください。",
        link_added="✅ リンクを追加しました",
        link_removed="✅ リンクを削除しました",
        remove_link_button="🗑️ リンクを削除",
        google_meet_label="🎥 Google Meet",
        zoom_meeting_label="📹 Zoomミーティング",
        zoom_not_connected="Zoomが接続されていません。まず /connectzoom を使用してください。",
        custom_link_label="🔗 ミーティングリンク",
        # Updates
        field_updated="✅ {field}を更新しました",
        meeting_updated="ミーティングを更新しました",
        # Duration options
        duration_15_min="15分",
        duration_30_min="30分",
        duration_45_min="45分",
        duration_1_hour="1時間",
        duration_1_5_hours="1.5時間",
        duration_2_hours="2時間",
        # Reminder options
        reminder_none="なし",
        reminder_5_min="5分",
        reminder_10_min="10分",
        reminder_15_min="15分",
        reminder_30_min="30分",
        reminder_1_hour="1時間",
        reminder_1_day="1日",
        # Cancel edit
        cancel_edit_button="❌ キャンセル",
        edit_cancelled="編集をキャンセルしました",
        # Private chat prompts (for text input redirect)
        continue_in_private="これを編集するには、プライベートチャットで続けてください：",
        open_private_chat="💬 プライベートチャットを開く",
        session_expired_restart="セッションが期限切れです。元のメッセージから編集を再開してください。",
        edit_complete_return="✅ 完了！メッセージが更新されました。",
        back_to_chat_button="↩️ チャットに戻る",
        # Time selection grid
        select_time_title="🕐 *時間を選択*",
        time_morning="午前",
        time_afternoon="午後",
        custom_time_button="⌨️ カスタム",
        # Date selection grid
        select_date_title="📅 *日付を選択*",
        date_today="今日",
        date_tomorrow="明日",
        date_day_after="明後日",
        date_in_3_days="3日後",
        date_in_a_week="1週間後",
        custom_date_button="⌨️ カスタム",
    ),
    donation=DonationTranslations(
        support_title="**HandyCalBotをサポート** ⭐",
        support_description="このボットが役立つと思ったら、Telegram Starsで開発をサポートしてください!",
        support_helps="あなたのサポートはボットの運営と新機能の開発に役立ちます。",
        select_amount="金額を選択:",
        custom_amount_button="💫 カスタム金額",
        custom_amount_prompt="**カスタム寄付** 💫\n\n寄付するStarsの数を入力してください (1-10000):",
        invalid_amount="1から10000の間の有効な金額を入力してください。",
        invalid_number="有効な数字を入力してください (1-10000)。",
        donation_error="申し訳ありませんが、寄付の処理中にエラーが発生しました。後でもう一度お試しください。",
        thank_you="**ご寄付ありがとうございます!** 🙏",
        you_donated="{amount} Telegram Starsを寄付していただきました。あなたのサポートに感謝します!",
        thank_you_running="HandyCalBotの運営をサポートしていただきありがとうございます! ⭐",
    ),
    reminder=ReminderTranslations(
        meeting_reminder="🔔 *ミーティングリマインダー*",
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
        connectzoom="ミーティングリンク用にZoomを接続",
        disconnectzoom="Zoomアカウントを切断",
        settings="設定を表示",
        timezone="タイムゾーンを変更",
        duration="デフォルト時間を設定",
        reminder="デフォルトリマインダーを設定",
        notifications="通知のオン/オフ",
        privacy="招待のプライバシー設定",
        language="言語を変更",
        donate="Starsでボットをサポート",
        feedback="フィードバックまたはバグ報告",
    ),
)
