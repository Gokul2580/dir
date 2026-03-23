@echo off
REM Director - Development Mode
REM This script starts the application in development mode

setlocal enabledelayedexpansion

echo.
echo ================================================
echo   Director - Development Mode
echo ================================================
echo.

REM Create logs directory if it doesn't exist
if not exist logs mkdir logs

REM Start backend with auto-reload
echo Starting backend in development mode...
start "Director Backend (Dev)" cmd /k "cd backend && call venv\Scripts\activate.bat && set FLASK_ENV=development && set FLASK_DEBUG=1 && python -m director.entrypoint.app"

REM Wait for backend to start
timeout /t 3 /nobreak

REM Start frontend with hot reload
echo Starting frontend in development mode...
start "Director Frontend (Dev)" cmd /k "cd frontend && npm run dev"

echo.
echo ================================================
echo   Development Mode Started
echo ================================================
echo.
echo Backend: http://127.0.0.1:8000
echo Frontend: http://127.0.0.1:8080
echo.
echo Features enabled:
echo   - Auto-reload on code changes
echo   - Debug mode on backend
echo   - Hot Module Replacement (HMR) on frontend
echo.
echo Close the command windows to stop services.
echo ================================================
echo.

pause
