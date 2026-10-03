# HANDOFF — handycalbot: сессии старого Claude Code

> Составлено 2026-10-03 при переносе legacy-сессий в bb. Памяти (memory/) у старого Claude по этому проекту не было.
> Проект не относится к Warp (личный сайд-продукт владельца, handycal.bot).

## Источники
- Linux: `/home/klava/legacy-sessions/server/-home-klava-handycalbot/`
  - `0db03fc7-7e9e-438e-b4ba-9177e8e92f5a.jsonl`: 2026-08-28, единственная содержательная сессия;
  - `2e82cdcf…`, `43b1bf1b…`, `ba2998e3…`, `f0078f58…`: короткие служебные запуски того же дня.
- Windows (январь 2026): `/home/klava/legacy-sessions/win-projects/C--Users-s-OneDrive-Desktop-Github-Repos-calendarbot/sessions-index.json`.
  Сохранились только заголовки 18 сессий, логов нет.

## Январь 2026 (Windows, по заголовкам)
Деплой Telegram-бота-планировщика встреч; исправление OAuth-домена; баги часовых поясов, создание встреч, страницы
privacy; сценарий видео для верификации Google OAuth; нормализация кавычек с iPhone, напоминания, донаты,
локализация; @username с защитой приватности; многошаговое редактирование встречи; ввод текста в личном чате;
переключение privacy mode; исправление ссылок на события; комплаенс Zoom Marketplace (security docs); обновление
JWT-токенов и интеграция Outlook Calendar; UX-улучшения (23.01).

## 28.08.2026 (Linux)
- Задача: добавлять ссылку на Zoom / Google Meet из location/description события в напоминание.
- Сделано: миграция Alembic `011_meeting_url`, ссылка в тексте напоминания; коммит **`3210a29`** запушен в `master`,
  GitHub Actions CI ✅ и CD ✅, `https://handycal.bot/health` → 200.
- Не проверено: логи контейнера. На klava нет SSH-алиаса `handycal` из `CLAUDE.md`. Проверка:
  `ssh handycal "docker logs calendarbot --tail=50 2>&1 | grep -iE 'error|exception|traceback' || echo clean"`.

## Что открыто
- Добавить SSH-алиас `handycal` на klava, если нужен доступ к логам (хост указан в WARP_ECOSYSTEM.md §4).
- В remote URL локального клона лежит токен; по решению Сергея оставлен как есть.
