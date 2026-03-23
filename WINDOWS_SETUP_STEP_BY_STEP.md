
# Windows Step-by-Step Setup Guide

## Complete Setup from Zero to Running

This guide takes you from nothing to a fully running voice chat app on Windows.

---

## Prerequisites

Ensure you have installed:
- Node.js (https://nodejs.org)
- Python 3.10+ (https://www.python.org/downloads)
- Git (https://git-scm.com/download/win)

Test in Command Prompt:
```bash
node --version
python --version
```

---

## Step 1: Get Your API Keys (15 minutes)

### 1.1 OpenAI API Key

1. Open browser: https://platform.openai.com/account/api-keys
2. Sign in (create account if needed)
3. Click "Create new secret key"
4. Copy the key (starts with `sk-proj-`)
5. Save it somewhere safe (notepad)

**Your key:** `sk-proj-XXXXXXXXXXXXXX`

### 1.2 VideoDB API Key

1. Open browser: https://app.videodb.io
2. Sign up (with email or GitHub)
3. Verify your email
4. Go to Settings → API Keys
5. Click "Generate New API Key"
6. Copy and save it

**Your key:** `XXXXXXXXXXXXXX`

### 1.3 ElevenLabs API Key (Optional)

1. Go to https://elevenlabs.io
2. Sign up
3. Verify email
4. Go to https://elevenlabs.io/app/settings/api-keys
5. Copy API key
6. Save it (can leave blank in .env if you skip)

**Your key:** `XXXXXXXXXXXXXX`

---

## Step 2: Generate SECRET_KEY (2 minutes)

Open Command Prompt and run:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output. Example:
```
aB3xK9mN2pQ7vR5tZ8wL1uY6cJ4hG0iF-sD_eA
```

Save it.

---

## Step 3: Create .env File (5 minutes)

### Windows Steps:

1. Open File Explorer
2. Navigate to your project folder
3. Open `backend` folder
4. Right-click → New → Text Document
5. Name it `.env` (delete the `.txt`)
   - If you see `.txt`, open as text document in Notepad
   - Save As → Change name to `.env`

### Paste This Into .env:

Replace the XXXXX with YOUR actual keys from Step 1:

```env
# API Keys - Replace with YOUR keys
VIDEO_DB_API_KEY=your-videodb-key-here
OPENAI_API_KEY=sk-proj-your-openai-key-here
ELEVENLABS_API_KEY=your-elevenlabs-key-here

# Server Configuration
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
FRONTEND_URL=http://127.0.0.1:8080

# Database (SQLite for local - no changes needed)
DATABASE_URL=sqlite:///./voice_app.db
DB_TYPE=sqlite

# Security - Use the key from Step 2
SECRET_KEY=your-generated-secret-key-from-step-2

# CORS
CORS_ORIGINS=http://127.0.0.1:8080

# Voice Settings
VOICE_QUALITY=high
MAX_AUDIO_SIZE=52428800
```

Save the file (Ctrl+S).

### Verify File Saved Correctly:

In File Explorer, the file should show as `.env` (not `.env.txt`)

---

## Step 4: Install Frontend Dependencies (2 minutes)

Open Command Prompt and run:

```bash
cd frontend
npm install
```

This downloads all required packages. Will take 1-2 minutes.

---

## Step 5: Start Backend (Terminal 1)

Open NEW Command Prompt window:

```bash
cd backend
uv run python -m director.entrypoint.api.server
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Keep this window open!

---

## Step 6: Start Frontend (Terminal 2)

Open ANOTHER NEW Command Prompt window:

```bash
cd frontend
npm run dev
```

You should see:
```
VITE v5.4.1  ready in XXX ms

Local:   http://127.0.0.1:5173/
```

---

## Step 7: Open Your App

1. Open web browser
2. Go to: `http://127.0.0.1:8080/voice`
3. Click "Start Recording"
4. Speak into your microphone
5. Click "Stop Recording"
6. Watch the magic happen!

---

## Troubleshooting

### Problem: "Port 8000 already in use"

Someone else is using port 8000. Options:
1. Close other apps
2. Change port in .env to 8001:
   ```
   BACKEND_PORT=8001
   FRONTEND_URL=http://127.0.0.1:8080
   ```
3. Restart

### Problem: "API key invalid"

- Copy key again from the website (no extra spaces)
- Make sure entire key is copied
- Try regenerating the key on the website

### Problem: "npm: command not found"

Node.js not installed. Download from https://nodejs.org

### Problem: "python: command not found"

Python not installed. Download from https://www.python.org/downloads

### Problem: "File .env not found"

Make sure:
1. File is named exactly `.env` (not `.env.txt`)
2. File is in `backend` folder
3. Use Notepad to verify - should show just text, no code highlighting

### Problem: "CORS error" in browser

Check .env has correct:
```
FRONTEND_URL=http://127.0.0.1:8080
CORS_ORIGINS=http://127.0.0.1:8080
```

### Problem: "Microphone access denied"

Browser is blocking microphone:
1. Click lock icon next to URL
2. Allow Microphone
3. Refresh page

---

## Testing Your Setup

### Test 1: Verify Backend Running

Open browser: `http://127.0.0.1:8000`

Should show backend API info.

### Test 2: Verify Frontend Running

Open browser: `http://127.0.0.1:8080`

Should show the app.

### Test 3: Test Voice Recording

1. Go to: `http://127.0.0.1:8080/voice`
2. Click "Start Recording"
3. Say "Hello World"
4. Click "Stop Recording"
5. Should transcribe what you said

---

## Next Steps - Production Deployment

Once everything works locally, you can deploy:

### Option 1: Heroku (Free)
- Heroku website: https://www.heroku.com
- Deploy instructions in DEPLOYMENT.md

### Option 2: Railway (Cheap)
- Railway website: https://railway.app
- Paste your repo URL

### Option 3: Vercel + Backend Service
- Frontend to Vercel (free)
- Backend to Railway or Render

---

## Files Reference

Your project structure should look like:

```
your-project/
├── backend/
│   ├── .env                    # Your config file (created Step 3)
│   ├── requirements.txt
│   └── director/
├── frontend/
│   ├── src/
│   ├── package.json
│   └── public/
├── setup.bat
└── README.md
```

---

## Quick Command Reference

| Command | What it does |
|---------|-------------|
| `cd frontend` | Enter frontend folder |
| `cd backend` | Enter backend folder |
| `npm install` | Install dependencies |
| `npm run dev` | Start dev server |
| `uv run python -m director.entrypoint.api.server` | Start backend |
| `python -c "import secrets; print(secrets.token_urlsafe(32))"` | Generate secret key |
| `Ctrl+C` | Stop running process |

---

## Success Checklist

- [ ] Obtained all API keys (OpenAI, VideoDB)
- [ ] Generated SECRET_KEY
- [ ] Created `.env` file in backend folder
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Backend running on http://127.0.0.1:8000
- [ ] Frontend running on http://127.0.0.1:8080
- [ ] Can access voice chat at http://127.0.0.1:8080/voice
- [ ] Microphone recording works
- [ ] Voice transcription works

---

## You're Done!

If you reach this point, everything is working. Enjoy your voice chat app!

Need help? Check the other documentation files or create an issue on GitHub.
