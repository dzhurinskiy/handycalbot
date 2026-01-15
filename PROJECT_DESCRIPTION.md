# CalendarBot - Project Description

## Overview

CalendarBot is a Telegram bot that enables users to schedule calendar meetings directly from any Telegram chat using inline commands. The bot integrates with external calendar services (Google Calendar, Outlook) and sends meeting invitations to specified attendees.

---

## Core Features

### 1. Inline Meeting Creation (MVP)
**Command syntax:**
```
@CalendarBot 14:30 25-01-2026 "Project Sync" john@example.com, jane@example.com
@CalendarBot 10:00 "Daily Standup"  # Uses current date
@CalendarBot 16:00 "Quick Call"     # No attendees, just blocks time
```

**Parameters:**
| Parameter | Format | Required | Description |
|-----------|--------|----------|-------------|
| Time | HH:MM | Yes | Meeting start time (24h format) |
| Date | DD-MM-YYYY | No | Defaults to user's local date |
| Title | "quoted string" | Yes | Meeting title |
| Attendees | email1, email2 | No | Comma-separated emails |

### 2. User Configuration (Settings)
- Connect/disconnect email accounts (OAuth2)
- Set default meeting duration (15/30/45/60 min)
- Set timezone preference
- Set default calendar

### 3. Meeting Management
- `/meetings` - List upcoming meetings
- `/cancel <meeting_id>` - Cancel a meeting
- `/reschedule <meeting_id> <new_time>` - Reschedule

### 4. Calendar Integration
- Google Calendar API
- Microsoft Outlook/Graph API (future phase)

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         TELEGRAM CLOUD                               │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Webhook / Long Polling
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                            VPS (Docker)                              │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                      NGINX (Reverse Proxy)                    │   │
│  │                    SSL Termination + Rate Limiting            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                    │                                 │
│                                    ▼                                 │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     BOT SERVICE (Python)                      │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │   │
│  │  │  Telegram   │  │  Command    │  │  Calendar           │  │   │
│  │  │  Handler    │──│  Parser     │──│  Service            │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘  │   │
│  │         │                                     │              │   │
│  │         ▼                                     ▼              │   │
│  │  ┌─────────────┐                    ┌─────────────────────┐  │   │
│  │  │  User       │                    │  OAuth Token        │  │   │
│  │  │  Service    │                    │  Manager            │  │   │
│  │  └─────────────┘                    └─────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                    │                                 │
│                                    ▼                                 │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     POSTGRESQL DATABASE                       │   │
│  │    users │ oauth_tokens │ meetings │ user_settings           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │     EXTERNAL CALENDAR APIs    │
                    │   Google Calendar │ Outlook   │
                    └───────────────────────────────┘
