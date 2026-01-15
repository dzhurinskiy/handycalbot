#!/bin/bash
set -e

# Development Setup Script
# Usage: ./setup_dev.sh

echo "=== CalendarBot Development Setup ==="

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
if [ "$PYTHON_VERSION" != "3.12" ] && [ "$PYTHON_VERSION" != "3.13" ]; then
    echo "Warning: Python 3.12+ recommended, found $PYTHON_VERSION"
fi

# Create virtual environment if not exists
if [ ! -d ".venv" ]; then
    echo ">>> Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Install dependencies
echo ">>> Installing dependencies..."
pip install --upgrade pip
pip install -e ".[dev]"

# Copy env file if not exists
if [ ! -f ".env" ]; then
    echo ">>> Creating .env file..."
    cp .env.example .env
    echo "Please edit .env with your configuration!"
fi

# Generate encryption key if not in .env
if ! grep -q "ENCRYPTION_KEY=" .env || grep -q "ENCRYPTION_KEY=$" .env; then
    echo ">>> Generating encryption key..."
    KEY=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
    if grep -q "ENCRYPTION_KEY=" .env; then
        sed -i "s|ENCRYPTION_KEY=.*|ENCRYPTION_KEY=$KEY|" .env
    else
        echo "ENCRYPTION_KEY=$KEY" >> .env
    fi
    echo "Encryption key generated and saved to .env"
fi

# Start development database
echo ">>> Starting development database..."
docker compose -f docker-compose.dev.yml up -d db

# Wait for DB
echo ">>> Waiting for database..."
sleep 5

# Run migrations
echo ">>> Running database migrations..."
alembic upgrade head 2>/dev/null || echo "Run 'alembic revision --autogenerate' to create initial migration"

echo ""
echo "=== Development Setup Complete ==="
echo ""
echo "To start the bot:"
echo "  source .venv/bin/activate"
echo "  python -m calendarbot.main"
echo ""
echo "Or with Docker:"
echo "  docker compose -f docker-compose.dev.yml up"
echo ""
