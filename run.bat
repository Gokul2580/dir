@echo off
REM Director - Start Both Backend and Frontend
REM This script starts both services

setlocal enabledelayedexpansion

echo.
echo ================================================
echo   Director - Starting Application
echo ================================================
echo.

REM Start backend
echo Starting backend server...
start "Director Backend" cmd /k "cd backend && call venv\Scripts\activate.bat && python -m director.entrypoint.app"

REM Wait a moment for backend to start
timeout /t 2 /nobreak

REM Start frontend
echo Starting frontend development server...
start "Director Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Backend: http://127.0.0.1:8000
echo Frontend: http://127.0.0.1:8080
echo.
echo Close these command windows to stop the services.
echo ================================================
echo.

pause
