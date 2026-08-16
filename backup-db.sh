#!/bin/bash
# Backup PostgreSQL database
# Usage: ./backup-db.sh [output_dir] [database_name|all]

DB_USER="postgres"
CONTAINER="shared-postgres"
OUTPUT_DIR="${1:-./backups}"
TARGET="${2:-agentrunnerv2}"

# List of databases to backup when using "all"
DATABASES="agentrunnerv2 agentrunner ukbe pa personal-assistant"

# Create backup directory
mkdir -p "$OUTPUT_DIR"

# Generate timestamp
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

if [ "$TARGET" = "all" ]; then
    echo "Backing up all databases..."
    for DB in $DATABASES; do
        BACKUP_FILE="$OUTPUT_DIR/${DB}-${TIMESTAMP}.sql"
        echo "  Backing up '$DB'..."
        docker exec -t "$CONTAINER" pg_dump -U "$DB_USER" -d "$DB" --clean --if-exists > "$BACKUP_FILE"
        if [ $? -eq 0 ]; then
            echo "  Done: $DB"
        else
            echo "  Failed: $DB"
        fi
    done
    echo "All databases backed up to $OUTPUT_DIR"
else
    BACKUP_FILE="$OUTPUT_DIR/${TARGET}-${TIMESTAMP}.sql"
    echo "Backing up database '$TARGET' to $BACKUP_FILE..."
    docker exec -t "$CONTAINER" pg_dump -U "$DB_USER" -d "$TARGET" --clean --if-exists > "$BACKUP_FILE"
    if [ $? -eq 0 ]; then
        echo "Backup completed: $BACKUP_FILE"
        echo "Size: $(du -h "$BACKUP_FILE" | cut -f1)"
    else
        echo "Backup failed!"
        exit 1
    fi
fi

# Keep only last 10 backups per database
for DB in $DATABASES; do
    ls -t "$OUTPUT_DIR"/${DB}-*.sql 2>/dev/null | tail -n +11 | xargs -r rm --
done
echo "Old backups cleaned (keeping last 10 per database)"
