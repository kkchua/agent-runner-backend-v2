@echo off
REM Backup PostgreSQL database (Windows)
REM Usage: backup-db.bat [output_dir] [database_name|all]

set DB_USER=postgres
set CONTAINER=shared-postgres
set OUTPUT_DIR=%1
if "%OUTPUT_DIR%"=="" set OUTPUT_DIR=.\backups
set TARGET=%2
if "%TARGET%"=="" set TARGET=agentrunnerv2

REM List of databases to backup when using "all"
set DATABASES=agentrunnerv2 agentrunner ukbe pa personal-assistant

REM Create backup directory
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

REM Generate timestamp
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set TIMESTAMP=%datetime:~0,8%-%datetime:~8,6%

if /i "%TARGET%"=="all" (
    echo Backing up all databases...
    setlocal enabledelayedexpansion
    for %%D in (%DATABASES%) do (
        echo   Backing up '%%D'...
        docker exec -t %CONTAINER% pg_dump -U %DB_USER% -d "%%D" --clean --if-exists > "%OUTPUT_DIR%\%%D-%TIMESTAMP%.sql"
        if !ERRORLEVEL! EQU 0 (
            echo   Done: %%D
        ) else (
            echo   Failed: %%D
        )
    )
    endlocal
    echo All databases backed up to %OUTPUT_DIR%
) else (
    set BACKUP_FILE=%OUTPUT_DIR%\%TARGET%-%TIMESTAMP%.sql
    echo Backing up database '%TARGET%' to %BACKUP_FILE%...
    docker exec -t %CONTAINER% pg_dump -U %DB_USER% -d %TARGET% --clean --if-exists > "%BACKUP_FILE%"
    if %ERRORLEVEL% EQU 0 (
        echo Backup completed: %BACKUP_FILE%
    ) else (
        echo Backup failed!
        exit /b 1
    )
)
