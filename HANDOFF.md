# HandyCalBot — где остановились

Только состояние на дату. Постоянное (устройство, сборка, деплой, i18n, правила VPS) — в `CLAUDE.md`.
История до bb — `docs/legacy/HANDOFF.md`.

## Сводка на 2026-10-06

- 06.10: inline-режим не работал — webhook смотрел на `handycal.dzhurinskiy.com/webhook`, который отдаёт 301 на
  `handycal.bot`; Telegram редиректы не выполняет. Webhook переставлен на `https://handycal.bot/webhook`, секрет
  `WEBHOOK_URL` обновлён. Доступ к VPS с klava есть (`root@164.92.157.14`, ключ из `~/.ssh`, алиаса нет).

- Прод работает: `https://handycal.bot/health` → 200 (проверено 3 октября).
- Последняя фича — ссылка Zoom / Google Meet в напоминании (`3210a29`, 28 августа), CI и CD прошли.
- Новых задач нет; проект ждёт решения Сергея о следующем шаге.

## Напоминания и ссылки на встречи

**Готово**
- 28.08.2026: ссылка на встречу (Zoom / Google Meet из location/description события) в тексте напоминания;
  миграция `011_meeting_url`; коммит `3210a29` в `master`, GitHub Actions CI ✅ CD ✅.
- Ранее: исправлен разбор команды напоминания, съедавший адреса вида `r.email@domain.com` (`47a00df`).

**Открыто**
- Логи проверены 04.10: ошибок нет, кроме ежечасных `Zoom token refresh failed` (`invalid_grant`) у трёх
  пользователей с отозванными токенами — некритично.

## Домен и деплой

**Готово**
- Основной домен `handycal.bot`, `handycal.dzhurinskiy.com` редиректит (`20d01f6`, `.env.example` — `a176952`).

**Готово (06.10)**
- Webhook Telegram: `https://handycal.bot/webhook` (setWebhook + GitHub Secret `WEBHOOK_URL`). Причина поломки —
  301 со старого домена (редирект в nginx с `20d01f6`, вступил в силу при пересоздании nginx в деплое 04.10).

**Открыто**
- SSH-алиаса `handycal` (из `CLAUDE.md`) на klava нет, но `ssh root@164.92.157.14` работает.
- В `cd.yml` `ZOOM_REDIRECT_URI` и `OUTLOOK_REDIRECT_URI` всё ещё на `handycal.dzhurinskiy.com` — работает через
  редирект; переводить ли на `handycal.bot`, не решалось.

**Решения Сергея**
- 04.10.2026: в `cd.yml` добавлен `paths-ignore: ['**.md', 'docs/**']` — docs-only коммиты больше не деплоят
  (CI в `ci.yml` по-прежнему запускается). Push `c0bbeea` и этой правки одобрен; был один деплой без изменений кода.
- Токен в git remote локального клона оставлен намеренно, не трогать.

**Вопросы к Сергею**
- Добавить SSH-алиас `handycal` в `~/.ssh/config`?
- Секреты `GOOGLE_REDIRECT_URI` / `OUTLOOK_REDIRECT_URI` и Zoom redirect в `cd.yml` всё ещё на старом домене
  (работают через 301 в браузере). Переносить на `handycal.bot` — нужно менять и в консолях Google/Microsoft/Zoom.

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
