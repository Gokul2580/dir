# Director Voice Chat - Quick Reference

## Windows Users - Quick Start

```batch
# Run these commands in order:

# 1. Setup (first time only)
setup.bat

# 2. Configure API Keys
notepad backend\.env
# Add your API keys:
# OPENAI_API_KEY=sk-...
# ELEVENLABS_API_KEY=... (optional)
# VIDEO_DB_API_KEY=...

# 3. Start Application
run.bat

# 4. Open in Browser
# Visit: http://127.0.0.1:8080/voice
```

## Getting API Keys

### OpenAI (Required)
1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Copy and save in `backend\.env` as `OPENAI_API_KEY`

### ElevenLabs (Optional, for better voices)
1. Sign up at https://elevenlabs.io
2. Go to API Keys section
3. Copy key to `backend\.env` as `ELEVENLABS_API_KEY`

### VideoDB (Required)
1. Visit https://console.videodb.io
2. Create API key
3. Add to `backend\.env` as `VIDEO_DB_API_KEY`

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `setup.bat` | Initial setup (run once) |
| `run.bat` | Start backend + frontend |
| `run-be.bat` | Start backend only |
| `run-fe.bat` | Start frontend only |
| `dev.bat` | Development mode with auto-reload |

## Accessing the Application

- **Voice Chat**: http://127.0.0.1:8080/voice
- **Backend API**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs

## Voice Chat Features

### Recording
- Click "🎤 Start Recording" 
- Speak clearly
- Click "⏹️ Stop Recording"
- Auto-transcription (if enabled)

### Playback
- Click "▶️ Play" to hear responses
- Adjust volume with slider
- Seek to any position

### Settings
- **Response Voice**: Select voice for AI responses
- **Auto-transcribe**: Auto-transcribe after recording
- **Auto-play**: Auto-play AI responses
- **Backend URL**: Configure server address

## Troubleshooting

### Issue: "Microphone access denied"
**Fix**: 
1. Check browser permissions
2. Click camera icon in address bar
3. Allow microphone access
4. Reload page

### Issue: "Failed to transcribe audio"
**Fix**:
1. Verify OPENAI_API_KEY is correct
2. Check audio format (WAV, MP3, OGG)
3. Ensure file < 50MB
4. Check API quota

### Issue: Ports already in use
**Fix**:
```batch
# Change port in frontend\.env
# VITE_PORT=8081

# Or kill existing processes:
taskkill /F /IM node.exe
taskkill /F /IM python.exe
```

### Issue: Slow performance
**Fix**:
1. Close other applications
2. Check internet connection
3. Restart app: `Ctrl+C` then run script again
4. Check API rate limits

## Common Commands

### Check if services running
```batch
netstat -ano | findstr :8000
netstat -ano | findstr :8080
```

### View logs
```batch
# Backend logs
cd backend
type venv\Scripts\python.log

# Frontend logs
cd frontend
type npm.log
```

### Reset everything
```batch
# Delete and recreate
rmdir /s /q backend\venv
rmdir /s /q frontend\node_modules
setup.bat
```

## Useful URLs

- Voice Chat: http://127.0.0.1:8080/voice
- Default View: http://127.0.0.1:8080
- Backend Status: http://127.0.0.1:8000
- Windows Guide: `/docs/get_started/windows.md`
- Voice Chat Docs: `/docs/guides/VOICE_CHAT.md`

## Production Deployment

For production, see: `/DEPLOYMENT.md`

Quick summary:
1. Use PostgreSQL (not SQLite)
2. Set up SSL/TLS certificates
3. Configure environment variables
4. Use Docker for deployment
5. Set up monitoring with Prometheus
6. Enable error tracking with Sentry
7. Configure automatic backups

## File Structure

```
director/
├── setup.bat              ← Run this first
├── run.bat                ← Run this to start
├── backend/
│   └── .env               ← Edit this with API keys
├── frontend/
│   └── .env               ← Configure backend URL
├── docs/
│   ├── get_started/
│   │   └── windows.md     ← Detailed Windows guide
│   └── guides/
│       └── VOICE_CHAT.md  ← Voice chat feature guide
└── DEPLOYMENT.md          ← Production deployment guide
```

## Voice Settings Reference

### Available Voices
- **default**: Rachel (warm, professional)
- **male**: Adam (deep, authoritative)
- **female**: Rachel (warm, professional)

### Voice Quality
- **low**: Faster, smaller files
- **medium**: Balanced
- **high**: Best quality, larger files

## API Endpoints

### Transcribe Audio
```
POST /voice/transcribe
Body: multipart/form-data with "file"
Returns: { transcription: "..." }
```

### Generate Speech
```
POST /voice/speech
Body: JSON { text: "...", voice_id: "default" }
Returns: { audio_url: "..." }
```

### Full Chat
```
POST /voice/chat
Body: multipart/form-data with audio + settings
Returns: { transcription: "...", audio_response_url: "..." }
```

## Performance Tips

1. **Recording**: Use clear, close microphone
2. **Network**: Ensure stable internet connection
3. **Processing**: Wait for transcription to complete
4. **Browser**: Use modern browser (Chrome, Edge, Firefox)
5. **Volume**: Adjust mic and speaker volume appropriately

## Security Tips

1. Never share API keys in code
2. Keep .env files private (in .gitignore)
3. Use strong SECRET_KEY for production
4. Enable HTTPS/SSL in production
5. Restrict CORS origins to trusted domains
6. Implement rate limiting for API
7. Use JWT authentication for APIs

## Support

- GitHub Issues: https://github.com/Gokul2580/dir/issues
- Documentation: `/docs/`
- Windows Guide: `/docs/get_started/windows.md`
- Voice Chat Guide: `/docs/guides/VOICE_CHAT.md`
- Deployment Guide: `/DEPLOYMENT.md`

---

**Quick Reference Version 1.0**  
**Last Updated: March 2024**  
**Status: Production Ready**