```

### Why This Architecture?

**For 1-10k users, a simple monolithic approach is optimal:**
- No need for microservices complexity
- Single Python service handles everything
- Horizontal scaling not needed at this scale
- Easy to deploy, monitor, and debug

**Estimated load:**
- 10k users × ~5 commands/day = 50k requests/day
- ~0.6 requests/second average
- Single Python process handles this easily

---

## Technology Stack

| Component | Technology | Justification |
|-----------|------------|---------------|
| Language | Python 3.12+ | Rich Telegram bot ecosystem, async support |
| Bot Framework | python-telegram-bot v20+ | Async, well-maintained, inline query support |
| Web Framework | FastAPI | OAuth callbacks, health checks, webhooks |
| Database | PostgreSQL 15+ | Reliable, good JSON support, scalable |
| ORM | SQLAlchemy 2.0 + Alembic | Type hints, async, migrations |
| Task Queue | None (phase 1) / Celery (if needed) | Overkill for this scale initially |
| Caching | None (phase 1) / Redis (if needed) | DB queries fast enough at this scale |
| Containerization | Docker + Docker Compose | Consistent environments, easy deployment |
| Reverse Proxy | Nginx | SSL, rate limiting, static files |
| CI/CD | GitHub Actions | Free, well-integrated, reliable |

---

## Monorepo Structure

```
calendarbot/
├── .github/
│   └── workflows/
│       ├── ci.yml              # Lint, test, type-check
│       ├── cd.yml              # Deploy to VPS
│       └── security.yml        # Dependency scanning
│
├── src/
│   └── calendarbot/
│       ├── __init__.py
│       ├── main.py             # Application entry point
│       ├── config.py           # Settings management
│       │
│       ├── bot/                # Telegram bot logic
│       │   ├── __init__.py
│       │   ├── handlers/       # Command handlers
│       │   │   ├── __init__.py
│       │   │   ├── start.py
│       │   │   ├── meetings.py
│       │   │   ├── settings.py
│       │   │   └── inline.py   # Inline query handler
│       │   ├── keyboards.py    # Reply keyboards
│       │   └── filters.py      # Custom filters
│       │
│       ├── api/                # FastAPI routes
│       │   ├── __init__.py
│       │   ├── oauth.py        # OAuth callbacks
│       │   └── health.py       # Health checks
│       │
│       ├── services/           # Business logic
│       │   ├── __init__.py
│       │   ├── calendar.py     # Calendar operations
│       │   ├── user.py         # User management
│       │   └── parser.py       # Command parsing
│       │
│       ├── integrations/       # External APIs
│       │   ├── __init__.py
│       │   ├── google.py       # Google Calendar
│       │   └── outlook.py      # Microsoft Graph
│       │
│       ├── db/                 # Database layer
│       │   ├── __init__.py
│       │   ├── models.py       # SQLAlchemy models
│       │   ├── repository.py   # Data access
│       │   └── migrations/     # Alembic migrations
│       │
│       └── utils/              # Utilities
│           ├── __init__.py
│           ├── timezone.py
│           └── encryption.py   # Token encryption
│
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_parser.py
│   │   ├── test_calendar.py
│   │   └── test_user.py
│   ├── integration/
│   │   ├── test_bot_handlers.py
│   │   └── test_oauth_flow.py
│   └── e2e/
│       └── test_full_flow.py
│
├── docker/
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   └── nginx/
│       └── nginx.conf
│
├── scripts/
│   ├── deploy.sh
│   ├── backup_db.sh
│   └── setup_dev.sh
│
├── docker-compose.yml          # Production
├── docker-compose.dev.yml      # Development
├── pyproject.toml              # Project config + dependencies
├── alembic.ini                 # Migration config
├── .env.example                # Environment template
├── .gitignore
├── README.md
└── PROJECT_DESCRIPTION.md      # This file
```

---

## Database Schema

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    telegram_username VARCHAR(255),
    timezone VARCHAR(50) DEFAULT 'UTC',
    default_duration INTEGER DEFAULT 30,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- OAuth tokens (encrypted)
CREATE TABLE oauth_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL,  -- 'google', 'outlook'
    access_token_encrypted TEXT NOT NULL,
    refresh_token_encrypted TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    calendar_id VARCHAR(255),  -- Default calendar
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, provider)
);

-- Meetings (local cache for quick listing)
CREATE TABLE meetings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    external_id VARCHAR(255) NOT NULL,  -- Google/Outlook event ID
    provider VARCHAR(50) NOT NULL,
    title VARCHAR(500),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    attendees JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, external_id, provider)
);

-- Indexes
CREATE INDEX idx_users_telegram_id ON users(telegram_id);
CREATE INDEX idx_meetings_user_start ON meetings(user_id, start_time);
CREATE INDEX idx_oauth_user_provider ON oauth_tokens(user_id, provider);
```

---

## Security Considerations

1. **OAuth Token Storage**
   - Encrypt tokens at rest using Fernet (AES-128)
   - Encryption key from environment variable
   - Never log tokens

2. **Rate Limiting**
   - Nginx: 10 req/s per IP
   - Bot level: 5 commands/minute per user

3. **Input Validation**
   - Sanitize all user input
   - Validate email formats
   - Limit title length (500 chars)

4. **Secrets Management**
   - All secrets via environment variables
   - `.env` file never committed
   - Separate secrets for dev/staging/prod

---

## CI/CD Pipeline

