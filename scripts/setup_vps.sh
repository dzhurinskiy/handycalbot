#!/bin/bash
set -e

# VPS Initial Setup Script
# Run this on a fresh DigitalOcean droplet
# Usage: curl -sSL <raw-url> | bash

echo "=== CalendarBot VPS Setup ==="

# Update system
echo ">>> Updating system packages..."
apt-get update && apt-get upgrade -y

# Install Docker
echo ">>> Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker
    systemctl start docker
fi

# Install Docker Compose
echo ">>> Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    apt-get install -y docker-compose-plugin
fi

# Install other tools
echo ">>> Installing utilities..."
apt-get install -y git curl nginx certbot python3-certbot-nginx

# Create project directory
echo ">>> Setting up project directory..."
mkdir -p /opt/handycal
cd /opt/handycal

# Clone repository (if not exists)
if [ ! -d ".git" ]; then
    echo ">>> Please clone your repository manually:"
    echo "    git clone <your-repo-url> /opt/handycal"
fi

# Create SSL directory
mkdir -p /opt/handycal/ssl

# Setup firewall
echo ">>> Configuring firewall..."
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# Create backup cron job
echo ">>> Setting up backup cron job..."
(crontab -l 2>/dev/null; echo "0 3 * * * /opt/handycal/scripts/backup_db.sh >> /var/log/handycal-backup.log 2>&1") | crontab -

echo ""
echo "=== VPS Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Clone your repository: git clone <repo-url> /opt/handycal"
echo "2. Create .env file: cp .env.example .env && nano .env"
echo "3. Get SSL certificate: certbot certonly --standalone -d your-domain.com"
echo "4. Copy SSL certs: cp /etc/letsencrypt/live/domain/* /opt/handycal/ssl/"
echo "5. Start services: docker compose up -d"
echo ""
