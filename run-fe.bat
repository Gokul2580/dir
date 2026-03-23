@echo off
REM Director - Start Frontend Only
REM This script starts only the frontend development server

setlocal enabledelayedexpansion

echo.
echo ================================================
echo   Director - Starting Frontend
echo ================================================
echo.

cd frontend

REM Check if node_modules exists
if not exist node_modules (
    echo Error: Dependencies not installed. Run setup.bat first.
    pause
    exit /b 1
)

REM Start frontend
echo Starting frontend development server on http://127.0.0.1:8080
echo Press Ctrl+C to stop.
echo.

npm run dev

pause
