# Windows Setup Guide for Director

This guide provides step-by-step instructions to set up and run the Director application on Windows.

## Prerequisites

Before you begin, ensure you have the following installed on your Windows system:

### 1. **Node.js 22.8.0+**
- Download from: https://nodejs.org/
- Recommended: Download the LTS (Long Term Support) version or specifically v22.8.0+
- During installation, make sure to check "Add to PATH"
- Verify installation by opening PowerShell or Command Prompt and running:
  ```
  node --version
  npm --version
  ```

### 2. **Python 3.9+**
- Download from: https://www.python.org/
- **Important**: During installation, check the box "Add Python to PATH"
- Verify installation by opening PowerShell or Command Prompt and running:
  ```
  python --version
  ```

### 3. **Git** (Optional but recommended)
- Download from: https://git-scm.com/
- This allows you to clone the repository

## Installation Steps

### Step 1: Clone or Download the Repository

**Using Git:**
```bash
git clone https://github.com/Gokul2580/dir.git
cd dir
```

**Or manually download** and extract the ZIP file.

### Step 2: Run the Setup Script

1. Navigate to the project directory in File Explorer
2. Right-click and select "Open PowerShell window here" or "Open Command Prompt window here"
3. Run the setup script:
   ```
   setup.bat
   ```

The setup script will:
- Check for Node.js and Python installations
- Create a Python virtual environment
- Install all Python dependencies
- Install all Node.js dependencies
- Create `.env` files with default configuration
- Initialize the SQLite database

### Step 3: Configure Environment Variables

After setup, you need to add your API keys:

1. Open `backend\.env` with a text editor (Notepad, VS Code, etc.)
2. Add your API keys:
   ```
   VIDEO_DB_API_KEY=your_videodb_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   ```

3. Save the file

**Where to get these keys:**
- **VIDEO_DB_API_KEY**: https://console.videodb.io/
- **OPENAI_API_KEY**: https://platform.openai.com/api-keys
- **ELEVENLABS_API_KEY**: https://elevenlabs.io/ (optional, for voice)

### Step 4: Start the Application

You have several options to run the application:

#### Option A: Start Everything at Once (Recommended)
```
run.bat
```
This opens two new command windows - one for the backend and one for the frontend.

#### Option B: Start Backend Only
```
run-be.bat
```
Backend runs on http://127.0.0.1:8000

#### Option C: Start Frontend Only
```
run-fe.bat
```
Frontend runs on http://127.0.0.1:8080

#### Option D: Development Mode
```
dev.bat
```
Starts both services with auto-reload enabled for faster development.

### Step 5: Access the Application

Once both services are running, open your web browser and go to:
```
http://127.0.0.1:8080
```

## Available Commands

All scripts are located in the root directory:

| Command | Purpose |
|---------|---------|
| `setup.bat` | Initial setup and dependency installation |
| `run.bat` | Start both backend and frontend |
| `run-be.bat` | Start backend only |
| `run-fe.bat` | Start frontend only |
| `dev.bat` | Start in development mode with hot-reload |

## Troubleshooting

### Issue: "Node.js is not installed or not in PATH"

**Solution:**
1. Restart your computer after installing Node.js
2. Or add Node.js to PATH manually:
   - Open System Properties → Environment Variables
   - Edit the PATH variable and ensure Node.js installation directory is included
   - Typically: `C:\Program Files\nodejs\`

### Issue: "Python is not installed or not in PATH"

**Solution:**
1. During Python reinstallation, make sure to check "Add Python to PATH"
2. Or add it manually:
   - Open System Properties → Environment Variables
   - Edit the PATH variable and add your Python installation directory
   - Typically: `C:\Users\{Username}\AppData\Local\Programs\Python\Python39\`

### Issue: "Access is denied" when running scripts

**Solution:**
1. Disable execution policy temporarily for this session:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
   ```
2. Then run the script

### Issue: Port 8000 or 8080 already in use

**Solution:**
1. Find the process using the port:
   ```
   netstat -ano | findstr :8000
   ```
2. Kill the process:
   ```
   taskkill /PID <PID_NUMBER> /F
   ```
3. Or change the port in `.env` files and restart

### Issue: Database initialization fails

**Solution:**
1. Delete the `instance/` folder if it exists
2. Run `setup.bat` again
3. Or manually initialize:
   ```
   cd backend
   call venv\Scripts\activate.bat
   python -m director.entrypoint.database init-sqlite
   ```

### Issue: Frontend doesn't load / shows "connection refused"

**Solution:**
1. Verify backend is running: http://127.0.0.1:8000
2. Check if VITE_APP_BACKEND_URL in `frontend\.env` matches your backend URL
3. Clear browser cache (Ctrl+Shift+Delete)
4. Restart both services

## Development Workflow

### Running with Auto-Reload

For faster development, use the development mode:
```
dev.bat
```

Changes to backend Python files will auto-reload (if Flask is in debug mode).
Changes to frontend Vue files will hot-reload automatically via Vite.

### Debugging Backend

Set breakpoints in VS Code:
1. Install Python extension in VS Code
2. Create `.vscode/launch.json`:
   ```json
   {
     "version": "0.2.0",
     "configurations": [
       {
         "name": "Python: Backend",
         "type": "python",
         "request": "launch",
         "module": "director.entrypoint.app",
         "jinja": true,
         "cwd": "${workspaceFolder}/backend"
       }
     ]
   }
   ```

### Debugging Frontend

1. Open http://127.0.0.1:8080 in your browser
2. Press F12 to open DevTools
3. Use Vue DevTools extension for better debugging

## Next Steps

Once the application is running:

1. **Explore the UI**: Familiarize yourself with the interface
2. **Test Features**: Try uploading videos and generating content
3. **Read Documentation**: Check the docs folder for more detailed guides
4. **Voice Chat**: To enable voice chat, follow the Voice Chat Setup Guide

## Production Deployment

To deploy to production:

1. Review `DEPLOYMENT.md` in the project root
2. Build the frontend:
   ```
   cd frontend
   npm run build
   ```
3. Deploy using Docker or your preferred platform

## Getting Help

- Check `DEPLOYMENT.md` for production deployment steps
- Review backend logs in `logs/` directory if enabled
- Open an issue on GitHub for bugs
- Check existing documentation in the `docs/` folder

## Security Notes

1. Never commit `.env` files with real API keys
2. Use environment variables for secrets in production
3. Keep your API keys secure and rotate them regularly
4. Review `backend/.env` regularly and update as needed

---

**Happy developing with Director on Windows!** 🚀
