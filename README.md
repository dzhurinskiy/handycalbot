# HandyCalBot

A Telegram bot for scheduling Google Calendar meetings directly from any chat.

## Features

- **Inline Meeting Creation**: Schedule meetings from any Telegram chat
- **Google Calendar Integration**: Syncs with your Google Calendar
- **Zoom Integration**: Automatically add Zoom meeting links
- **Attendee Invitations**: Automatically sends calendar invites
- **Timezone Support**: Respects user timezone settings
- **Meeting Reminders**: Get notified before your meetings
- **Multi-language**: Supports 10 languages
- **Privacy Mode**: Option for minimal calendar access

## Quick Start

### Inline Usage

In any Telegram chat, type:

```
@yourbotname 14:30 "Team Meeting" john@example.com
@yourbotname 10:00 25-01-2026 "Project Review"
@yourbotname 16:00 "Quick Call"
```

### Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot |
| `/connect` | Connect Google Calendar |
| `/connectzoom` | Connect Zoom for meeting links |
| `/disconnect` | Disconnect calendar |
| `/disconnectzoom` | Disconnect Zoom |
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
- (Optional) Zoom App for meeting links

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/calendarbot.git
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

### VPS Setup

1. **Provision a VPS** (e.g., DigitalOcean, Linode, Hetzner)
   - Ubuntu 22.04+ recommended
   - 1GB RAM minimum
   - Docker pre-installed or install manually

2. **Configure SSH access**
   ```bash
   # Generate a deploy key (on your local machine)
   ssh-keygen -t ed25519 -C "calendarbot-deploy" -f ~/.ssh/calendarbot_deploy

   # Add the PUBLIC key to your VPS ~/.ssh/authorized_keys

   # Add to ~/.ssh/config for easier access:
   # Host calendarbot
   #   HostName YOUR_VPS_IP
   #   User root
   #   IdentityFile ~/.ssh/calendarbot_deploy
   ```

3. **Clone and configure on VPS**
   ```bash
   mkdir -p /opt/calendarbot
   cd /opt/calendarbot
   git clone https://github.com/yourusername/calendarbot.git .
   cp .env.example .env
   nano .env  # Configure all variables
   ```

4. **Get SSL certificate**
   ```bash
   # Install certbot if not installed
   apt install certbot

   # Get certificate for your domain
   certbot certonly --standalone -d your-domain.com

   # Copy certificates
   mkdir -p /opt/calendarbot/ssl
   cp /etc/letsencrypt/live/your-domain.com/fullchain.pem /opt/calendarbot/ssl/
   cp /etc/letsencrypt/live/your-domain.com/privkey.pem /opt/calendarbot/ssl/
   ```

5. **Start services**
   ```bash
   docker compose up -d
   ```

### GitHub Actions CI/CD

The repository includes GitHub Actions workflows for automated deployment.

#### Required Secrets

Add these secrets to your GitHub repository settings:

| Secret | Description |
|--------|-------------|
| `VPS_HOST` | Your VPS IP address |
| `VPS_USER` | SSH user (e.g., `root`) |
| `VPS_SSH_KEY` | Private SSH key for deployment |
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather |
| `DATABASE_URL` | PostgreSQL connection string |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret |
| `GOOGLE_REDIRECT_URI` | OAuth callback URL |
| `ENCRYPTION_KEY` | Fernet key for token encryption |
| `WEBHOOK_URL` | Telegram webhook URL |

#### Optional Secrets (for Zoom integration)

| Secret | Description |
|--------|-------------|
| `ZOOM_CLIENT_ID` | Zoom OAuth client ID |
| `ZOOM_CLIENT_SECRET` | Zoom OAuth client secret |
| `ZOOM_REDIRECT_URI` | Zoom OAuth callback URL |

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
| `DEFAULT_MEETING_DURATION` | Default duration in minutes | No (60) |
| `ZOOM_CLIENT_ID` | Zoom OAuth client ID | No |
| `ZOOM_CLIENT_SECRET` | Zoom OAuth client secret | No |
| `ZOOM_REDIRECT_URI` | Zoom OAuth callback URL | No |

### Generate Encryption Key

```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

### Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable **Google Calendar API**
4. Go to **APIs & Services** > **Credentials**
5. Create **OAuth 2.0 Client ID** (Web application type)
6. Add authorized redirect URI: `https://your-domain.com/oauth/google/callback`
7. Copy Client ID and Client Secret to your `.env`

### Zoom App Setup (Optional)

1. Go to [Zoom App Marketplace](https://marketplace.zoom.us/develop/create)
2. Create a new **OAuth** app
3. Add scopes: `meeting:write`, `user:read`
4. Add redirect URL: `https://your-domain.com/oauth/zoom/callback`
5. Copy Client ID and Client Secret to your `.env`

### Telegram Bot Setup

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot`
3. Enable inline mode with `/setinline`
4. Copy the bot token to your `.env`

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Telegram      │     │  Google         │     │     Zoom        │
│   Cloud         │     │  Calendar API   │     │     API         │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                        VPS (Docker)                              │
│  ┌─────────┐  ┌─────────────────────────────┐  ┌─────────────┐  │
│  │  Nginx  │──│     CalendarBot Service     │──│   OAuth     │  │
│  │  (SSL)  │  │  (FastAPI + Telegram Bot)   │  │   Flows     │  │
│  └─────────┘  └──────────────┬──────────────┘  └─────────────┘  │
│                              │                                   │
│                        ┌─────┴─────┐                            │
│                        │ PostgreSQL│                            │
│                        └───────────┘                            │
└─────────────────────────────────────────────────────────────────┘
```

## Security

- OAuth tokens are encrypted at rest using Fernet (AES-256)
- HTTPS/TLS required for production
- No passwords stored - OAuth-only authentication
- Privacy mode option for minimal calendar access

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) file for details.