### Continuous Integration (on every push)
```yaml
steps:
  - Checkout code
  - Setup Python 3.12
  - Install dependencies
  - Run linters (ruff, black)
  - Run type checker (mypy)
  - Run tests (pytest)
  - Check test coverage (>80%)
  - Build Docker image
  - Run security scan (trivy)
```

### Continuous Deployment (on merge to main)
```yaml
steps:
  - Build production Docker image
  - Push to container registry
  - SSH to VPS
  - Pull new image
  - Run database migrations
  - Rolling restart (docker-compose)
  - Health check
  - Notify on Telegram (success/failure)
```

---

## Development Workflow

### Local Development
```bash
# Clone and setup
git clone <repo>
cd calendarbot
cp .env.example .env  # Configure secrets

# Start services
docker-compose -f docker-compose.dev.yml up -d

# Run bot locally (outside docker for hot-reload)
python -m src.calendarbot.main
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/calendarbot --cov-report=html

# Run specific test
pytest tests/unit/test_parser.py -v
```

---

## Deployment Requirements

### VPS Specifications (for 1-10k users)
- **CPU**: 2 vCPU
- **RAM**: 4 GB
- **Storage**: 40 GB SSD
- **OS**: Ubuntu 22.04 LTS

### Required Services
- Docker + Docker Compose
- Nginx (in Docker)
- PostgreSQL (in Docker)
- Certbot for SSL (Let's Encrypt)

### Domain/DNS
- Domain with A record pointing to VPS
- SSL certificate (Let's Encrypt auto-renewal)

---

## External Service Setup Required

1. **Telegram Bot**
   - Create bot via @BotFather
   - Enable inline mode
   - Get bot token

2. **Google Cloud Console**
   - Create project
   - Enable Google Calendar API
   - Create OAuth 2.0 credentials
   - Configure consent screen
   - Add redirect URI

3. **Container Registry** (optional)
   - Docker Hub or GitHub Container Registry
   - For storing built images

---

## Implementation Phases

### Phase 1: MVP (Core Functionality)
- Basic bot setup with inline queries
- Google Calendar integration only
- Meeting creation with time/title/attendees
- User settings (timezone, connect Google)
- PostgreSQL storage
- Docker deployment
- Basic CI/CD

### Phase 2: Enhanced Features
- `/meetings` list view
- Cancel/reschedule meetings
- Meeting reminders
- Improved error handling
- Comprehensive logging

### Phase 3: Expansion
- Microsoft Outlook integration
- Multiple calendar support
- Meeting templates
- Analytics dashboard

---

## Claude Code Tips

Here are the commands you'll find useful:

```bash
# Start Claude Code
claude

# In Claude Code, useful commands:
/help          # Show all available commands
/clear         # Clear conversation context
/compact       # Reduce context size

# When working on tasks:
# - I'll create todo lists to track progress
# - I can run bash commands, create/edit files
# - I can search the codebase with grep/glob

# To give me specific permissions:
# - I'll ask before running potentially destructive commands
# - You can pre-approve certain operations

# For long tasks:
# - I can run commands in background
# - You can check on progress anytime
```

---

## Next Steps

Once you approve this architecture:

1. **Initialize project structure** - Create all directories and config files
2. **Setup Docker environment** - Dockerfile, docker-compose
3. **Implement database models** - SQLAlchemy + Alembic migrations
4. **Build bot skeleton** - Basic command handlers
5. **Add Google OAuth** - Connect calendar accounts
6. **Implement inline queries** - The core meeting creation feature
7. **Setup CI/CD** - GitHub Actions workflows
8. **Deploy to VPS** - Production setup

---

## Questions for You

Before we proceed, please confirm:

1. **Bot username**: What should the bot be called? (e.g., @YourCalendarBot)
2. **Default meeting duration**: 30 minutes?
3. **Google Calendar only for MVP**: OK to add Outlook later?
4. **VPS provider**: Which provider? (for deployment scripts)
5. **Domain**: Do you have a domain for OAuth callbacks?

---

*Document created: 2026-01-15*
*Author: CalendarBot CTO (Claude)*
