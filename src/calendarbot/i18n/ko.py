"""Korean translations for CalendarBot."""

from calendarbot.i18n.base import (
    CommandTranslations,
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
        please_start_first="먼저 /start를 실행해 주세요.",
        cancelled="취소되었습니다.",
        error_user_not_found="오류: 사용자를 찾을 수 없습니다.",
    ),
    start=StartTranslations(
        welcome_message="""
*HandyCalBot*에 오신 것을 환영합니다!

텔레그램에서 직접 회의를 예약할 수 있도록 도와드립니다.

*빠른 시작:*
1. /connect로 Google 캘린더 연결
2. 아무 채팅에서 @handycalbot 입력하여 회의 생성

*인라인 사용법:*
`@handycalbot 14:30 "회의 제목" email@example.com`
`@handycalbot 10:00 25-01-2026 "프로젝트 동기화"`
`@handycalbot 14:30 "회의" r 10m` (알림 포함)

*모든 명령어:*
/start - 환영 메시지
/help - 도움말 및 사용법
/connect - Google 캘린더 연결
/disconnect - 캘린더 연결 해제
/meetings - 예정된 회의 목록
/cancel - 회의 취소
/settings - 설정 보기
/timezone - 시간대 변경
/duration - 기본 시간 설정
/reminder - 기본 알림 설정
/notifications - 알림 켜기/끄기
/language - 언어 변경
/donate - 봇 후원하기
""",
        help_message="""
*HandyCalBot 도움말*

*회의 만들기 (인라인):*
아무 채팅에서 `@handycalbot` 입력 후:
- 시간 (필수): `HH:MM` (24시간 형식)
- 날짜 (선택): `DD-MM-YYYY`
- 제목 (필수): `"회의 제목"`
- 참석자 (선택): `email@example.com`
- 알림 (선택): `r 10m` 또는 `r 10m/30m` 또는 `r`

*알림 형식:*
- `r 10m` - 10분 전 알림
- `r 1h` - 1시간 전 알림
- `r 1d` - 1일 전 알림
- `r 10m/30m` - 여러 알림
- `r` - 기본 알림 사용
- (r 없음) - 알림 없음

*예시:*
`@handycalbot 14:30 "팀 스탠드업"`
`@handycalbot 10:00 25-01-2026 "리뷰" kim@co.com`
`@handycalbot 16:00 "빠른 통화" r 15m`
`@handycalbot 14:00 "회의" lee@co.com r 10m/1h`

*모든 명령어:*
/start - 환영 메시지
/help - 이 도움말
/connect - Google 캘린더 연결
/disconnect - 캘린더 연결 해제
/meetings - 예정된 회의 보기
/cancel - 회의 취소
/settings - 설정 보기
/timezone - 시간대 설정
/duration - 기본 회의 시간 설정
/reminder - 기본 알림 설정
/notifications - 알림 켜기/끄기
/language - 언어 변경
/donate - Stars로 봇 후원
""",
        timezone_detected="텔레그램 언어 설정을 기반으로 시간대를 `{timezone}`로 설정했습니다. 변경하려면 /timezone을 사용하세요.",
        support_button="⭐ HandyCalBot 후원하기",
    ),
    settings=SettingsTranslations(
        your_settings="**설정**",
        timezone_label="시간대",
        duration_label="기본 시간",
        reminder_label="기본 알림",
        notifications_label="알림",
        google_calendar_label="Google 캘린더",
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
        connect_button="Google 캘린더 연결",
        calendar_disconnected="✅ Google 캘린더가 연결 해제되었습니다.\n다시 연결하려면 /connect를 사용하세요.",
        no_calendar_connected="연결된 캘린더가 없습니다.",
        select_timezone="시간대를 선택하거나 직접 입력하세요 (예: `Asia/Seoul`):",
        timezone_set="✅ 시간대 설정됨: `{timezone}`",
        timezone_set_ready='시간대 설정됨: `{timezone}`\n\n준비 완료! 회의 만들기:\n`@handycalbot 14:30 "회의 제목"`',
        invalid_timezone="❌ 잘못된 시간대: `{timezone}`\n`Asia/Seoul` 또는 `Asia/Tokyo`와 같은 유효한 시간대를 사용하세요.",
        select_duration="기본 회의 시간 선택:",
        duration_set="✅ 기본 시간 설정됨: {duration}분",
        select_reminder="새 회의의 기본 알림 선택:\n\n_인라인 쿼리에서 `r 10m`을 사용하여 회의별로 재정의할 수 있습니다._",
        reminder_set="기본 알림 설정됨: {reminder}",
        reminder_override_hint="_쿼리에서 `r`을 사용하여 기본값을 적용하거나 `r 10m`으로 특정 시간을 지정하세요._",
        notifications_title="**회의 알림**",
        notifications_status="상태: {status}",
        notifications_explanation="활성화하면 설정한 알림 시간에 따라 회의 전에 텔레그램 알림을 받습니다.",
        select_option="옵션 선택:",
        enable_button="활성화",
        disable_button="비활성화",
        current_suffix="(현재)",
        notifications_updated="{emoji} 회의 알림 {status}.",
        will_receive_reminders="이제 회의 전에 알림을 받게 됩니다.",
        will_not_receive_reminders="더 이상 회의 알림을 받지 않습니다.",
        select_language="선호하는 언어 선택:",
        language_updated="✅ 언어가 성공적으로 업데이트되었습니다!",
    ),
    meetings=MeetingsTranslations(
        upcoming_meetings="**예정된 회의**",
        no_upcoming_meetings="예정된 회의가 없습니다.",
        use_cancel_hint="_회의를 취소하려면 /cancel 사용_",
        attendees_count="{count}명 참석자",
        select_meeting_to_cancel="**취소할 회의 선택:**",
        page_info="페이지 {current}/{total}",
        total_meetings="총 {count}개 회의",
        previous_button="이전",
        next_button="다음",
        dont_cancel_button="취소 안함",
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
        attendees_label="{count}명 참석자",
        today="오늘",
        create_meeting_button="회의 만들기",
        cancel_button="취소",
        creating_meeting="회의 생성 중...",
        meeting_data_expired="❌ 오류: 회의 데이터가 만료되었습니다. 다시 시도하세요.",
        not_your_meeting="❌ 이것은 당신의 회의가 아닙니다!",
        meeting_created="회의가 생성되었습니다!",
        reminder_label="알림: {reminder} 전",
        invitations_sent="초대장 발송:",
        attendees_will_receive="_이 참석자들은 자동으로 캘린더 초대를 받습니다._",
        add_to_calendar_button="내 캘린더에 추가",
        not_listed_add_calendar="_목록에 없으신가요? 아래를 클릭하여 캘린더에 추가:_",
        click_to_add_calendar="_아래를 클릭하여 캘린더에 추가:_",
        meeting_cancelled="✅ 회의가 취소되었습니다.",
    ),
    donation=DonationTranslations(
        support_title="**HandyCalBot 후원하기**",
        support_description="이 봇이 유용하다면 Telegram Stars로 개발을 지원해 주세요!",
        support_helps="여러분의 지원은 봇 운영과 새로운 기능 개발에 도움이 됩니다.",
        select_amount="금액 선택:",
        custom_amount_button="직접 입력",
        custom_amount_prompt="**직접 후원**\n\n후원할 Stars 수를 입력하세요 (1-10000):",
        invalid_amount="1에서 10000 사이의 유효한 금액을 입력하세요.",
        invalid_number="유효한 숫자를 입력하세요 (1-10000).",
        donation_error="죄송합니다, 후원 처리 중 오류가 발생했습니다. 나중에 다시 시도해 주세요.",
        thank_you="**후원해 주셔서 감사합니다!**",
        you_donated="{amount} Telegram Stars를 후원해 주셨습니다. 여러분의 지원에 감사드립니다!",
        thank_you_running="HandyCalBot 운영을 도와주셔서 감사합니다!",
    ),
    reminder=ReminderTranslations(
        meeting_reminder="*회의 알림*",
        starting_in="{time} 후 시작",
    ),
    commands=CommandTranslations(
        start="봇 시작 및 환영 메시지",
        help="도움말 및 사용법",
        meetings="예정된 회의 목록",
        cancel="회의 취소",
        connect="Google 캘린더 연결",
        disconnect="Google 캘린더 연결 해제",
        settings="설정 보기",
        timezone="시간대 변경",
        duration="기본 시간 설정",
        reminder="기본 알림 설정",
        notifications="알림 켜기/끄기",
        language="언어 변경",
        donate="Stars로 봇 후원",
        feedback="피드백 보내기 또는 버그 신고",
    ),
)
