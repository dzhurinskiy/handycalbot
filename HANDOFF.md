# HandyCalBot — где остановились

Только состояние на дату. Постоянное (устройство, сборка, деплой, i18n, правила VPS) — в `CLAUDE.md`.
История до bb — `docs/legacy/HANDOFF.md`.

## Сводка на 2026-10-03

- Прод работает: `https://handycal.bot/health` → 200 (проверено 3 октября).
- Последняя фича — ссылка Zoom / Google Meet в напоминании (`3210a29`, 28 августа), CI и CD прошли.
- Логи контейнера после этого деплоя не проверены: на klava нет SSH-алиаса `handycal`.
- Новых задач нет; проект ждёт решения Сергея о следующем шаге.

## Напоминания и ссылки на встречи

**Готово**
- 28.08.2026: ссылка на встречу (Zoom / Google Meet из location/description события) в тексте напоминания;
  миграция `011_meeting_url`; коммит `3210a29` в `master`, GitHub Actions CI ✅ CD ✅.
- Ранее: исправлен разбор команды напоминания, съедавший адреса вида `r.email@domain.com` (`47a00df`).

**Открыто**
- Не проверены логи `calendarbot` после деплоя `3210a29` на `ERROR` / `Exception` / `Traceback`.

## Домен и деплой

**Готово**
- Основной домен `handycal.bot`, `handycal.dzhurinskiy.com` редиректит (`20d01f6`, `.env.example` — `a176952`).

**Открыто**
- На klava нет SSH-алиаса `handycal` (из `CLAUDE.md`), поэтому логи и состояние VPS отсюда недоступны.
- `cd.yml` запускает деплой на любой push в `master`, включая docs-only (нет `paths-ignore`).
- В `cd.yml` `ZOOM_REDIRECT_URI` и `OUTLOOK_REDIRECT_URI` всё ещё на `handycal.dzhurinskiy.com` — работает через
  редирект; переводить ли на `handycal.bot`, не решалось.

**Решения Сергея**
- Токен в git remote локального клона оставлен намеренно, не трогать.

**Вопросы к Сергею**
- Нужен ли доступ к VPS с klava? Если да — добавить SSH-алиас `handycal` с ключом, затем проверить логи.
- Добавить ли в `cd.yml` `paths-ignore` для `**.md` / `docs/**`, чтобы docs-only коммиты не деплоили?
- Этот коммит (CLAUDE.md + HANDOFF.md) лежит в локальном `master` и не запушен: push вызовет деплой. Пушить?

## Интеграции и функциональность (январь 2026, по заголовкам сессий)

**Готово**
- Google Calendar (OAuth, верификация, видео-сценарий), Outlook Calendar, Zoom (комплаенс Zoom Marketplace),
  выбор календаря при нескольких провайдерах, единые `/connect` / `/disconnect`, privacy mode и @username,
  многошаговое редактирование встречи, донаты, 10 языков.

**Открыто**
- Задач нет.

## Ссылки

- История до bb: `docs/legacy/HANDOFF.md` (логи сессий — `/home/klava/legacy-sessions/server/-home-klava-handycalbot/`).
- CI/CD: GitHub Actions репозитория `dzhurinskiy/handycalbot` (`gh run list --limit 5`).
