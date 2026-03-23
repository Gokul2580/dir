## Quick Start - Voice Chat App

### Setup (Windows)

```batch
# Run setup (first time only)
setup.bat

# Then in the project root:
dev.bat
```

Or manually:
```batch
# Terminal 1 - Backend
cd backend
uv run python -m director.entrypoint.api.server

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Access the App

1. **Text Chat:** http://127.0.0.1:8080
2. **Voice Chat:** http://127.0.0.1:8080/voice
3. **Voice Editor:** Use the playback component after recording

### Features Quick Reference

| Feature | How To | What It Does |
|---------|--------|------------|
| **Record** | Click "Start Recording" button | Capture voice input with auto-transcription |
| **Play/Edit** | Click "Play" in editor | Control playback with full editing suite |
| **Trim** | Set start/end times or drag on waveform | Cut unwanted audio sections |
| **Voice Filter** | Select from 6 voice effects | Change voice characteristics (deep, high, robotic, etc) |
| **Enhance** | Click enhancement buttons | Improve audio quality (denoise, normalize, compress) |
| **Subtitle** | Auto-generated from transcription | Edit and export as SRT for video editors |
| **Cut/Segment** | Click "Add Cut" at timestamp | Create breakpoints in audio |
| **Export** | Choose format and click Export | Download edited audio |

### Key Keyboard Shortcuts

- **Space** - Play/Pause audio
- **Ctrl+S** - Save/Export
- **Arrow Keys** - Seek forward/backward 5 seconds

### File Locations

```
frontend/
├── src/
│   ├── components/
│   │   ├── AudioRecorder.vue      # Recording component
│   │   ├── VoicePlayback.vue      # Full editor with CapCut features
│   │   └── VoiceChatInterface.vue # Chat interface
│   ├── views/
│   │   └── VoiceChatView.vue      # Voice chat page
│   └── router/
│       └── index.js               # Routes setup

backend/
├── director/
│   ├── agents/
│   │   └── voice_chat.py          # Voice processing agent
│   └── entrypoint/
│       └── api/
│           ├── routes.py          # API endpoints
│           └── server.py          # Server setup
```

### Common Issues

**Q: "Microphone access denied"**
A: Check browser permissions. Click the lock icon in address bar and enable microphone.

**Q: "No audio playback"**
A: Ensure your system audio is not muted. Check browser volume settings.

**Q: "Subtitles not generating"**
A: Verify transcription completed successfully. Auto-subtitles require transcription text.

**Q: "Export button disabled"**
A: Recording must complete and audio must load successfully before export is enabled.

### Supported Formats

- **Input:** WAV, MP3, OGG, AAC (via browser support)
- **Output:** WAV, MP3, AAC, OGG
- **Subtitles:** SRT format for all video editors

### Performance Tips

- Use 16-bit mono audio for best results
- Keep recordings under 10 minutes initially
- Clear browser cache if having issues
- Use Chrome/Firefox for best compatibility

### Backend API Endpoints

```
POST /voice/transcribe     # Convert audio to text
POST /voice/speech         # Convert text to audio
POST /voice/chat           # Full voice interaction
```

### Next Steps

1. Try recording a short message
2. Use voice filters to modify it
3. Export edited audio
4. Generate and export subtitles
5. Experiment with all enhancement options

Enjoy your voice editing experience!
