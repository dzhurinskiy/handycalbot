"""Chinese translations for CalendarBot."""

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
        please_start_first="请先运行 /start。",
        cancelled="已取消。",
        aborted="已中止。",
        error_user_not_found="错误：未找到用户。",
    ),
    start=StartTranslations(
        welcome_message="""
欢迎使用 *HandyCalBot*!

我可以帮助您直接从 Telegram 安排会议。

*快速开始:*
1. 使用 /connect 连接您的 Google 日历
2. 在任意聊天中输入 @handycalbot 创建会议

*内联使用方法:*
`@handycalbot 14:30 "会议标题" email@example.com`
`@handycalbot 10:00 25-01-2026 "项目同步"`
`@handycalbot 14:30 "会议" r 10m` (带提醒)

*所有命令:*
/start - 欢迎消息
/help - 显示帮助和用法
/connect - 连接 Google 日历
/disconnect - 断开日历连接
/meetings - 列出即将到来的会议
/cancel - 取消会议
/settings - 查看设置
/timezone - 更改时区
/duration - 设置默认时长
/reminder - 设置默认提醒
/notifications - 开关提醒
/language - 更改语言
/feedback - 发送反馈或报告错误
/donate - 支持机器人

_欢迎提交错误报告和UI改进建议！_
""",
        help_message="""
*HandyCalBot 帮助*

*创建会议 (内联):*
在任意聊天中输入 `@handycalbot` 后跟:
- 时间 (必需): `HH:MM` (24小时格式)
- 日期 (可选): `DD-MM-YYYY`
- 标题 (必需): `"您的会议标题"`
- 参与者 (可选): `email@example.com`
- 提醒 (可选): `r 10m` 或 `r 10m/30m` 或仅 `r`

*提醒格式:*
- `r 10m` - 10分钟前提醒
- `r 1h` - 1小时前提醒
- `r 1d` - 1天前提醒
- `r 10m/30m` - 多个提醒
- `r` - 使用默认提醒
- (无r) - 无提醒

*示例:*
`@handycalbot 14:30 "团队站会"`
`@handycalbot 10:00 25-01-2026 "评审" wang@co.com`
`@handycalbot 16:00 "快速通话" r 15m`
`@handycalbot 14:00 "会议" li@co.com r 10m/1h`

*所有命令:*
/start - 欢迎消息
/help - 此帮助消息
/connect - 连接 Google 日历
/disconnect - 断开日历连接
/meetings - 显示即将到来的会议
/cancel - 取消会议
/settings - 查看设置
/timezone - 设置时区
/duration - 设置默认会议时长
/reminder - 设置默认提醒
/notifications - 开关提醒通知
/language - 更改语言
/feedback - 发送反馈或报告错误
/donate - 用 Stars 支持机器人
""",
        timezone_detected="根据您的 Telegram 语言设置，已将时区设置为 `{timezone}`。如需更改请使用 /timezone。",
        support_button="⭐ 支持 HandyCalBot",
    ),
    settings=SettingsTranslations(
        your_settings="**您的设置**",
        timezone_label="时区",
        duration_label="默认时长",
        reminder_label="默认提醒",
        notifications_label="通知",
        google_calendar_label="Google 日历",
        change_settings="**更改设置:**",
        connected="✅ 已连接",
        not_connected="未连接",
        enabled="已启用",
        disabled="已禁用",
        no_reminder="无提醒",
        before="前",
        day="天",
        days="天",
        hour="小时",
        hours="小时",
        minutes="分钟",
        calendar_already_connected="Google 日历已连接!\n请先使用 /disconnect 断开连接。",
        click_to_connect="点击下方按钮连接您的 Google 日历。\n\n您将被重定向到 Google 进行授权。",
        connect_button="连接 Google 日历",
        calendar_disconnected="✅ Google 日历已成功断开。\n使用 /connect 重新连接。",
        no_calendar_connected="未连接日历。",
        select_timezone="选择您的时区或手动输入 (例如 `Asia/Shanghai`):",
        timezone_set="✅ 时区已设置: `{timezone}`",
        timezone_set_ready='时区已设置: `{timezone}`\n\n准备就绪! 创建会议:\n`@handycalbot 14:30 "会议标题"`',
        invalid_timezone="❌ 无效的时区: `{timezone}`\n请使用有效的时区如 `Asia/Shanghai` 或 `Asia/Hong_Kong`。",
        select_duration="选择默认会议时长:",
        duration_set="✅ 默认时长已设置: {duration}分钟",
        select_reminder="选择新会议的默认提醒:\n\n_您可以在内联查询中使用 `r 10m` 覆盖每个会议的设置。_",
        reminder_set="默认提醒已设置: {reminder}",
        reminder_override_hint="_在查询中使用 `r` 应用默认值，或使用 `r 10m` 指定特定时间。_",
        notifications_title="**会议通知**",
        notifications_status="状态: {status}",
        notifications_explanation="启用后，您将根据设置的提醒时间在会议前收到 Telegram 通知。",
        select_option="选择选项:",
        enable_button="启用",
        disable_button="禁用",
        current_suffix="(当前)",
        notifications_updated="{emoji} 会议通知 {status}。",
        will_receive_reminders="您现在将在会议前收到提醒。",
        will_not_receive_reminders="您将不再收到会议提醒。",
        select_language="选择您的首选语言:",
        language_updated="✅ 语言更新成功!",
    ),
    meetings=MeetingsTranslations(
        upcoming_meetings="**即将到来的会议**",
        no_upcoming_meetings="未找到即将到来的会议。",
        use_cancel_hint="_使用 /cancel 取消会议_",
        attendees_count="{count}位参与者",
        select_meeting_to_cancel="**选择要取消的会议:**",
        page_info="第 {current}/{total} 页",
        total_meetings="共 {count} 个会议",
        previous_button="上一页",
        next_button="下一页",
        dont_cancel_button="不取消",
        no_meeting_cancelled="✅ 未取消任何会议。",
        cancelling_meeting="正在取消会议...",
        meeting_cancelled="✅ 会议已取消: **{title}**",
        attendees_notified="_参与者将自动收到通知。_",
        cancel_not_your_menu="❌ 错误：这不是您的取消菜单。",
        session_expired="❌ 错误：会话已过期。请重新使用 /cancel。",
        meeting_not_found="❌ 错误：未找到会议。请重新使用 /cancel。",
    ),
    inline=InlineTranslations(
        how_to_create="如何创建会议",
        inline_help_description='输入: 14:30 "会议标题" email@example.com',
        inline_help_message='要创建会议，请输入:\n@handycalbot 14:30 "会议标题" email@example.com\n\n格式: 时间 [日期] "标题" [邮箱]',
        please_start_first_title="请先启动机器人",
        please_start_first_description="点击打开机器人并运行 /start",
        please_start_first_message="请先发送 /start 启动 @handycalbot",
        could_not_parse="无法解析会议",
        parse_error_description='使用格式: 14:30 "会议标题" emails...',
        parse_error_message='无法解析会议。使用格式:\n14:30 "会议标题" email@example.com\n\n时间和引号内的标题是必需的。\n添加 r 10m 设置提醒，或仅 r 使用默认值。',
        calendar_not_connected_warning="⚠️ 日历未连接 - 请先 /connect",
        attendees_label="{count}位参与者",
        today="今天",
        create_meeting_button="创建会议",
        cancel_button="取消",
        creating_meeting="正在创建会议...",
        meeting_data_expired="❌ 错误：会议数据已过期。请重试。",
        not_your_meeting="❌ 这不是您的会议!",
        meeting_created="会议已创建!",
        reminder_label="提醒: {reminder}前",
        invitations_sent="邀请已发送给:",
        attendees_will_receive="_这些参与者将自动收到日历邀请。_",
        add_to_calendar_button="添加到我的日历",
        not_listed_add_calendar="_不在列表中? 点击下方添加到您的日历:_",
        click_to_add_calendar="_点击下方添加到您的日历:_",
        meeting_cancelled="✅ 会议已取消。",
    ),
    donation=DonationTranslations(
        support_title="**支持 HandyCalBot**",
        support_description="如果您觉得这个机器人有用，请考虑使用 Telegram Stars 支持它的开发!",
        support_helps="您的支持有助于保持机器人运行并开发新功能。",
        select_amount="选择金额:",
        custom_amount_button="自定义金额",
        custom_amount_prompt="**自定义捐赠**\n\n请输入您想捐赠的 Stars 数量 (1-10000):",
        invalid_amount="请输入1到10000之间的有效金额。",
        invalid_number="请输入有效数字 (1-10000)。",
        donation_error="抱歉，处理您的捐赠时出错。请稍后重试。",
        thank_you="**感谢您的捐赠!**",
        you_donated="您捐赠了 {amount} Telegram Stars。感谢您的支持!",
        thank_you_running="感谢您帮助保持 HandyCalBot 运行!",
    ),
    reminder=ReminderTranslations(
        meeting_reminder="*会议提醒*",
        starting_in="{time}后开始",
    ),
    feedback=FeedbackTranslations(
        feedback_title="📝 **反馈**",
        feedback_prompt="请描述您的反馈、错误报告或建议。",
        feedback_abort_hint="输入 /abort 取消。",
        feedback_received="✅ 感谢您的反馈!",
        feedback_thank_you="您的消息已收到，我们会进行审核。",
    ),
    commands=CommandTranslations(
        start="启动机器人并查看欢迎消息",
        help="显示帮助和使用说明",
        meetings="列出即将到来的会议",
        cancel="取消会议",
        connect="连接 Google 日历",
        disconnect="断开 Google 日历",
        settings="查看设置",
        timezone="更改时区",
        duration="设置默认时长",
        reminder="设置默认提醒",
        notifications="开关通知",
        language="更改语言",
        donate="用 Stars 支持机器人",
        feedback="发送反馈或报告错误",
    ),
)
