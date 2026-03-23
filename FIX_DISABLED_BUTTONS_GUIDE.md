## Why All Buttons Are Disabled - Complete Fix

### Root Cause
The UI buttons are disabled because the frontend is waiting for the backend to respond with a successful health check. This typically happens when:

1. Backend isn't running
2. Backend has initialization errors
3. Database connection failed
4. API keys are missing
5. Vite dev server cache is stale

---

## Step-by-Step Fix

### Step 1: Clear Everything and Fresh Start

#### On Windows - Command Prompt (Run as Administrator):
```batch
REM Kill any running processes
taskkill /F /IM node.exe
taskkill /F /IM python.exe

REM Clear npm cache
npm cache clean --force

REM Clear vite cache
cd frontend
rmdir /s /q node_modules\.vite
cd ..
```

#### On Mac/Linux:
```bash
# Kill processes
pkill -f "node" || true
pkill -f "python" || true

# Clear caches
rm -rf frontend/node_modules/.vite
npm cache clean --force
```

---

### Step 2: Create .env File

**Create file: `backend/.env`**

```
# API Keys (you can add dummy values for now to test)
VIDEO_DB_API_KEY=test_key
OPENAI_API_KEY=sk-test-key
ELEVENLABS_API_KEY=test_key

# Server Configuration
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
FRONTEND_URL=http://127.0.0.1:8080

# Database (SQLite for local testing - NO setup required)
DATABASE_URL=sqlite:///./app.db
DB_TYPE=sqlite

# Security
SECRET_KEY=your-temporary-secret-key-change-this-in-production

# CORS
CORS_ORIGINS=http://127.0.0.1:8080

# Voice
VOICE_QUALITY=high
MAX_AUDIO_SIZE=52428800
```

**Save this file and DO NOT modify after creation until you understand each value.**

---

### Step 3: Install Dependencies (Clean Install)

#### Backend:
```batch
cd backend
pip install -r requirements.txt
```

#### Frontend:
```batch
cd frontend
npm install
```

---

### Step 4: Start Backend (New Terminal)

```batch
cd backend
python -m director.entrypoint.api.server
```

**You should see:**
```
* Running on http://127.0.0.1:8000
* Press CTRL+C to quit
```

**If you see errors:**
- Check `.env` file exists in `backend/` folder
- Check DATABASE_URL line doesn't have quotes
- Restart and look at the error message

---

### Step 5: Start Frontend (Another Terminal)

```batch
cd frontend
npm run dev
```

**You should see:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://127.0.0.1:8080/
```

---

### Step 6: Test in Browser

1. Open: `http://127.0.0.1:8080`
2. Wait 3-5 seconds for initial load
3. Press F12 to open Developer Console
4. Look for any red errors
5. Buttons should now be **enabled** (not grayed out)

---

## If Buttons STILL Disabled

### Check 1: Backend Connection
```
Open browser console (F12)
Look for errors like:
- "Failed to fetch from backend"
- "Connection refused"
- "CORS error"
```

**If you see CORS error:**
- Restart backend
- Check FRONTEND_URL in .env matches your actual URL

### Check 2: Backend Initialization
1. Look at backend terminal
2. Do you see any red text errors?
3. Common issues:
   - `ModuleNotFoundError` - Run `pip install -r requirements.txt`
   - `[Errno 111] Connection refused` - Database issue, restart
   - `Address already in use` - Port 8000 is taken, change BACKEND_PORT

### Check 3: .env File Location
- .env MUST be in `backend/.env`
- NOT in root or frontend folder
- File must be named exactly `.env` (with the dot)

### Check 4: Cache Issues
```batch
REM Windows
cd frontend
rmdir /s /q node_modules\.vite

REM Mac/Linux
rm -rf frontend/node_modules/.vite
```

Then restart frontend: `npm run dev`

---

## Verify Backend is Working

Open new terminal and test:

```batch
curl http://127.0.0.1:8000/config/check
```

**Should return JSON with no errors.**

Or open in browser:
```
http://127.0.0.1:8000/config/check
```

---

## What Each Button Needs

| Button | Requires |
|--------|----------|
| New Chat | Backend running + database |
| Collections | Backend + database setup |
| Explore Agents | Backend + API connection |
| Chats | Database initialized |

All are disabled until the backend responds successfully to the health check.

---

## Next Steps After Buttons Are Enabled

1. Get real API keys:
   - OPENAI_API_KEY from https://platform.openai.com
   - VIDEO_DB_API_KEY from https://app.videodb.io
   - Update .env and restart backend

2. Test voice features at `/voice` route

3. Review `DATABASE_CONFIG_GUIDE.md` for production setup

---

## Emergency Reset

If nothing works, complete reset:

```batch
REM Windows
taskkill /F /IM node.exe 2>nul
taskkill /F /IM python.exe 2>nul

cd frontend
rmdir /s /q node_modules
rmdir /s /q .vite
del package-lock.json

cd ../backend
rmdir /s /q __pycache__
del app.db

cd ..
npm install -C frontend
pip install -r backend/requirements.txt

REM Then start fresh from Step 2
```

Then restart both backend and frontend.
