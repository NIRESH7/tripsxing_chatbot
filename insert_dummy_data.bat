@echo off
echo ========================================
echo TripsXing Database Data Insertion Script
echo ========================================
echo.
echo This script will insert dummy data into your PostgreSQL database: tripsxing_chatbot
echo.
echo Make sure PostgreSQL is running and you have the correct credentials.
echo.

set /p DB_USER="Enter PostgreSQL username (default: postgres): "
if "%DB_USER%"=="" set DB_USER=postgres

set /p DB_HOST="Enter PostgreSQL host (default: localhost): "
if "%DB_HOST%"=="" set DB_HOST=localhost

set /p DB_PORT="Enter PostgreSQL port (default: 5432): "
if "%DB_PORT%"=="" set DB_PORT=5432

echo.
echo Connecting to database: tripsxing_chatbot
echo User: %DB_USER%
echo Host: %DB_HOST%
echo Port: %DB_PORT%
echo.

psql -U %DB_USER% -h %DB_HOST% -p %DB_PORT% -d tripsxing_chatbot -f tripsxing_dummy_data.sql

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Data insertion completed successfully!
    echo ========================================
) else (
    echo.
    echo ========================================
    echo Error occurred during data insertion.
    echo Please check your PostgreSQL connection and try again.
    echo ========================================
)

pause

