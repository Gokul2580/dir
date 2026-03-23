## MASTER TROUBLESHOOTING & SETUP GUIDE

### Your Current Issue
**Problem:** All buttons are disabled after running the app  
**Reason:** Backend not fully initialized (missing .env file or API key issues)  
**Solution:** 5-10 minute fix below

---

## QUICK FIX (Do This First)

### 1. Create Backend Configuration File

**Create file:** `backend/.env` (in the backend folder, NOT root or frontend)

**Copy-paste this exactly:**
```
VIDEO_DB_API_KEY=test
OPENAI_API_KEY=test
ELEVENLABS_API_KEY=test
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
FRONTEND_URL=http://127.0.0.1:8080
DATABASE_URL=sqlite:///./app.db
DB_TYPE=sqlite
SECRET_KEY=test-secret-key-123
CORS_ORIGINS=http://127.0.0.1:8080
VOICE_QUALITY=high
MAX_AUDIO_SIZE=52428800
```

### 2. Restart Everything

**Kill old processes:**
```batch
taskkill /F /IM node.exe
taskkill /F /IM python.exe
```

**Start backend (Terminal 1):**
```batch
cd backend
python -m director.entrypoint.api.server
```

**Start frontend (Terminal 2):**
```batch
cd frontend
npm run dev
```

### 3. Check Browser

- Open: http://127.0.0.1:8080
- Wait 5 seconds
- Buttons should now be ENABLED

---

## DATABASE_URL - What to Use?

### Simplest Option (Local Testing)
```
DATABASE_URL=sqlite:///./app.db
```
- No installation needed
- Works immediately
- Use this for getting started

### For Production
See `DATABASE_CONFIG_GUIDE.md` for PostgreSQL/MySQL options

---

## API Keys Explained

| Key | What It Does | Get It From |
|-----|-------------|------------|
| OPENAI_API_KEY | Powers AI responses | https://platform.openai.com/account/api-keys |
| VIDEO_DB_API_KEY | Manages video data | https://app.videodb.io |
| ELEVENLABS_API_KEY | Voice synthesis (optional) | https://elevenlabs.io |

**For now:** Use "test" as placeholder values. Get real keys later.

---

## If Buttons STILL Disabled

### Check 1: Is .env file in correct location?
```
backend/.env  ← Must be HERE
frontend/.env ← NOT here
.env ← NOT here
```

### Check 2: Any errors in backend terminal?
- Look for RED text
- Most common: `ModuleNotFoundError`
  - Fix: `pip install -r requirements.txt`

### Check 3: Is backend really running?
```batch
curl http://127.0.0.1:8000/config/check
```
Should return JSON with no errors.

### Check 4: Browser console errors (F12)
- Open http://127.0.0.1:8080
- Press F12
- Look for red errors about:
  - CORS
  - Connection refused
  - 404 errors

---

## Advanced Guides

- **DATABASE_CONFIG_GUIDE.md** - Production database setup
- **FIX_DISABLED_BUTTONS_GUIDE.md** - Detailed troubleshooting
- **API_SETUP_COMPLETE.md** - All API services explained

---

## Success Indicators

✅ Backend running without errors  
✅ Frontend loads at http://127.0.0.1:8080  
✅ Buttons are ENABLED (clickable)  
✅ "New Chat" button works  
✅ No red errors in browser console

---

## Next: Get Real API Keys

Once buttons work:

1. **OpenAI:**
   - Go: https://platform.openai.com/account/api-keys
   - Click "Create new secret key"
   - Copy the full key
   - Update `OPENAI_API_KEY=` in backend/.env
   - Restart backend

2. **VideoDB:**
   - Go: https://app.videodb.io
   - Sign up or log in
   - Get API key from dashboard
   - Update `VIDEO_DB_API_KEY=` in backend/.env
   - Restart backend

3. **Restart backend:**
   ```batch
   cd backend
   python -m director.entrypoint.api.server
   ```

---

## File Structure Reference

```
your-project/
├── backend/
│   ├── .env ← CREATE THIS FILE HERE
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── director/
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
└── setup.bat
```

---

## One-Command Test

Verify everything is connected:

```batch
REM Test backend is running
curl http://127.0.0.1:8000/config/check

REM Test frontend is running
curl http://127.0.0.1:8080
```

Both should respond without errors.

---

## Emergency: Complete Reset

If nothing works:

```batch
REM Kill everything
taskkill /F /IM node.exe 2>nul
taskkill /F /IM python.exe 2>nul

REM Clear caches
cd frontend && rmdir /s /q node_modules .vite & cd ..
cd backend && rmdir /s /q __pycache__ & del app.db & cd ..

REM Reinstall
npm install -C frontend
pip install -r backend/requirements.txt

REM Start fresh
REM Terminal 1: cd backend && python -m director.entrypoint.api.server
REM Terminal 2: cd frontend && npm run dev
```

Then open http://127.0.0.1:8080 in browser.

