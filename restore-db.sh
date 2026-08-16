#!/bin/bash
# Restore PostgreSQL database from backup
# Usage: ./restore-db.sh <backup_file>

if [ -z "$1" ]; then
    echo "Usage: $0 <backup_file>"
    echo "Available backups:"
    ls -la ./backups/*.sql 2>/dev/null || echo "  No backups found in ./backups/"
    exit 1
fi

BACKUP_FILE="$1"
DB_NAME="agentrunnerv2"
DB_USER="postgres"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: File not found: $BACKUP_FILE"
    exit 1
fi

echo "WARNING: This will overwrite the current database!"
echo "Backup file: $BACKUP_FILE"
echo "Target database: $DB_NAME"
read -p "Continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 0
fi

echo "Restoring database..."

# Restore database
docker exec -i shared-postgres psql -U "$DB_USER" -d "$DB_NAME" < "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "Restore completed successfully!"
else
    echo "Restore failed!"
    exit 1
fi
