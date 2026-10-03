# Claude Code Instructions

> Постоянный слой: устройство проекта, сборка, деплой, договорённости. Состояние на дату (готово / открыто /
> вопросы к Сергею) — в `HANDOFF.md` в корне. История до bb — `docs/legacy/` (не редактировать).

## Project Overview

- HandyCalBot — личный проект Сергея (не Warp): Telegram-бот для назначения встреч из любого чата
  (inline-режим и личный чат) с интеграцией Google Calendar, Outlook Calendar и Zoom.
- Стек: Python 3.12, python-telegram-bot (webhooks), FastAPI + uvicorn, SQLAlchemy async + asyncpg (PostgreSQL),
  Alembic, Docker Compose, nginx.
- Код: `src/calendarbot/` — `bot/` (хендлеры), `api/` (FastAPI, OAuth-коллбэки, `/health`), `integrations/`
  (Google, Outlook, Zoom), `services/`, `db/` (модели и миграции), `i18n/`, `static/`; точка входа
  `calendarbot.main`. Тесты: `tests/` (`unit`, `integration`, `e2e`). Скрипты: `scripts/`. Docker: `docker/`.
- Локальный запуск: `pip install -e ".[dev]"`, `cp .env.example .env`,
  `docker compose -f docker-compose.dev.yml up -d db`, `python -m calendarbot.main` (подробнее — `README.md`).
- Проверки (как в CI): `ruff check src/`, `black --check src/`, `mypy src/calendarbot --ignore-missing-imports`,
  `pytest tests/ -v` (нужен PostgreSQL; переменные `DATABASE_URL`, `TELEGRAM_BOT_TOKEN`, `ENCRYPTION_KEY`).
- Production: домен `handycal.bot` (`handycal.dzhurinskiy.com` редиректит на него), health —
  `https://handycal.bot/health`. На VPS код в `/opt/handycal`, контейнеры `calendarbot` и `calendarbot-db`.
- Переменные окружения: список — `.env.example` и `.github/workflows/cd.yml`. Значения — только в GitHub Secrets
  (`TELEGRAM_BOT_TOKEN`, `DB_PASSWORD`, `GOOGLE_CLIENT_ID`/`_SECRET`, `GOOGLE_REDIRECT_URI`, `ENCRYPTION_KEY`,
  `WEBHOOK_URL`, `ADMIN_CHAT_ID`, `ZOOM_CLIENT_ID`/`_SECRET`, `OUTLOOK_CLIENT_ID`/`_SECRET`, `VPS_HOST`,
  `VPS_USER`, `VPS_SSH_KEY`). `ZOOM_REDIRECT_URI` и `OUTLOOK_REDIRECT_URI` захардкожены в `cd.yml`.
- Документация интеграций: `docs/GOOGLE_OAUTH_SETUP.md`, `docs/OUTLOOK_SETUP.md`, `docs/security/`,
  `docs/google-oauth-video-script.md`.

## CI/CD — push в master = деплой

- `.github/workflows/ci.yml`: lint (ruff, black, mypy), тесты на PostgreSQL 15, сборка Docker-образа.
- `.github/workflows/cd.yml`: на каждый push в `main`/`master` (без `paths-ignore`, т.е. и для docs-only)
  SSH на VPS → `git reset --hard origin/master` → генерация `.env` из Secrets → `docker compose build` и `up --wait`
  → `alembic upgrade head` → проверка логов → уведомление в Telegram.
- Поэтому push в master — это production deploy; порядок действий и проверки — разделы «Deployment workflow» и «Deployment Verification» ниже.

## Project Management

- Be proactive and autonomous - do as much work as needed without asking for permission
- The user manages the project, Claude codes and executes tasks
- When something needs to be done (VPS setup, deployments, fixes), just do it
- Only ask questions when truly blocked or need critical business decisions

## Git/SSH

- Always use SSH keys for Git and VPS connections, never prompt for passwords
- The VPS at 164.92.157.14 should be accessed via SSH key authentication
- GitHub remote should use SSH URL format: `git@github.com:dzhurinskiy/handycalbot.git`

## VPS Connection Management - CRITICAL RULES

**NEVER violate these rules - they prevent VPS lockups that require power cycling:**

1. **ONE SSH connection at a time** - NEVER run SSH in parallel, NEVER use background mode for SSH
2. **Chain all commands** - Use `&&` to run multiple commands in a single SSH call
3. **Always use timeout** - Every SSH command must include `-o ConnectTimeout=10`
4. **Prefer HTTPS health checks** - Use `curl https://handycal.dzhurinskiy.com/health` instead of SSH when possible
5. **Trust the CI/CD** - After `git push`, let GitHub Actions handle deployment. Don't SSH to monitor.
6. **Max 1 SSH per minute** - Wait at least 60 seconds between SSH connections

**Standard SSH command format (use the handycal alias from ~/.ssh/config):**
```bash
ssh -o ConnectTimeout=10 -o BatchMode=yes handycal "command1 && command2 && command3"
```

- `handycal` - SSH alias configured in `~/.ssh/config` with correct key and host
- `-o BatchMode=yes` - REQUIRED: prevents password prompts, fails fast if key doesn't work

