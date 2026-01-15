# HandyCalBot

A Telegram bot for scheduling Google Calendar meetings directly from any chat.

## Features

- **Inline Meeting Creation**: Schedule meetings from any Telegram chat
- **Google Calendar Integration**: Syncs with your Google Calendar
- **Attendee Invitations**: Automatically sends calendar invites
- **Timezone Support**: Respects user timezone settings
- **Meeting Management**: View, cancel, and manage meetings

## Quick Start

### Inline Usage

In any Telegram chat, type:

```
@handycalbot 14:30 "Team Meeting" john@example.com
@handycalbot 10:00 25-01-2026 "Project Review"
@handycalbot 16:00 "Quick Call"
```

### Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot |
| `/connect` | Connect Google Calendar |
| `/disconnect` | Disconnect calendar |
| `/settings` | View settings |
| `/timezone` | Set timezone |
| `/duration` | Set default meeting duration |
| `/meetings` | List upcoming meetings |
| `/cancel` | Cancel a meeting |
| `/help` | Show help |

## Development Setup

### Prerequisites

- Python 3.12+
- Docker & Docker Compose
- A Telegram Bot Token (from @BotFather)
- Google Cloud Project with Calendar API enabled

### Local Development

```bash
# Clone the repository
git clone <repo-url>
cd calendarbot

# Run setup script
./scripts/setup_dev.sh

# Or manually:
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

# Copy and configure environment
cp .env.example .env
# Edit .env with your credentials

# Start database
docker compose -f docker-compose.dev.yml up -d db

# Run the bot
python -m calendarbot.main
```

### Running Tests

```bash
pytest tests/ -v
pytest tests/ -v --cov=src/calendarbot
```

## Production Deployment

### VPS Setup (DigitalOcean)

1. **Add SSH key to your droplet**

   Public key to add:
   ```
   ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGIKcx9QcC4JV1MEBefyvyndQwx1xQlI9zYE+kBaen/1 calendarbot-deploy
   ```

2. **SSH into server and run setup**
   ```bash
   # Use SSH key to avoid password prompts
   ssh -i ~/.ssh/calendarbot_deploy root@164.92.157.14

   # Or add to ~/.ssh/config for easier access:
   # Host handycal
   #   HostName 164.92.157.14
   #   User root
   #   IdentityFile ~/.ssh/calendarbot_deploy
   # Then just: ssh handycal
   ```

3. **Clone and configure**
   ```bash
   cd /opt/handycal
   git clone <repo-url> .
   cp .env.example .env
   nano .env  # Configure all variables
   ```

4. **Get SSL certificate**
   ```bash
   certbot certonly --standalone -d handycal.dzhurinskiy.com
   cp /etc/letsencrypt/live/handycal.dzhurinskiy.com/* /opt/handycal/ssl/
   ```

5. **Start services**
   ```bash
   docker compose up -d
   ```

### GitHub Secrets

Add these secrets to your GitHub repository:

| Secret | Description |
|--------|-------------|
| `VPS_HOST` | `164.92.157.14` |
| `VPS_USER` | `root` |
| `VPS_SSH_KEY` | Contents of `.ssh/calendarbot_deploy` (private key) |

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather | Yes |
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | Yes |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret | Yes |
| `GOOGLE_REDIRECT_URI` | OAuth callback URL | Yes |
| `ENCRYPTION_KEY` | Fernet key for token encryption | Yes |
| `APP_ENV` | `development` or `production` | No |
| `WEBHOOK_URL` | Telegram webhook URL (production) | Prod only |
| `DEFAULT_MEETING_DURATION` | Default duration in minutes | No (default: 60) |

### Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable **Google Calendar API**
4. Create OAuth 2.0 credentials (Web application)
5. Add redirect URI: `https://handycal.dzhurinskiy.com/oauth/google/callback`
6. Download credentials and add to `.env`

## Architecture

```
┌─────────────────┐     ┌─────────────────┐
│   Telegram      │     │  Google         │
│   Cloud         │     │  Calendar API   │
└────────┬────────┘     └────────┬────────┘
         │                       │
         ▼                       ▼
┌─────────────────────────────────────────┐
│              VPS (Docker)                │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │  Nginx  │──│   Bot   │──│  OAuth  │  │
│  │  (SSL)  │  │ Service │  │  Flow   │  │
│  └─────────┘  └────┬────┘  └─────────┘  │
│                    │                     │
│              ┌─────┴─────┐               │
│              │ PostgreSQL│               │
│              └───────────┘               │
└─────────────────────────────────────────┘
```

## License

MIT
