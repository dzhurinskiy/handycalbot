#!/bin/bash
set -e

# CalendarBot Deployment Script
# Usage: ./deploy.sh [production|staging]

ENV=${1:-production}
PROJECT_DIR="/opt/handycal"
COMPOSE_FILE="docker-compose.yml"

echo "=== CalendarBot Deployment ==="
echo "Environment: $ENV"
echo "Project dir: $PROJECT_DIR"
echo ""

cd $PROJECT_DIR

# Pull latest changes
echo ">>> Pulling latest code..."
git fetch origin
git reset --hard origin/main

# Build and restart
echo ">>> Building containers..."
docker compose -f $COMPOSE_FILE build --no-cache app

echo ">>> Starting services..."
docker compose -f $COMPOSE_FILE up -d

# Wait for DB
echo ">>> Waiting for database..."
sleep 5

# Run migrations
echo ">>> Running database migrations..."
docker compose -f $COMPOSE_FILE exec -T app alembic upgrade head

# Health check
echo ">>> Running health check..."
sleep 5
if curl -sf http://localhost:8000/health > /dev/null; then
    echo ">>> Health check passed!"
else
    echo ">>> Health check FAILED!"
    docker compose -f $COMPOSE_FILE logs app --tail 50
    exit 1
fi

# Cleanup
echo ">>> Cleaning up old images..."
docker image prune -f

echo ""
echo "=== Deployment Complete ==="
docker compose -f $COMPOSE_FILE ps
