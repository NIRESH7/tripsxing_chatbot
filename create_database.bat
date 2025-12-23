@echo off
echo ========================================
echo Creating PostgreSQL Database
echo ========================================
echo.
echo This script will create the tripsxing_chatbot database
echo.

set /p DB_USER="Enter PostgreSQL username (default: postgres): "
if "%DB_USER%"=="" set DB_USER=postgres

set /p DB_HOST="Enter PostgreSQL host (default: localhost): "
if "%DB_HOST%"=="" set DB_HOST=localhost

set /p DB_PORT="Enter PostgreSQL port (default: 5432): "
if "%DB_PORT%"=="" set DB_PORT=5432

echo.
echo Creating database: tripsxing_chatbot
echo User: %DB_USER%
echo Host: %DB_HOST%
echo Port: %DB_PORT%
echo.

REM Connect to postgres database to create the new database
psql -U %DB_USER% -h %DB_HOST% -p %DB_PORT% -d postgres -c "CREATE DATABASE tripsxing_chatbot;"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Database created successfully!
    echo ========================================
    echo.
    echo You can now run the dummy data insertion script.
) else (
    echo.
    echo ========================================
    echo Error: Database might already exist or connection failed.
    echo ========================================
    echo.
    echo Trying to connect to existing database...
    psql -U %DB_USER% -h %DB_HOST% -p %DB_PORT% -d tripsxing_chatbot -c "SELECT version();"
)

pause

