
# QUICK API KEYS REFERENCE CARD

## Getting API Keys (5 minutes each)

### 1. OPENAI_API_KEY
```
URL: https://platform.openai.com/account/api-keys
Free: $5 credit for new users
Key format: sk-proj-XXXXXXXXXXXXX
```

### 2. VIDEO_DB_API_KEY
```
URL: https://app.videodb.io
Free: Yes (free tier available)
Go to: Settings → API Keys → Generate New API Key
```

### 3. ELEVENLABS_API_KEY (Optional)
```
URL: https://elevenlabs.io
Free: 10,000 characters/month
Go to: Settings → API Keys
```

---

## Database Setup

### SQLite (Easy - Recommended for Local)
```
DATABASE_URL=sqlite:///./voice_app.db
DB_TYPE=sqlite
# No setup needed - creates automatically!
```

### PostgreSQL (For Production)

**Option 1: Supabase (Easiest)**
```
1. Go to https://supabase.com → Sign up
2. Create Project → Settings → Database
3. Copy Connection Pooling URL
DATABASE_URL=postgresql://user:pass@host:5432/db
```

**Option 2: Heroku**
```
1. https://www.heroku.com → Create app
2. Add Heroku Postgres add-on
3. Copy DATABASE_URL from Config Vars
```

**Option 3: Local PostgreSQL (Windows)**
```
Download: https://www.postgresql.org/download/windows/
Install → Open Command Prompt:

psql -U postgres

In postgres console:
CREATE DATABASE voice_app;
\q

DATABASE_URL=postgresql://postgres:password@localhost:5432/voice_app
```

---

## SECRET_KEY Generation (Pick ONE)

### Using Python
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Using OpenSSL
```bash
openssl rand -hex 32
```

### Manual (Copy & Modify)
```
aB3xK9mN2pQ7vR5tZ8wL1uY6cJ4hG0iF-sD_eA
```

---

## Complete .env File Template

Create file: `backend/.env`

```env
VIDEO_DB_API_KEY=your-key-here
OPENAI_API_KEY=sk-proj-your-key-here
ELEVENLABS_API_KEY=your-key-here

BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
FRONTEND_URL=http://127.0.0.1:8080

DATABASE_URL=sqlite:///./voice_app.db
DB_TYPE=sqlite

SECRET_KEY=generated-secret-key-here
CORS_ORIGINS=http://127.0.0.1:8080

VOICE_QUALITY=high
MAX_AUDIO_SIZE=52428800
```

---

## Windows Setup (3 Steps)

### Step 1: Create .env
```
Open folder: C:\your-project\backend
Create file: .env (using Notepad)
Paste the template above
Fill in your API keys
Save
```

### Step 2: Verify
```
cd backend
uv run python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"
```
Should print your key if correct!

### Step 3: Run
```
cd backend
uv run python -m director.entrypoint.api.server
```

Frontend opens at: http://127.0.0.1:8080/voice

---

## Troubleshooting Quick Fix

| Error | Fix |
|-------|-----|
| Key invalid | Copy again (no extra spaces) |
| Port 8000 in use | Close other app using port 8000 |
| CORS error | Check FRONTEND_URL matches where frontend runs |
| Database error | Check DATABASE_URL format matches your DB type |
| Module not found | Install: `pip install python-dotenv` |

---

## Pro Tips

1. **Keep keys private** - Never commit .env to git
2. **Use free tier first** - Test with free credits before paying
3. **Different keys for prod** - Create new keys for production
4. **Rotate regularly** - Regenerate keys every 90 days
5. **Check .gitignore** - Add `.env` to prevent accidental commits

---

## URLs Quick Links

OpenAI: https://platform.openai.com/account/api-keys
VideoDB: https://app.videodb.io
ElevenLabs: https://elevenlabs.io/app/settings/api-keys
Supabase: https://supabase.com
Heroku: https://www.heroku.com
PostgreSQL: https://www.postgresql.org/download/windows/

---

## That's it!

Follow the steps above and you'll have everything configured in 15 minutes.

Questions? See `API_SETUP_COMPLETE.md` for detailed guide.
