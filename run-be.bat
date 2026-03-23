@echo off
REM Director - Start Backend Only
REM This script starts only the backend server

setlocal enabledelayedexpansion

echo.
echo ================================================
echo   Director - Starting Backend
echo ================================================
echo.

cd backend

REM Check if venv exists
if not exist venv (
    echo Error: Virtual environment not found. Run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start backend
echo Starting backend server on http://127.0.0.1:8000
echo Press Ctrl+C to stop.
echo.

python -m director.entrypoint.app

pause
