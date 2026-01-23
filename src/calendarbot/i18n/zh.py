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
欢迎使用 *HandyCalBot*! 📅

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
/connectzoom - 连接 Zoom 获取会议链接
/disconnectzoom - 断开Zoom连接
/meetings - 查看和管理会议
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
*HandyCalBot 帮助* 📅

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
/connectzoom - 连接 Zoom 获取会议链接
/disconnectzoom - 断开Zoom连接
/meetings - 查看和管理会议
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
        pending_invites_found="🎉 您有待处理的会议邀请！",
        pending_invite_notification="📅 **{title}**\n🕐 {time}\n邀请者: {inviter}",
    ),
    settings=SettingsTranslations(
        your_settings="**您的设置** ⚙️",
        timezone_label="时区",
        duration_label="默认时长",
        reminder_label="默认提醒",
        notifications_label="通知",
        google_calendar_label="Google 日历",
        outlook_calendar_label="Outlook 日历",
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
        connect_button="🔗 连接 Google 日历",
        calendar_disconnected="✅ Google 日历已成功断开。\n使用 /connect 重新连接。",
        no_calendar_connected="未连接日历。",
        # Zoom Connect/Disconnect
        zoom_already_connected="Zoom 已连接！\n请先使用 /disconnectzoom 断开连接。",
        click_to_connect_zoom="点击下方按钮连接您的 Zoom 账户。\n\n您将被重定向到 Zoom 授权访问。",
        connect_zoom_button="📹 连接 Zoom",
        zoom_disconnected="✅ Zoom 已成功断开连接。\n使用 /connectzoom 重新连接。",
        no_zoom_connected="未连接 Zoom 账户。",
        # Outlook Connect/Disconnect
        outlook_already_connected="Outlook 日历已连接！\n请先使用 /disconnectoutlook 断开连接。",
        click_to_connect_outlook="点击下方按钮连接您的 Microsoft Outlook 日历。\n\n您将被重定向到 Microsoft 进行授权。",
        connect_outlook_button="🔗 连接 Outlook 日历",
        outlook_disconnected="✅ Outlook 日历已成功断开。\n使用 /connectoutlook 重新连接。",
        no_outlook_connected="未连接 Outlook 日历。",
        connect_outlook_mode_title="**连接 Outlook 日历**\n\n选择连接模式：",
        outlook_connected_status="**Outlook日历已连接** ✅\n\n当前模式: {mode}\n\n您可以在下方切换模式或断开连接:",
        # Privacy mode selection
        connect_mode_title="**连接 Google 日历**\n\n选择连接模式：",
        connect_full_access_button="📅 完全访问",
        connect_privacy_mode_button="🔒 隐私模式",
        connect_full_access_desc="_完全访问：创建会议并查看日历（/meetings 显示所有事件）_",
        connect_privacy_mode_desc="_隐私模式：仅创建会议，不读取日历（/meetings 仅显示机器人创建的事件）_",
        # Calendar connected status (mode switching)
        calendar_connected_status="**Google日历已连接** ✅\n\n当前模式: {mode}\n\n您可以在下方切换模式或断开连接:",
        current_mode_full="📅 完全访问",
        current_mode_privacy="🔒 隐私模式",
        switch_to_full_button="📅 切换到完全访问",
        switch_to_privacy_button="🔒 切换到隐私模式",
        disconnect_button="❌ 断开连接",
        select_timezone="选择您的时区或手动输入 (例如 `Asia/Shanghai`):",
        timezone_set="✅ 时区已设置: `{timezone}`",
        timezone_set_ready='时区已设置: `{timezone}`\n\n准备就绪! 创建会议:\n`@handycalbot 14:30 "会议标题"`',
        invalid_timezone="❌ 无效的时区: `{timezone}`\n请使用有效的时区如 `Asia/Shanghai` 或 `Asia/Hong_Kong`。",
        select_duration="选择默认会议时长:",
        duration_set="✅ 默认时长已设置: {duration}分钟",
        select_reminder="选择新会议的默认提醒:\n\n_您可以在内联查询中使用 `r 10m` 覆盖每个会议的设置。_",
        reminder_set="默认提醒已设置: {reminder}",
        reminder_override_hint="_在查询中使用 `r` 应用默认值，或使用 `r 10m` 指定特定时间。_",
        notifications_title="**会议通知** 🔔",
        notifications_status="状态: {status}",
        notifications_explanation="启用后，您将根据设置的提醒时间在会议前收到 Telegram 通知。",
        select_option="选择选项:",
        enable_button="启用",
        disable_button="禁用",
        current_suffix="(当前)",
        notifications_updated="{emoji} 会议通知 {status}。",
        will_receive_reminders="您现在将在会议前收到提醒。",
        will_not_receive_reminders="您将不再收到会议提醒。",
        select_language="🌍 选择您的首选语言:",
        language_updated="✅ 语言更新成功!",
        privacy_title="**隐私设置** 🔒",
        privacy_username_invites="允许@用户名邀请",
        privacy_enabled_desc="其他人可以通过您的@用户名邀请您参加会议",
        privacy_disabled_desc="只有直接电子邮件邀请才会生效",
        privacy_updated="{emoji} 用户名邀请{status}。",
    ),
    meetings=MeetingsTranslations(
        upcoming_meetings="**即将到来的会议** 📅",
        no_upcoming_meetings="未找到即将到来的会议。",
        use_cancel_hint="_使用 /cancel 取消会议_",
        attendees_count="👥 {count}位参与者",
        privacy_mode_note="_🔒 隐私模式：仅显示机器人创建的会议_",
        # Meeting list and detail view
        close_button="✖️ 关闭",
        edit_button="✏️ 编辑",
        cancel_meeting_button="🗑️ 取消",
        back_to_list_button="↩️ 返回列表",
        closed="会议列表已关闭。",
        # Edit menu
        edit_menu_title="✏️ **编辑会议**\n\n选择要编辑的字段：",
        edit_title_btn="📝 标题",
        edit_time_btn="🕐 时间",
        edit_date_btn="📅 日期",
        edit_duration_btn="⏱️ 时长",
        edit_attendees_btn="👥 参与者",
        edit_link_btn="🔗 链接",
        field_updated="✅ {field} 已更新",
        select_meeting_to_cancel="**选择要取消的会议:**",
        page_info="第 {current}/{total} 页",
        total_meetings="共 {count} 个会议",
        previous_button="⬅️ 上一页",
        next_button="下一页 ➡️",
        dont_cancel_button="❌ 不取消",
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
        attendees_label="👥 {count}位参与者",
        today="今天",
        create_meeting_button="创建会议",
        cancel_button="取消",
        creating_meeting="正在创建会议...",
        meeting_data_expired="❌ 错误：会议数据已过期。请重试。",
        not_your_meeting="❌ 这不是您的会议!",
        meeting_created="会议已创建!",
        reminder_label="🔔 提醒: {reminder}前",
        invitations_sent="📧 邀请已发送给:",
        attendees_will_receive="_这些参与者将自动收到日历邀请。_",
        add_to_calendar_button="📅 添加到我的日历",
        not_listed_add_calendar="_不在列表中? 点击下方添加到您的日历:_",
        click_to_add_calendar="_点击下方添加到您的日历:_",
        meeting_cancelled="✅ 会议已取消。",
        username_registered="已注册",
        username_privacy_disabled="隐私已禁用",
        username_not_found="未找到",
        pending_invites_note="⏳ 尚未注册:",
        rate_limit_warning="⚠️ 用户搜索次数过多。请稍后再试。",
        no_calendar_users_note="⚠️ 已注册但未连接日历:",
        privacy_disabled_users_note="🔒 隐私已禁用（未发送邀请）:",
        register_link_text="注册",
        # Edit menu
        edit_button="编辑",
        edit_menu_title="✏️ *编辑会议*\n\n您想修改什么？",
        edit_title_button="📝 标题",
        edit_time_button="🕐 时间",
        edit_date_button="📅 日期",
        edit_duration_button="⏱️ 时长",
        edit_reminder_button="🔔 提醒",
        edit_attendees_button="👥 参与者",
        edit_link_button="🔗 添加链接",
        back_button="↩️ 返回",
        done_editing_button="✅ 完成",
        # Edit prompts
        enter_new_title='📝 *输入新标题*\n\n当前: "{current}"\n\n输入新标题并发送。',
        enter_new_time="🕐 *输入新时间*\n\n当前: {current}\n\n输入新时间（HH:MM）并发送。",
        enter_new_date="📅 *输入新日期*\n\n当前: {current}\n\n输入新日期（DD-MM-YYYY）并发送。",
        select_duration="⏱️ *选择时长*",
        select_reminder="🔔 *选择提醒*",
        # Attendees
        current_attendees="*当前参与者:*",
        add_attendee_prompt="👥 *添加参与者*\n\n输入邮箱地址或@用户名并发送。",
        recent_contacts_title="*最近联系人:*",
        no_recent_contacts="没有最近联系人",
        type_manually_button="✍️ 输入邮箱/@用户名",
        remove_attendee_button="🗑️",
        attendee_added="✅ 已添加参与者: {attendee}",
        attendee_removed="✅ 已移除参与者: {attendee}",
        invalid_email_format="❌ 格式无效。请使用 email@example.com 或 @用户名",
        no_attendees="暂无参与者",
        # Link
        add_link_title="🔗 *会议链接*",
        invalid_link_format="❌ 链接无效。请输入以 http:// 或 https:// 开头的URL",
        invalid_time_format="❌ 时间格式无效。请尝试 14:00、2pm 或 14.30",
        invalid_date_format="❌ 日期格式无效。请尝试 明天、Jan 20 或 20-01",
        auto_google_meet="🎥 自动Google Meet",
        auto_teams_meeting="📹 自动Microsoft Teams",
        auto_zoom_meeting="📹 自动 Zoom 会议",
        paste_custom_link="📋 粘贴自定义链接",
        enter_link_prompt="🔗 *输入会议链接*\n\n粘贴您的会议URL。",
        link_added="✅ 链接已添加",
        link_removed="✅ 链接已移除",
        remove_link_button="🗑️ 移除链接",
        google_meet_label="🎥 Google Meet",
        teams_meeting_label="📹 Microsoft Teams",
        zoom_meeting_label="📹 Zoom 会议",
        zoom_not_connected="Zoom 未连接。请先使用 /connectzoom。",
        outlook_not_connected="Outlook 未连接。请先使用 /connectoutlook。",
        custom_link_label="🔗 会议链接",
        # Updates
        field_updated="✅ {field}已更新",
        meeting_updated="会议已更新",
        # Duration options
        duration_15_min="15分钟",
        duration_30_min="30分钟",
        duration_45_min="45分钟",
        duration_1_hour="1小时",
        duration_1_5_hours="1.5小时",
        duration_2_hours="2小时",
        # Reminder options
        reminder_none="无",
        reminder_5_min="5分钟",
        reminder_10_min="10分钟",
        reminder_15_min="15分钟",
        reminder_30_min="30分钟",
        reminder_1_hour="1小时",
        reminder_1_day="1天",
        # Cancel edit
        cancel_edit_button="❌ 取消",
        edit_cancelled="编辑已取消",
        # Private chat prompts (for text input redirect)
        continue_in_private="要编辑此内容，请在私聊中继续：",
        open_private_chat="💬 打开私聊",
        session_expired_restart="会话已过期。请从原始消息重新开始编辑。",
        edit_complete_return="✅ 完成！消息已更新。",
        back_to_chat_button="↩️ 返回聊天",
        # Time selection grid
        select_time_title="🕐 *选择时间*",
        time_morning="上午",
        time_afternoon="下午",
        custom_time_button="⌨️ 自定义",
        # Date selection grid
        select_date_title="📅 *选择日期*",
        date_today="今天",
        date_tomorrow="明天",
        date_day_after="后天",
        date_in_3_days="3天后",
        date_in_a_week="一周后",
        custom_date_button="⌨️ 自定义",
    ),
    donation=DonationTranslations(
        support_title="**支持 HandyCalBot** ⭐",
        support_description="如果您觉得这个机器人有用，请考虑使用 Telegram Stars 支持它的开发!",
        support_helps="您的支持有助于保持机器人运行并开发新功能。",
        select_amount="选择金额:",
        custom_amount_button="💫 自定义金额",
        custom_amount_prompt="**自定义捐赠** 💫\n\n请输入您想捐赠的 Stars 数量 (1-10000):",
        invalid_amount="请输入1到10000之间的有效金额。",
        invalid_number="请输入有效数字 (1-10000)。",
        donation_error="抱歉，处理您的捐赠时出错。请稍后重试。",
        thank_you="**感谢您的捐赠!** 🙏",
        you_donated="您捐赠了 {amount} Telegram Stars。感谢您的支持!",
        thank_you_running="感谢您帮助保持 HandyCalBot 运行! ⭐",
    ),
    reminder=ReminderTranslations(
        meeting_reminder="🔔 *会议提醒*",
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
        connectzoom="连接 Zoom 获取会议链接",
        disconnectzoom="断开 Zoom 账户",
        connectoutlook="连接 Outlook 日历",
        disconnectoutlook="断开 Outlook 日历",
        settings="查看设置",
        timezone="更改时区",
        duration="设置默认时长",
        reminder="设置默认提醒",
        notifications="开关通知",
        privacy="邀请隐私设置",
        language="更改语言",
        donate="用 Stars 支持机器人",
        feedback="发送反馈或报告错误",
    ),
)
