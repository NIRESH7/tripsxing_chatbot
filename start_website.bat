@echo off
echo Starting TripsXing Chatbot...

cd /d %~dp0

echo Starting Backend (FastAPI with PostgreSQL)...
start "TripsXing Backend" cmd /k "python -m uvicorn backend.main:app --reload --port 8000"

echo Starting Frontend (React)...
start "TripsXing Frontend" cmd /k "cd frontend && npm run dev"

echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Press any key to exit this launcher (servers will keep running in new windows).
pause
