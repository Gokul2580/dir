# Database Configuration Guide

## Quick Answer: What DATABASE_URL to Use?

### For Local Development (Easiest - Recommended)
```
DATABASE_URL=sqlite:///./app.db
```
This creates a SQLite database file locally. No external services needed.

---

## DATABASE_URL Options

### 1. SQLite (Local Development)
**Use this if you're starting out on Windows**
```
DATABASE_URL=sqlite:///./app.db
```
- No installation required
- File-based database
- Perfect for testing
- Not recommended for production

### 2. PostgreSQL (Recommended for Production)

#### Option A: Local PostgreSQL on Windows
**After installing PostgreSQL:**
```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/director_db
```

#### Option B: PostgreSQL on Cloud (Easiest for Production)

**Supabase (Free tier available):**
```
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@[PROJECT-ID].supabase.co:5432/postgres
```
1. Go to: https://supabase.com
2. Click "New project"
3. Set project name: "director"
4. Choose a password
5. Wait for setup (2-3 min)
6. Copy connection string from Settings > Database > Connection Pooling
7. Keep "Session mode" selected
8. Paste full URL into DATABASE_URL

**Railway (Simple 1-Click Deploy):**
```
DATABASE_URL=postgresql://postgres:password@containers.railway.app:5432/railway
```
1. Go to: https://railway.app
2. Click "Create"
3. Select "PostgreSQL"
4. Copy DATABASE_URL from variables tab

**Heroku (With free tier):**
```
DATABASE_URL=postgresql://username:password@host:port/database
```
1. Go to: https://www.heroku.com
2. Create account
3. Create new app
4. Add "Heroku Postgres" add-on
5. Copy DATABASE_URL from Config Vars

### 3. MySQL (Alternative)
```
DATABASE_URL=mysql://user:password@localhost:3306/director_db
```

---

## Environment File Setup

### Create `.env` file in backend directory

**Windows (using Notepad):**
1. Open Notepad
2. Paste this:
```
# API Keys
VIDEO_DB_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here

# Server Configuration
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
FRONTEND_URL=http://127.0.0.1:8080

# Database (choose ONE of these)
DATABASE_URL=sqlite:///./app.db
# OR for PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost:5432/director_db

DB_TYPE=sqlite

# Security
SECRET_KEY=your-super-secret-key-change-this
CORS_ORIGINS=http://127.0.0.1:8080

# Voice Configuration
VOICE_QUALITY=high
MAX_AUDIO_SIZE=52428800
```
3. File > Save As
4. Choose folder: `backend/`
5. Filename: `.env` (including the dot)
6. File type: "All Files (*.*)"
7. Click Save

---

## Why UI Buttons Are Disabled

The buttons are disabled because:

1. **Missing DATABASE_URL** - Backend can't connect to database
2. **Missing API Keys** - Backend services aren't initialized
3. **Backend not responding** - Frontend waiting for backend health check

### Fix Steps:

1. **Create `.env` file** in `backend/` folder with at least:
   ```
   DATABASE_URL=sqlite:///./app.db
   OPENAI_API_KEY=your_key
   VIDEO_DB_API_KEY=your_key
   SECRET_KEY=generate-random-string-here
   ```

2. **Restart backend:**
   ```batch
   cd backend
   python -m director.entrypoint.api.server
   ```

3. **Frontend should connect** and buttons become enabled

---

## Generate SECRET_KEY

### Windows Command Prompt:
```batch
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Or use this command:
```batch
python -c "import uuid; print(str(uuid.uuid4()))"
```

Copy the output and paste into `.env` as SECRET_KEY value.

---

## Database Type Guidance

| Database | Best For | Setup Time | Cost | Notes |
|----------|----------|-----------|------|-------|
| **SQLite** | Local dev, testing | 0 min | Free | File-based, no server |
| **PostgreSQL** | Production | 5-10 min | Free tier available | Industry standard |
| **MySQL** | Production | 5-10 min | Free tier available | Good alternative |

---

## Verify Configuration

After setting up `.env`:

1. Backend should start without errors
2. Frontend URL should load at `http://127.0.0.1:8080`
3. Buttons should be enabled (not grayed out)
4. You can create new chats and agents

If buttons still disabled:
1. Check browser console (F12) for errors
2. Check backend terminal for connection errors
3. Verify .env file is in correct folder (backend/)
4. Restart both frontend and backend

---

## Common Issues

### "DATABASE_URL not found"
- Check `.env` file is in `backend/` folder
- Restart backend after creating `.env`

### "PostgreSQL connection refused"
- Verify PostgreSQL is running
- Check username/password
- Verify database name exists

### Buttons still disabled
- Wait 5 seconds for backend to fully initialize
- Refresh browser (Ctrl+F5)
- Check console (F12) for network errors

