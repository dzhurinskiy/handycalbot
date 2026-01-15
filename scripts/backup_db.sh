#!/bin/bash
set -e

# Database Backup Script
# Usage: ./backup_db.sh

BACKUP_DIR="/opt/handycal/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/calendarbot_$TIMESTAMP.sql"

# Create backup directory if not exists
mkdir -p $BACKUP_DIR

echo "=== CalendarBot Database Backup ==="
echo "Backup file: $BACKUP_FILE"

# Create backup
docker compose exec -T db pg_dump -U calendarbot calendarbot > $BACKUP_FILE

# Compress
gzip $BACKUP_FILE
echo "Backup created: ${BACKUP_FILE}.gz"

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete
echo "Old backups cleaned up"

# Show backup size
ls -lh ${BACKUP_FILE}.gz

echo "=== Backup Complete ==="
