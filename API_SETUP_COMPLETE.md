
# Complete API Keys & Environment Setup Guide

## Overview
This guide helps you obtain all required API keys and configure your environment files for the Voice Chat application.

---

## 1. OPENAI_API_KEY - Speech-to-Text & Responses

### Get Your OpenAI API Key:

**Step-by-Step:**

1. Go to https://platform.openai.com/account/api-keys
2. Sign in with your OpenAI account (create one if needed)
3. Click "Create new secret key"
4. Copy the key (you can only see it once!)
5. Store it safely

**Free Credit:** OpenAI offers $5 free credits for new accounts (expires after 3 months)

**Pricing:** ~$0.001 per 1000 tokens for Whisper (speech-to-text)

**Add to .env:**
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 2. VIDEO_DB_API_KEY - Video/Audio Database

### Get Your VideoDb API Key:

**Step-by-Step:**

1. Go to https://app.videodb.io
2. Sign up with email or GitHub
3. Verify your email
4. Go to Settings → API Keys
5. Click "Generate New API Key"
6. Copy the API key

**Free Credit:** VideoDB provides free tier access

**Add to .env:**
```
VIDEO_DB_API_KEY=your-videodb-api-key-here
```

---

## 3. ELEVENLABS_API_KEY - Text-to-Speech (Optional)

### Get Your ElevenLabs API Key:

**Step-by-Step:**

1. Go to https://elevenlabs.io
2. Click "Sign Up" (or login if you have account)
3. Verify email
4. Go to https://elevenlabs.io/app/settings/api-keys
5. Copy your API Key
6. Store it safely

**Free Tier:** 10,000 characters/month free

**Add to .env:**
```
ELEVENLABS_API_KEY=your-elevenlabs-api-key-here
```

**Note:** If you skip this, the app will still work using OpenAI's TTS

---

## 4. Database Configuration

### For Local Development (SQLite - Recommended):

**No additional setup needed!**

SQLite is built-in. Just use:

```
DATABASE_URL=sqlite:///./voice_app.db
DB_TYPE=sqlite
```

The database file will auto-create at `voice_app.db`

### For Production (PostgreSQL - Recommended):

**Option A: Use a Cloud Provider (Easy)**

#### Supabase (FREE tier available):
1. Go to https://supabase.com
2. Sign up
3. Create a new project
4. Go to Settings → Database
5. Copy the connection string under "Connection pooling"
6. Format: `postgresql://user:password@host:port/database`

```
DATABASE_URL=postgresql://username:password@db.supabase.co:5432/postgres
DB_TYPE=postgresql
```

#### Heroku Postgres:
1. Go to https://www.heroku.com
2. Create account
3. Create new app → Add Heroku Postgres add-on
4. Copy DATABASE_URL from Config Vars

#### Render PostgreSQL:
1. Go to https://render.com
2. Create new PostgreSQL database
3. Copy the External Database URL

**Option B: Self-Hosted PostgreSQL:**

On Windows (using WSL or native):
```bash
# Install PostgreSQL from https://www.postgresql.org/download/windows/
# After installation, open Command Prompt:
psql -U postgres

# In postgres console:
CREATE DATABASE voice_app;
\q
```

Then add to .env:
```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/voice_app
DB_TYPE=postgresql
```

---

## 5. Server Configuration

### Explanation:

```
BACKEND_HOST=127.0.0.1          # Localhost for development
BACKEND_PORT=8000               # Flask/Uvicorn default port
FRONTEND_URL=http://127.0.0.0:8080  # Where frontend runs
```

**For Local Development (No Changes Needed):**
```
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
FRONTEND_URL=http://127.0.0.1:8080
```

**For Production:**
```
BACKEND_HOST=0.0.0.0            # Listen on all interfaces
BACKEND_PORT=8000               # Or your cloud provider's port
FRONTEND_URL=https://yourdomain.com  # Your actual domain
```

---

## 6. Security Configuration

### SECRET_KEY - Generate One:

**Option 1: Python (Easiest)**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Output example: `Z_X9w3k_n2jL_c8X9k2_n3mL_9jK_8wL`

