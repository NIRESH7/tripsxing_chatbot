@echo off
REM This script must be run from the project root (C:\tripsxing_chatbot)
cd /d %~dp0
echo Current directory: %CD%
echo.
echo Starting TripsXing Backend Server...
echo.
python -m uvicorn backend.main:app --reload --port 8000
pause

