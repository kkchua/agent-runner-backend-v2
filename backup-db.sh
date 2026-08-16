#!/bin/bash
# Backup PostgreSQL database
# Usage: ./backup-db.sh [output_dir]

DB_NAME="agentrunnerv2"
DB_USER="postgres"
DB_HOST="localhost"
DB_PORT="5432"
OUTPUT_DIR="${1:-./backups}"

# Create backup directory
mkdir -p "$OUTPUT_DIR"

# Generate filename with timestamp
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_FILE="$OUTPUT_DIR/${DB_NAME}-${TIMESTAMP}.sql"

echo "Backing up database '$DB_NAME' to $BACKUP_FILE..."

# Dump database (plain SQL format)
docker exec -t postgres pg_dump -U "$DB_USER" -d "$DB_NAME" --clean --if-exists > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "Backup completed: $BACKUP_FILE"
    echo "Size: $(du -h "$BACKUP_FILE" | cut -f1)"
else
    echo "Backup failed!"
    exit 1
fi

# Keep only last 10 backups
ls -t "$OUTPUT_DIR"/*.sql 2>/dev/null | tail -n +11 | xargs -r rm --
echo "Old backups cleaned (keeping last 10)"