**Option 2: OpenSSL**
```bash
openssl rand -hex 32
```

**Option 3: Manual (Less Secure)**
```
your-super-secret-key-with-random-characters-here-12345
```

**Add to .env:**
```
SECRET_KEY=Z_X9w3k_n2jL_c8X9k2_n3mL_9jK_8wL
```

### CORS_ORIGINS:

```
# Local development:
CORS_ORIGINS=http://127.0.0.1:8080,http://localhost:8080

# Production:
CORS_ORIGINS=https://yourdomain.com
```

---

## 7. Voice Configuration

### VOICE_QUALITY:

```
VOICE_QUALITY=high      # Best quality, slower processing (recommended)
VOICE_QUALITY=medium    # Balanced
VOICE_QUALITY=low       # Fast processing, lower quality
```

### MAX_AUDIO_SIZE:

```
MAX_AUDIO_SIZE=52428800  # 50MB in bytes (can handle long recordings)
```

---

## Complete .env Template

Save this as `backend/.env`:

```env
# API Keys
VIDEO_DB_API_KEY=your-videodb-api-key-here
OPENAI_API_KEY=sk-proj-your-openai-key-here
ELEVENLABS_API_KEY=your-elevenlabs-key-here

# Server Configuration
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
FRONTEND_URL=http://127.0.0.1:8080

# Database Configuration (Use ONE based on your choice)
# For SQLite (Local Development):
DATABASE_URL=sqlite:///./voice_app.db
DB_TYPE=sqlite

# For PostgreSQL (Uncomment if using PostgreSQL):
# DATABASE_URL=postgresql://username:password@localhost:5432/voice_app
# DB_TYPE=postgresql

# Security Configuration
SECRET_KEY=your-generated-secret-key-here
CORS_ORIGINS=http://127.0.0.1:8080,http://localhost:8080

# Voice Configuration
VOICE_QUALITY=high
MAX_AUDIO_SIZE=52428800
```

---

## Windows Setup Instructions

### 1. Backend (.env file)

```bash
cd backend
# Create .env file in this directory
# Edit with Notepad and add the values from above
```

### 2. Test Configuration

```bash
cd backend
uv run python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"
```

If you see your key printed, configuration is correct!

### 3. Run Backend

```bash
cd backend
uv run python -m director.entrypoint.api.server
```

---

## Quick Reference Checklist

- [ ] OpenAI API Key obtained and added
- [ ] VideoDb API Key obtained and added
- [ ] ElevenLabs API Key obtained (or leave blank)
- [ ] Database configured (SQLite or PostgreSQL)
- [ ] Backend host/port configured
- [ ] Frontend URL configured
- [ ] Secret key generated
- [ ] CORS origins set correctly
- [ ] Voice quality set
- [ ] Max audio size set

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'dotenv'"

Solution: Add python-dotenv to requirements
```bash
pip install python-dotenv
```

### "API key is invalid"

- Verify the key is copied completely (no extra spaces)
- Check if key has expired (OpenAI keys don't expire, but check VideoDB)
- Try regenerating the key

### "Connection refused" on backend

- Ensure backend is running: `uv run python -m director.entrypoint.api.server`
- Check port 8000 isn't already in use

### "CORS error" in browser

- Verify FRONTEND_URL in backend .env matches where frontend is running
- Check CORS_ORIGINS includes the frontend URL

---

## Security Best Practices

1. **Never commit .env files to Git**
   ```bash
   # Add to .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use different keys for production**
   - Create separate OpenAI API key for production
   - Use different database for production

3. **Rotate keys regularly**
   - Regenerate API keys every 90 days
   - If compromised, regenerate immediately

4. **Use environment variables in CI/CD**
   - GitHub Actions, GitLab CI, etc.
   - Never hardcode secrets in code

---

## Next Steps

1. Obtain all API keys from the services above
2. Create `backend/.env` file
3. Add all values from the template
4. Run the backend: `uv run python -m director.entrypoint.api.server`
5. Run the frontend: `npm run dev`
6. Visit http://127.0.0.1:8080/voice

Done! Your voice chat app is ready to use.
