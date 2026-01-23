"""Korean translations for CalendarBot."""

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
        please_start_first="먼저 /start를 실행해 주세요.",
        cancelled="취소되었습니다.",
        aborted="중단되었습니다.",
        error_user_not_found="오류: 사용자를 찾을 수 없습니다.",
    ),
    start=StartTranslations(
        welcome_message="""
*HandyCalBot*에 오신 것을 환영합니다! 📅

텔레그램에서 직접 회의를 예약할 수 있도록 도와드립니다.

*빠른 시작:*
1️⃣ /connect로 캘린더 연결
2️⃣ 아무 채팅에서 @handycalbot 입력하여 회의 생성

*인라인 사용법:*
`@handycalbot 14:30 "회의 제목" email@example.com`
`@handycalbot 10:00 25-01-2026 "프로젝트 동기화"`
`@handycalbot 14:30 "회의" r 10m` (알림 포함)
`@handycalbot 14:30 "회의" @alice @bob` (사용자명으로 초대)

*명령어:*
/connect - 캘린더 또는 Zoom 연결
/disconnect - 서비스 연결 해제
/meetings - 일정 보기 및 관리
/settings - 설정 보기
/timezone, /duration, /reminder - 기본값 설정
/notifications, /privacy, /language - 환경 설정
/feedback - 피드백 보내기 또는 버그 신고
/donate - 봇 후원하기 ⭐

_버그 신고 및 UI 개선 제안을 환영합니다!_
""",
        help_message="""
*HandyCalBot 도움말* 📅

*회의 만들기 (인라인):*
아무 채팅에서 `@handycalbot` 입력 후:
• 시간 (필수): `HH:MM` (24시간 형식)
• 날짜 (선택): `DD-MM-YYYY`
• 제목 (필수): `"회의 제목"`
• 참석자 (선택): `email@example.com` 또는 `@사용자명`
• 알림 (선택): `r 10m` 또는 `r 10m/30m` 또는 `r`

*알림 형식:*
• `r 10m` - 10분 전 알림
• `r 1h` - 1시간 전 알림
• `r 1d` - 1일 전 알림
• `r 10m/30m` - 여러 알림
• `r` - 기본 알림 사용
• (r 없음) - 알림 없음

*예시:*
`@handycalbot 14:30 "팀 스탠드업"`
`@handycalbot 10:00 25-01-2026 "리뷰" kim@co.com`
`@handycalbot 16:00 "빠른 통화" r 15m`
`@handycalbot 14:00 "회의" @alice @bob r 10m`

*명령어:*
/connect - Google 캘린더, Outlook 또는 Zoom 연결
/disconnect - 서비스 연결 해제
/meetings - 예정된 일정 보기 및 관리
/settings - 현재 설정 보기
/timezone - 시간대 설정
/duration - 기본 회의 시간 설정
/reminder - 기본 알림 설정
/notifications - 알림 켜기/끄기
/privacy - 사용자명 초대 설정
/language - 언어 변경
/feedback - 피드백 보내기 또는 버그 신고
/donate - Stars로 봇 후원 ⭐
""",
        timezone_detected="텔레그램 언어 설정을 기반으로 시간대를 `{timezone}`로 설정했습니다. 변경하려면 /timezone을 사용하세요.",
        support_button="⭐ HandyCalBot 후원하기",
        pending_invites_found="🎉 대기 중인 회의 초대가 있습니다!",
        pending_invite_notification="📅 **{title}**\n🕐 {time}\n초대자: {inviter}",
    ),
    settings=SettingsTranslations(
        your_settings="**설정** ⚙️",
        timezone_label="시간대",
        duration_label="기본 시간",
        reminder_label="기본 알림",
        notifications_label="알림",
        google_calendar_label="Google 캘린더",
        outlook_calendar_label="Outlook 캘린더",
        change_settings="**설정 변경:**",
        connected="✅ 연결됨",
        not_connected="연결 안됨",
        enabled="활성화",
        disabled="비활성화",
        no_reminder="알림 없음",
        before="전",
        day="일",
        days="일",
        hour="시간",
        hours="시간",
        minutes="분",
        calendar_already_connected="Google 캘린더가 이미 연결되어 있습니다!\n먼저 /disconnect로 연결을 해제하세요.",
        click_to_connect="아래 버튼을 클릭하여 Google 캘린더를 연결하세요.\n\nGoogle로 이동하여 액세스를 승인합니다.",
        connect_button="🔗 Google 캘린더 연결",
        calendar_disconnected="✅ Google 캘린더가 연결 해제되었습니다.\n다시 연결하려면 /connect를 사용하세요.",
        no_calendar_connected="연결된 캘린더가 없습니다.",
        # Zoom Connect/Disconnect
        zoom_already_connected="Zoom이 이미 연결되어 있습니다!\n먼저 /disconnectzoom으로 연결을 해제하세요.",
        click_to_connect_zoom="아래 버튼을 클릭하여 Zoom 계정을 연결하세요.\n\nZoom으로 이동하여 액세스를 승인합니다.",
        connect_zoom_button="📹 Zoom 연결",
        zoom_disconnected="✅ Zoom 연결이 해제되었습니다.\n다시 연결하려면 /connectzoom을 사용하세요.",
        no_zoom_connected="연결된 Zoom 계정이 없습니다.",
        # Outlook Connect/Disconnect
        outlook_already_connected="Outlook 캘린더가 이미 연결되어 있습니다!\n먼저 /disconnectoutlook으로 연결을 해제하세요.",
        click_to_connect_outlook="아래 버튼을 클릭하여 Microsoft Outlook 캘린더를 연결하세요.\n\nMicrosoft로 이동하여 액세스를 승인합니다.",
        connect_outlook_button="🔗 Outlook 캘린더 연결",
        outlook_disconnected="✅ Outlook 캘린더 연결이 해제되었습니다.\n다시 연결하려면 /connectoutlook을 사용하세요.",
        no_outlook_connected="연결된 Outlook 캘린더가 없습니다.",
        connect_outlook_mode_title="**Outlook 캘린더 연결**\n\n연결 모드를 선택하세요:",
        outlook_connected_status="**Outlook 캘린더 연결됨** ✅\n\n현재 모드: {mode}\n\n아래에서 모드를 변경하거나 연결을 해제할 수 있습니다:",
        # Privacy mode selection
        connect_mode_title="**Google Calendar 연결**\n\n연결 모드를 선택하세요:",
        connect_full_access_button="📅 전체 액세스",
        connect_privacy_mode_button="🔒 개인정보 보호 모드",
        connect_full_access_desc="_전체 액세스: 일정 생성 및 캘린더 보기 (/meetings에서 모든 일정 표시)_",
        connect_privacy_mode_desc="_개인정보 보호 모드: 일정 생성만 가능, 캘린더 읽기 불가 (/meetings에서 봇이 만든 일정만 표시)_",
        # Calendar connected status (mode switching)
        calendar_connected_status="**Google 캘린더 연결됨** ✅\n\n현재 모드: {mode}\n\n아래에서 모드를 변경하거나 연결을 해제할 수 있습니다:",
        current_mode_full="📅 전체 액세스",
        current_mode_privacy="🔒 개인정보 보호 모드",
        switch_to_full_button="📅 전체 액세스로 전환",
        switch_to_privacy_button="🔒 개인정보 보호 모드로 전환",
        disconnect_button="❌ 연결 해제",
        # Timezone
        select_timezone="시간대를 선택하거나 직접 입력하세요 (예: `Asia/Seoul`):",
        timezone_set="✅ 시간대 설정됨: `{timezone}`",
        timezone_set_ready='시간대 설정됨: `{timezone}`\n\n준비 완료! 회의 만들기:\n`@handycalbot 14:30 "회의 제목"`',
        invalid_timezone="❌ 잘못된 시간대: `{timezone}`\n`Asia/Seoul` 또는 `Asia/Tokyo`와 같은 유효한 시간대를 사용하세요.",
        select_duration="기본 회의 시간 선택:",
        duration_set="✅ 기본 시간 설정됨: {duration}분",
        select_reminder="새 회의의 기본 알림 선택:\n\n_인라인 쿼리에서 `r 10m`을 사용하여 회의별로 재정의할 수 있습니다._",
        reminder_set="기본 알림 설정됨: {reminder}",
        reminder_override_hint="_쿼리에서 `r`을 사용하여 기본값을 적용하거나 `r 10m`으로 특정 시간을 지정하세요._",
        notifications_title="**회의 알림** 🔔",
        notifications_status="상태: {status}",
        notifications_explanation="활성화하면 설정한 알림 시간에 따라 회의 전에 텔레그램 알림을 받습니다.",
        select_option="옵션 선택:",
        enable_button="활성화",
        disable_button="비활성화",
        current_suffix="(현재)",
        notifications_updated="{emoji} 회의 알림 {status}.",
        will_receive_reminders="이제 회의 전에 알림을 받게 됩니다.",
        will_not_receive_reminders="더 이상 회의 알림을 받지 않습니다.",
        select_language="🌍 선호하는 언어 선택:",
        language_updated="✅ 언어가 성공적으로 업데이트되었습니다!",
        privacy_title="**개인정보 설정** 🔒",
        privacy_username_invites="@사용자명 초대 허용",
        privacy_enabled_desc="다른 사람들이 @사용자명으로 회의에 초대할 수 있습니다",
        privacy_disabled_desc="직접 이메일 초대만 작동합니다",
        privacy_updated="{emoji} 사용자명 초대 {status}.",
        # Default calendar preference
        default_calendar_label="기본 캘린더",
        default_calendar_requires_both="기본 설정을 지정하려면 Google과 Outlook 캘린더가 모두 연결되어 있어야 합니다.\n\n/connect를 사용하여 둘 다 연결하세요.",
        default_calendar_title="**기본 캘린더** 🎯",
        default_calendar_desc="회의 생성 시 기본으로 사용할 캘린더를 선택하세요.\n\n편집 메뉴에서 개별 회의의 캘린더를 변경할 수 있습니다.",
        default_calendar_updated="✅ 기본 캘린더가 {calendar}로 설정되었습니다.\n\n새 회의는 거기에 생성됩니다.",
        # Unified connect/disconnect
        connect_services_title="**서비스 연결** 🔗",
        connect_select_service="연결할 서비스를 선택하세요:",
        connect_another_service="다른 서비스 연결:",
        connected_services_title="**연결된 서비스**",
        manage_button="⚙️ 관리",
        disconnect_services_title="**서비스 연결 해제** 🔌",
        disconnect_select_service="연결 해제할 서비스를 선택하세요:",
        no_services_connected="연결된 서비스가 없습니다.\n\n/connect를 사용하여 캘린더를 연결하세요.",
        service_disconnected="✅ {service} 연결이 해제되었습니다.",
    ),
    meetings=MeetingsTranslations(
        upcoming_meetings="**예정된 회의** 📅",
        no_upcoming_meetings="예정된 회의가 없습니다.",
        use_cancel_hint="_회의를 취소하려면 /cancel 사용_",
        attendees_count="👥 {count}명 참석자",
        privacy_mode_note="_🔒 개인정보 보호 모드: 봇이 만든 일정만 표시됩니다_",
        # Meeting list and detail view
        close_button="✖️ 닫기",
        edit_button="✏️ 수정",
        cancel_meeting_button="🗑️ 취소",
        back_to_list_button="↩️ 목록으로",
        closed="일정 목록이 닫혔습니다.",
        # Edit menu
        edit_menu_title="✏️ **일정 수정**\n\n수정할 항목을 선택하세요:",
        edit_title_btn="📝 제목",
        edit_time_btn="🕐 시간",
        edit_date_btn="📅 날짜",
        edit_duration_btn="⏱️ 기간",
        edit_attendees_btn="👥 참석자",
        edit_link_btn="🔗 링크",
        switch_to_calendar="{calendar}로 이동",
        calendar_switched="✅ 회의가 {calendar}로 이동되었습니다.",
        field_updated="✅ {field} 업데이트됨",
        select_meeting_to_cancel="**취소할 회의 선택:**",
        page_info="페이지 {current}/{total}",
        total_meetings="총 {count}개 회의",
        previous_button="⬅️ 이전",
        next_button="다음 ➡️",
        dont_cancel_button="❌ 취소 안함",
        no_meeting_cancelled="✅ 취소된 회의 없음.",
        cancelling_meeting="회의 취소 중...",
        meeting_cancelled="✅ 회의 취소됨: **{title}**",
        attendees_notified="_참석자에게 자동으로 알림이 전송됩니다._",
        cancel_not_your_menu="❌ 오류: 이것은 당신의 취소 메뉴가 아닙니다.",
        session_expired="❌ 오류: 세션이 만료되었습니다. /cancel을 다시 사용하세요.",
        meeting_not_found="❌ 오류: 회의를 찾을 수 없습니다. /cancel을 다시 사용하세요.",
    ),
    inline=InlineTranslations(
        how_to_create="회의 만드는 방법",
        inline_help_description='입력: 14:30 "회의 제목" email@example.com',
        inline_help_message='회의를 만들려면 입력:\n@handycalbot 14:30 "회의 제목" email@example.com\n\n형식: 시간 [날짜] "제목" [이메일]',
        please_start_first_title="먼저 봇을 시작하세요",
        please_start_first_description="클릭하여 봇을 열고 /start 실행",
        please_start_first_message="먼저 /start를 보내 @handycalbot을 시작하세요",
        could_not_parse="회의를 분석할 수 없음",
        parse_error_description='형식 사용: 14:30 "회의 제목" emails...',
        parse_error_message='회의를 분석할 수 없습니다. 형식 사용:\n14:30 "회의 제목" email@example.com\n\n시간과 따옴표 안의 제목은 필수입니다.\n알림은 r 10m, 기본값은 r만 추가하세요.',
        calendar_not_connected_warning="⚠️ 캘린더 연결 안됨 - 먼저 /connect",
        attendees_label="👥 {count}명 참석자",
        today="오늘",
        create_meeting_button="회의 만들기",
        cancel_button="취소",
        creating_meeting="회의 생성 중...",
        meeting_data_expired="❌ 오류: 회의 데이터가 만료되었습니다. 다시 시도하세요.",
        not_your_meeting="❌ 이것은 당신의 회의가 아닙니다!",
        meeting_created="회의가 생성되었습니다!",
        reminder_label="🔔 알림: {reminder} 전",
        invitations_sent="📧 초대장 발송:",
        attendees_will_receive="_이 참석자들은 자동으로 캘린더 초대를 받습니다._",
        add_to_calendar_button="📅 내 캘린더에 추가",
        not_listed_add_calendar="_목록에 없으신가요? 아래를 클릭하여 캘린더에 추가:_",
        click_to_add_calendar="_아래를 클릭하여 캘린더에 추가:_",
        meeting_cancelled="✅ 회의가 취소되었습니다.",
        username_registered="등록됨",
        username_privacy_disabled="개인정보 비활성화",
        username_not_found="찾을 수 없음",
        pending_invites_note="⏳ 아직 미등록:",
        rate_limit_warning="⚠️ 사용자 검색이 너무 많습니다. 나중에 다시 시도하세요.",
        no_calendar_users_note="⚠️ 등록됨, 캘린더 미연결:",
        privacy_disabled_users_note="🔒 개인정보 비활성화 (초대 미발송):",
        register_link_text="등록하기",
        # Edit menu
        edit_button="편집",
        edit_menu_title="✏️ *회의 편집*\n\n무엇을 변경하시겠습니까?",
        edit_title_button="📝 제목",
        edit_time_button="🕐 시간",
        edit_date_button="📅 날짜",
        edit_duration_button="⏱️ 길이",
        edit_reminder_button="🔔 알림",
        edit_attendees_button="👥 참석자",
        edit_link_button="🔗 링크 추가",
        back_button="↩️ 뒤로",
        done_editing_button="✅ 완료",
        # Edit prompts
        enter_new_title='📝 *새 제목 입력*\n\n현재: "{current}"\n\n새 제목을 입력하고 보내세요.',
        enter_new_time="🕐 *새 시간 입력*\n\n현재: {current}\n\n새 시간(HH:MM)을 입력하고 보내세요.",
        enter_new_date="📅 *새 날짜 입력*\n\n현재: {current}\n\n새 날짜(DD-MM-YYYY)를 입력하고 보내세요.",
        select_duration="⏱️ *길이 선택*",
        select_reminder="🔔 *알림 선택*",
        # Attendees
        current_attendees="*현재 참석자:*",
        add_attendee_prompt="👥 *참석자 추가*\n\n이메일 주소 또는 @사용자명을 입력하고 보내세요.",
        recent_contacts_title="*최근 연락처:*",
        no_recent_contacts="최근 연락처 없음",
        type_manually_button="✍️ 이메일/@사용자명 입력",
        remove_attendee_button="🗑️",
        attendee_added="✅ 참석자 추가됨: {attendee}",
        attendee_removed="✅ 참석자 제거됨: {attendee}",
        invalid_email_format="❌ 잘못된 형식입니다. email@example.com 또는 @사용자명을 사용하세요",
        no_attendees="아직 참석자가 없습니다",
        # Link
        add_link_title="🔗 *회의 링크*",
        invalid_link_format="❌ 잘못된 링크입니다. http:// 또는 https://로 시작하는 URL을 입력하세요",
        invalid_time_format="❌ 잘못된 시간 형식입니다. 14:00, 2pm 또는 14.30을 시도하세요",
        invalid_date_format="❌ 잘못된 날짜 형식입니다. 내일, Jan 20 또는 20-01을 시도하세요",
        auto_google_meet="🎥 자동 Google Meet",
        auto_teams_meeting="📹 자동 Microsoft Teams",
        auto_zoom_meeting="📹 자동 Zoom 회의",
        paste_custom_link="📋 사용자 정의 링크 붙여넣기",
        enter_link_prompt="🔗 *회의 링크 입력*\n\n회의 URL을 붙여넣으세요.",
        link_added="✅ 링크 추가됨",
        link_removed="✅ 링크 제거됨",
        remove_link_button="🗑️ 링크 제거",
        google_meet_label="🎥 Google Meet",
        teams_meeting_label="📹 Microsoft Teams",
        zoom_meeting_label="📹 Zoom 회의",
        zoom_not_connected="Zoom이 연결되지 않았습니다. 먼저 /connect를 사용하세요.",
        outlook_not_connected="Outlook이 연결되지 않았습니다. 먼저 /connect를 사용하세요.",
        custom_link_label="🔗 회의 링크",
        # Updates
        field_updated="✅ {field} 업데이트됨",
        meeting_updated="회의 업데이트됨",
        # Duration options
        duration_15_min="15분",
        duration_30_min="30분",
        duration_45_min="45분",
        duration_1_hour="1시간",
        duration_1_5_hours="1.5시간",
        duration_2_hours="2시간",
        # Reminder options
        reminder_none="없음",
        reminder_5_min="5분",
        reminder_10_min="10분",
        reminder_15_min="15분",
        reminder_30_min="30분",
        reminder_1_hour="1시간",
        reminder_1_day="1일",
        # Cancel edit
        cancel_edit_button="❌ 취소",
        edit_cancelled="편집 취소됨",
        # Private chat prompts (for text input redirect)
        continue_in_private="이것을 편집하려면 비공개 채팅에서 계속하세요:",
        open_private_chat="💬 비공개 채팅 열기",
        session_expired_restart="세션이 만료되었습니다. 원본 메시지에서 편집을 다시 시작하세요.",
        edit_complete_return="✅ 완료! 메시지가 업데이트되었습니다.",
        back_to_chat_button="↩️ 채팅으로 돌아가기",
        # Time selection grid
        select_time_title="🕐 *시간 선택*",
        time_morning="오전",
        time_afternoon="오후",
        custom_time_button="⌨️ 사용자 정의",
        # Date selection grid
        select_date_title="📅 *날짜 선택*",
        date_today="오늘",
        date_tomorrow="내일",
        date_day_after="모레",
        date_in_3_days="3일 후",
        date_in_a_week="일주일 후",
        custom_date_button="⌨️ 사용자 정의",
    ),
    donation=DonationTranslations(
        support_title="**HandyCalBot 후원하기** ⭐",
        support_description="이 봇이 유용하다면 Telegram Stars로 개발을 지원해 주세요!",
        support_helps="여러분의 지원은 봇 운영과 새로운 기능 개발에 도움이 됩니다.",
        select_amount="금액 선택:",
        custom_amount_button="💫 직접 입력",
        custom_amount_prompt="**직접 후원** 💫\n\n후원할 Stars 수를 입력하세요 (1-10000):",
        invalid_amount="1에서 10000 사이의 유효한 금액을 입력하세요.",
        invalid_number="유효한 숫자를 입력하세요 (1-10000).",
        donation_error="죄송합니다, 후원 처리 중 오류가 발생했습니다. 나중에 다시 시도해 주세요.",
        thank_you="**후원해 주셔서 감사합니다!** 🙏",
        you_donated="{amount} Telegram Stars를 후원해 주셨습니다. 여러분의 지원에 감사드립니다!",
        thank_you_running="HandyCalBot 운영을 도와주셔서 감사합니다! ⭐",
    ),
    reminder=ReminderTranslations(
        meeting_reminder="🔔 *회의 알림*",
        starting_in="{time} 후 시작",
    ),
    feedback=FeedbackTranslations(
        feedback_title="📝 **피드백**",
        feedback_prompt="피드백, 버그 신고 또는 제안을 작성해 주세요.",
        feedback_abort_hint="취소하려면 /abort를 입력하세요.",
        feedback_received="✅ 피드백 감사합니다!",
        feedback_thank_you="메시지가 접수되어 검토될 예정입니다.",
    ),
    commands=CommandTranslations(
        start="봇 시작 및 환영 메시지",
        help="도움말 및 사용법",
        meetings="예정된 회의 목록",
        cancel="회의 취소",
        connect="캘린더 또는 Zoom 연결",
        disconnect="서비스 연결 해제",
        settings="설정 보기",
        timezone="시간대 변경",
        duration="기본 시간 설정",
        reminder="기본 알림 설정",
        notifications="알림 켜기/끄기",
        privacy="@사용자명 초대 개인정보 설정",
        language="언어 변경",
        donate="Stars로 봇 후원",
        feedback="피드백 보내기 또는 버그 신고",
    ),
)
