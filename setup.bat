@echo off
REM Director - Windows Setup Script
REM This script sets up the Director application on Windows

setlocal enabledelayedexpansion

echo.
echo ================================================
echo   Director - Windows Setup
echo ================================================
echo.

REM Color codes for output
set "SUCCESS=[OK]"
set "ERROR=[ERROR]"
set "INFO=[INFO]"

REM Check if Node.js is installed
echo %INFO% Checking for Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo %ERROR% Node.js is not installed or not in PATH
    echo Please install Node.js 22.8.0 from https://nodejs.org/
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('node --version') do (
        echo %SUCCESS% Node.js is installed: %%i
    )
)

REM Check if Python 3.9+ is installed
echo.
echo %INFO% Checking for Python 3.9+...
python --version >nul 2>&1
if errorlevel 1 (
    echo %ERROR% Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('python --version') do (
        echo %SUCCESS% Python is installed: %%i
    )
)

REM Create backend virtual environment
echo.
echo %INFO% Setting up Python virtual environment...
cd backend
if not exist venv (
    python -m venv venv
    echo %SUCCESS% Virtual environment created
) else (
    echo %SUCCESS% Virtual environment already exists
)

REM Activate virtual environment and install dependencies
echo.
echo %INFO% Installing backend dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo.
    echo %INFO% Creating .env file...
    (
        echo # Backend Configuration
        echo VIDEO_DB_API_KEY=
        echo OPENAI_API_KEY=
        echo ELEVENLABS_API_KEY=
        echo.
        echo # Server Configuration
        echo BACKEND_HOST=127.0.0.1
        echo BACKEND_PORT=8000
        echo FRONTEND_URL=http://127.0.0.1:8080
        echo.
        echo # Database Configuration
        echo DATABASE_URL=
        echo DB_TYPE=sqlite
        echo.
        echo # Security Configuration
        echo SECRET_KEY=your-secret-key-here
        echo CORS_ORIGINS=http://127.0.0.1:8080
        echo.
        echo # Voice Configuration
        echo VOICE_QUALITY=high
        echo MAX_AUDIO_SIZE=52428800
    ) > .env
    echo %SUCCESS% .env file created. Please update it with your API keys.
) else (
    echo %SUCCESS% .env file already exists
)

REM Initialize database
echo.
echo %INFO% Initializing SQLite database...
python -m director.entrypoint.database init-sqlite
if errorlevel 1 (
    echo %ERROR% Database initialization failed
    pause
    exit /b 1
) else (
    echo %SUCCESS% Database initialized
)

cd ..

REM Frontend setup
echo.
echo %INFO% Setting up frontend dependencies...
cd frontend

if not exist .env (
    echo.
    echo %INFO% Creating frontend .env file...
    (
        echo VITE_APP_BACKEND_URL=http://127.0.0.1:8000
        echo VITE_PORT=8080
        echo VITE_OPEN_BROWSER=true
    ) > .env
    echo %SUCCESS% Frontend .env file created
) else (
    echo %SUCCESS% Frontend .env file already exists
)

echo %INFO% Installing frontend dependencies...
call npm install
if errorlevel 1 (
    echo %ERROR% Frontend dependency installation failed
    pause
    exit /b 1
) else (
    echo %SUCCESS% Frontend dependencies installed
)

cd ..

echo.
echo ================================================
echo   Setup Completed Successfully!
echo ================================================
echo.
echo IMPORTANT: Next Steps:
echo.
echo 1. Review and Update Environment Variables:
echo    - Edit backend\.env and add your API keys
echo    - VIDEO_DB_API_KEY (from https://console.videodb.io/)
echo    - OPENAI_API_KEY (for voice transcription)
echo    - ELEVENLABS_API_KEY (for text-to-speech, optional)
echo.
echo 2. Start the Application:
echo    - Run: run.bat (starts both backend and frontend)
echo    - Or separately: run-be.bat and run-fe.bat
echo.
echo 3. Access the Application:
echo    - Frontend: http://127.0.0.1:8080
echo    - Backend API: http://127.0.0.1:8000
echo.
echo ================================================
echo.

pause
