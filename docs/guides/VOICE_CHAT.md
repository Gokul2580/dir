# Voice Chat Feature Implementation Guide

## Overview

The Director application now includes a fully functional voice chat system that allows users to interact with AI agents using speech-to-text and text-to-speech capabilities. This guide explains how to use and configure the voice chat feature.

## Features

### Core Voice Chat Features

1. **Speech-to-Text Transcription**
   - Uses OpenAI's Whisper API for accurate transcription
   - Supports multiple audio formats (WAV, MP3, OGG)
   - Real-time transcription feedback

2. **Text-to-Speech Response**
   - Uses ElevenLabs API for natural-sounding responses
   - Falls back to OpenAI TTS if ElevenLabs is unavailable
   - Customizable voice selection

3. **Audio Recording**
   - Built-in audio recorder with real-time waveform visualization
   - Recording time tracking
   - High-quality audio capture (44.1kHz, mono)

4. **Voice Playback**
   - Waveform visualization during playback
   - Volume control
   - Seek functionality
   - Progress tracking

5. **Chat History**
   - Persistent conversation history
   - User and AI message distinction
   - Audio file references

## Getting Started

### Windows Setup

For Windows users, follow these steps:

```batch
# 1. Run the setup script
setup.bat

# 2. Update backend\.env with your API keys
# Open backend\.env and add:
# - OPENAI_API_KEY
# - ELEVENLABS_API_KEY (optional)
# - VIDEO_DB_API_KEY

# 3. Start the application
run.bat

# 4. Access the voice chat
# Open browser: http://127.0.0.1:8080/voice
```

See `/docs/get_started/windows.md` for detailed Windows setup instructions.

### Mac/Linux Setup

```bash
# 1. Run the setup script
./setup.sh

# 2. Update backend/.env with your API keys
echo "OPENAI_API_KEY=sk-..." >> backend/.env
echo "ELEVENLABS_API_KEY=..." >> backend/.env

# 3. Start the application
make run

# 4. Access the voice chat
# Open browser: http://127.0.0.1:8080/voice
```

### Docker Setup

```bash
# 1. Build images
docker-compose build

# 2. Configure environment
cp .env.example .env
# Update .env with API keys

# 3. Start services
docker-compose up -d

# 4. Access the voice chat
# http://your-domain/voice
```

## API Endpoints

### Voice Transcription

**Endpoint**: `POST /voice/transcribe`

**Request**:
```bash
curl -X POST -F "file=@audio.wav" http://127.0.0.1:8000/voice/transcribe
```

**Response**:
```json
{
  "success": true,
  "transcription": "Hello, how are you doing today?"
}
```

### Voice Speech Generation

**Endpoint**: `POST /voice/speech`

**Request**:
```bash
curl -X POST http://127.0.0.1:8000/voice/speech \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I am doing great, thank you for asking!",
    "voice_id": "default"
  }'
```

**Response**:
```json
{
  "success": true,
  "audio_url": "audio_responses/response_abc123.mp3"
}
```

### Full Voice Chat

**Endpoint**: `POST /voice/chat`

**Request**:
```bash
curl -X POST http://127.0.0.1:8000/voice/chat \
  -F "audio=@user_audio.wav" \
  -F "response_text=This is the AI response" \
  -F "voice_id=default" \
  -F "generate_speech=true"
```

**Response**:
```json
{
  "success": true,
  "data": {
    "transcription": "What is the weather like?",
    "audio_response_url": "audio_responses/response_xyz789.mp3",
    "voice_id": "default"
  }
}
```

## Configuration

### Backend Configuration

#### Environment Variables

Create or update `backend/.env`:

```env
# OpenAI API (Required for transcription and fallback TTS)
OPENAI_API_KEY=sk-your-key-here

# ElevenLabs API (Optional, for premium text-to-speech)
ELEVENLABS_API_KEY=your-key-here

# Voice Settings
VOICE_QUALITY=high          # Quality: low, medium, high
MAX_AUDIO_SIZE=52428800     # Maximum audio file size (50MB)
AUDIO_TIMEOUT=30            # Audio processing timeout (seconds)
```

#### Available Voices

- **default** / **female**: Rachel (warm, professional)
- **male**: Adam (deep, authoritative)

### Frontend Configuration

The frontend automatically detects the backend URL. For custom backends, update `.env`:

```env
VITE_APP_BACKEND_URL=http://your-backend-domain:8000
```

## Voice Chat Interface Guide

### Recording Audio

1. Click "🎤 Start Recording" button
2. Speak clearly into your microphone
3. Click "⏹️ Stop Recording" when finished
4. Audio will be automatically transcribed

### Settings

Access settings by clicking "⚙️ Settings":

