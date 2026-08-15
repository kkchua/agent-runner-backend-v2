@echo off
setlocal enabledelayedexpansion

:: ============================================================
:: Daily PostgreSQL Backup Script
:: Backs up 'agentrunnerv2' from Docker container 'shared-postgres'
:: ============================================================

:: Configuration
set BACKUP_DIR=D:\MyProjectSpace\01_Workflows\agent-runner-backend-v2\backups
set DB_NAME=agentrunnerv2
set DB_USER=postgres
set CONTAINER_NAME=shared-postgres
set RETENTION_DAYS=14

:: Create backup directory if it doesn't exist
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

:: Generate timestamp (YYYYMMDD_HHMMSS)
for /f "tokens=1-3 delims=/- " %%a in ('echo %date%') do set DATESTR=%%c%%b%%a
for /f "tokens=1-3 delims=:. " %%a in ('echo %time%') do set TIMESTR=00%%a%%b%%c
set TIMESTR=%TIMESTR:~-6%
set TIMESTAMP=%DATESTR%_%TIMESTR%

:: Define backup file
set BACKUP_FILE=%BACKUP_DIR%\%DB_NAME%_%TIMESTAMP%.sql

:: Run pg_dump via docker
echo [INFO] Starting backup of '%DB_NAME%'..."
docker exec %CONTAINER_NAME% pg_dump -U %DB_USER% %DB_NAME% > "%BACKUP_FILE%"

if %errorlevel% equ 0 (
    echo [SUCCESS] Backup created: %BACKUP_FILE%
) else (
    echo [ERROR] Backup failed with exit code %errorlevel%
    exit /b %errorlevel%
)

:: Cleanup backups older than RETENTION_DAYS (PowerShell fallback for Windows)
echo [INFO] Cleaning up backups older than %RETENTION_DAYS% days...
powershell -Command "Get-ChildItem '%BACKUP_DIR%\*.sql' | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-%RETENTION_DAYS%) } | Remove-Item -Force"

echo [INFO] Backup routine completed.
