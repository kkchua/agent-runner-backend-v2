@echo off
REM Backup PostgreSQL database (Windows)
REM Usage: backup-db.bat [output_dir]

set DB_NAME=agentrunnerv2
set DB_USER=postgres
set OUTPUT_DIR=%1
if "%OUTPUT_DIR%"=="" set OUTPUT_DIR=.\backups

REM Create backup directory
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

REM Generate filename with timestamp
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set TIMESTAMP=%datetime:~0,8%-%datetime:~8,6%
set BACKUP_FILE=%OUTPUT_DIR%\%DB_NAME%-%TIMESTAMP%.sql

echo Backing up database '%DB_NAME%' to %BACKUP_FILE%...

REM Dump database
docker exec -t postgres pg_dump -U %DB_USER% -d %DB_NAME% --clean --if-exists > "%BACKUP_FILE%"

if %ERRORLEVEL% EQU 0 (
    echo Backup completed: %BACKUP_FILE%
) else (
    echo Backup failed!
    exit /b 1
)