- **Response Voice**: Choose which voice the AI should use
- **Auto-transcribe**: Automatically transcribe recorded audio
- **Auto-play responses**: Automatically play AI response audio
- **Backend URL**: Configure backend server address

### Chat History

- View all previous conversations
- Each message shows transcription and audio
- Click "Clear History" to start fresh

## Advanced Usage

### Batch Audio Processing

Process multiple audio files:

```python
import requests
import os

backend_url = "http://127.0.0.1:8000"

for audio_file in os.listdir("audio_files/"):
    with open(f"audio_files/{audio_file}", "rb") as f:
        response = requests.post(
            f"{backend_url}/voice/transcribe",
            files={"file": f}
        )
        print(f"{audio_file}: {response.json()['transcription']}")
```

### Custom Voice Cloning

For ElevenLabs users with voice cloning:

```json
{
  "text": "Hello world",
  "voice_id": "your-custom-voice-id"
}
```

### Real-time Transcription

Subscribe to real-time transcription via WebSocket:

```javascript
const socket = io('http://127.0.0.1:8000', {namespace: '/chat'});

socket.on('voice_message_start', () => {
  console.log('Voice processing started');
});

socket.on('voice_chunk', (data) => {
  console.log('Partial transcription:', data.partial_text);
});

socket.on('voice_message_end', (data) => {
  console.log('Final transcription:', data.text);
});
```

## Troubleshooting

### Microphone Not Found

**Error**: "Microphone access denied"

**Solution**:
1. Check browser permissions for microphone access
2. Ensure microphone is connected and enabled
3. Try a different browser
4. Restart the browser

### Transcription Fails

**Error**: "Failed to transcribe audio"

**Solution**:
1. Verify OPENAI_API_KEY is set correctly
2. Check audio file format (WAV, MP3, OGG supported)
3. Ensure audio file is not corrupted
4. Check file size (max 50MB)

### Speech Generation Not Working

**Error**: "Failed to generate speech"

**Solution**:
1. Verify OPENAI_API_KEY for fallback TTS
2. For ElevenLabs, verify ELEVENLABS_API_KEY
3. Check text length (max 5000 characters)
4. Ensure voice_id is valid

### Audio Won't Play

**Error**: Audio element shows error or no sound

**Solution**:
1. Check browser console for CORS errors
2. Verify audio file exists and is accessible
3. Check volume settings (not muted)
4. Try a different browser

## Performance Optimization

### For Large Audio Files

```python
# Compress audio before upload
import librosa
import soundfile as sf

# Load and resample
audio, sr = librosa.load('input.wav', sr=16000)

# Save compressed version
sf.write('compressed.wav', audio, sr)
```

### For Production Deployments

1. **Enable caching**:
   ```python
   from flask_caching import Cache
   cache = Cache(app, config={'CACHE_TYPE': 'redis'})
   ```

2. **Implement rate limiting**:
   ```python
   from flask_limiter import Limiter
   limiter.limit("10 per minute")(transcribe_audio)
   ```

3. **Use CDN for audio delivery**:
   - CloudFlare
   - AWS CloudFront
   - Azure CDN

## Security Considerations

### Privacy

- Audio files are not stored permanently (processed and deleted)
- Transcriptions are not logged to disk
- Use HTTPS/WSS for secure transmission

### API Security

- Restrict API endpoints with authentication
- Implement rate limiting to prevent abuse
- Validate all input (audio format, file size)
- Use environment variables for sensitive keys

### Compliance

- GDPR: Implement data deletion after retention period
- HIPAA: Ensure encryption for healthcare applications
- PCI-DSS: If handling payment information

## Limits and Quotas

### File Size

- Maximum audio file: 50MB
- Recommended: < 25MB for faster processing

### API Quotas

- OpenAI Whisper: Check your plan at openai.com
- ElevenLabs: Check your plan at elevenlabs.io

### Processing Time

- Average: 5-10 seconds per minute of audio
- Max: 60 seconds timeout per request

## Future Enhancements

Planned voice chat improvements:

- [ ] Real-time streaming audio processing
- [ ] Voice emotion detection
- [ ] Multi-language support
- [ ] Voice biometric authentication
- [ ] Audio quality analysis
- [ ] Conversation summarization
- [ ] Speaker identification
- [ ] Background noise reduction

## Support

For issues or questions:

1. Check this guide's troubleshooting section
2. Review `/docs` for additional documentation
3. Check logs: `docker-compose logs -f backend`
4. Open an issue: https://github.com/Gokul2580/dir/issues
5. Community: Discord/Slack (if available)

---

**Version**: 1.0  
**Last Updated**: 2024  
**Status**: Production Ready
