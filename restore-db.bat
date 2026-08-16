@echo off
REM Restore PostgreSQL database from backup (Windows)
REM Usage: restore-db.bat <backup_file>

if "%1"=="" (
    echo Usage: %0 ^<backup_file^>
    echo Available backups:
    dir /b .\backups\*.sql 2>nul || echo   No backups found in .\backups\
    exit /b 1
)

set BACKUP_FILE=%1
set DB_NAME=agentrunnerv2
set DB_USER=postgres

if not exist "%BACKUP_FILE%" (
    echo Error: File not found: %BACKUP_FILE%
    exit /b 1
)

echo WARNING: This will overwrite the current database!
echo Backup file: %BACKUP_FILE%
echo Target database: %DB_NAME%
set /p confirm=Continue? (yes/no): 

if /i not "%confirm%"=="yes" (
    echo Aborted.
    exit /b 0
)

echo Restoring database...

REM Restore database
docker exec -i postgres psql -U %DB_USER% -d %DB_NAME% < "%BACKUP_FILE%"

if %ERRORLEVEL% EQU 0 (
    echo Restore completed successfully!
) else (
    echo Restore failed!
    exit /b 1
)
