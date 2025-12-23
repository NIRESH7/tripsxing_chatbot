@echo off
echo Starting TripsXing Backend Server...
echo.
echo Make sure you're running this from the project root directory.
echo.

cd /d %~dp0

echo Starting Backend (FastAPI with PostgreSQL)...
start "TripsXing Backend" cmd /k "python -m uvicorn backend.main:app --reload --port 8000"

echo.
echo Backend server is starting...
echo Backend: http://localhost:8000
echo.
echo Press any key to exit this launcher (server will keep running in new window).
pause