**Deployment workflow:**
1. Make code changes
2. `git push` - triggers GitHub Actions
3. Wait for Telegram notification (success/failure)
4. Verify via HTTPS: `curl https://handycal.dzhurinskiy.com/health`
5. **ALWAYS check logs after deployment** - even if health check passes:
   ```bash
   ssh -o ConnectTimeout=10 -o BatchMode=yes handycal "docker logs calendarbot --tail=50 2>&1"
   ```
6. Look for `ERROR`, `Exception`, or `Traceback` in logs
7. If errors found, fix them and redeploy

## Database Migrations

- Use Alembic for database migrations
- **Keep revision IDs short** - max 32 characters (e.g., `001_default_reminder`, not `001_add_default_reminder_column`)
- After adding new model fields, create a migration file in `src/calendarbot/db/migrations/versions/`
- CD workflow runs `alembic upgrade head` automatically
- If migrations fail, you may need to manually stamp: `docker exec calendarbot alembic stamp head`
- To apply columns manually if migration fails:
  ```bash
  ssh handycal "docker exec calendarbot-db psql -U calendarbot -d calendarbot -c 'ALTER TABLE ... ADD COLUMN ...'"
  ```

## Environment & Deployment

- GitHub Secrets are the source of truth for all environment variables
- The `.env` file is recreated during CI/CD automated deployment from GitHub Secrets
- Never manually edit `.env` on VPS - update GitHub Secrets instead and redeploy
- Production domain: `handycal.bot` (старый `handycal.dzhurinskiy.com` редиректит)

## Deployment Verification - CRITICAL

**After every `git push`, you MUST verify deployment success:**

1. **Check GitHub Actions** - Go to the repository's Actions tab or use `gh run list` to see the latest workflow runs
2. **Both CI and CD must pass**:
   - CI (lint/tests) - runs ruff linter and any tests
   - CD (deploy) - deploys to VPS
3. **If CI fails (lint errors)**:
   - Read the error output carefully
   - Fix all lint errors (unused imports, import sorting, f-strings without placeholders, unused arguments)
   - Push again and verify
4. **Repeat until fully successful** - Never consider deployment done until both CI and CD show green checkmarks

**Common lint errors to watch for:**
- Unused imports: Remove them
- Import blocks unsorted: Use `ruff --fix` or manually sort (stdlib → third-party → local)
- f-strings without placeholders: Remove the `f` prefix
- Unused function arguments: Prefix with underscore (e.g., `_context`)

**Quick verification command:**
```bash
gh run list --limit 5
```

## i18n / Translations

- All translation files are in `src/calendarbot/i18n/`
- English (`en.py`) is the reference - all other languages must match its structure
- Supported languages: en, de, es, fr, ru, ja, ko, zh, id, fa (10 total)

### Emoji Consistency - CRITICAL

**Emojis must be identical across ALL language files.** This is a systemic issue that must be checked.

**Emoji checking algorithm:**
1. Identify all emojis in the English (`en.py`) file
2. For each emoji found, note its exact position (which field/string it's in)
3. Apply the EXACT SAME English emojis to all other language files
4. Do NOT localize emojis - use the English emoji as-is with localized text

**Example:**
- English: `add_to_calendar_button="📅 Add to My Calendar"`
- German: `add_to_calendar_button="📅 Zu meinem Kalender hinzufugen"` (same 📅 emoji)
- Russian: `add_to_calendar_button="📅 Добавить в мой календарь"` (same 📅 emoji)

**Common emoji locations in English that MUST be present in all languages:**
- `welcome_message`: 📅, 1️⃣, 2️⃣
- `help_message`: 📅
- `your_settings`: ⚙️
- `notifications_title`: 🔔
- `privacy_title`: 🔒
- `select_language`: 🌍
- `upcoming_meetings`: 📅
- `attendees_count` / `attendees_label`: 👥
- `previous_button`: ⬅️
- `next_button`: ➡️
- `dont_cancel_button`: ❌
- `reminder_label` (inline): 🔔
- `invitations_sent`: 📧
- `support_title` / `support_button`: ⭐
- `custom_amount_button` / `custom_amount_prompt`: 💫
- `thank_you`: 🙏
- `thank_you_running`: ⭐
- `meeting_reminder`: 🔔
- `connect_button`: 🔗
- `feedback_title`: 📝
- `add_to_calendar_button`: 📅
- `pending_invites_note`: ⏳
- `rate_limit_warning` / `calendar_not_connected_warning` / `no_calendar_users_note`: ⚠️
- `privacy_disabled_users_note`: 🔒
- `pending_invites_found`: 🎉
- `pending_invite_notification`: 📅, 🕐

**When making i18n changes:**
1. Always add/modify English first
2. Copy the exact emoji pattern to all other language files
3. Verify by grepping for emojis: `grep -n "📅\|⚙️\|🔔" src/calendarbot/i18n/*.py`

> История до bb: `docs/legacy/HANDOFF.md` — прочитай при работе над напоминаниями, OAuth/календарными интеграциями и деплоем.
> Текущее состояние — `HANDOFF.md` в корне.
