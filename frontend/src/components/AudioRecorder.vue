<template>
  <div class="audio-recorder">
    <div class="recorder-header">
      <h3>Audio Recorder</h3>
      <span class="recording-status" :class="{ recording: isRecording }">
        {{ isRecording ? '● Recording...' : 'Ready' }}
      </span>
    </div>

    <div class="recorder-controls">
      <button
        @click="toggleRecording"
        class="btn btn-primary"
        :disabled="isProcessing"
      >
        <span v-if="!isRecording">🎤 Start Recording</span>
        <span v-else>⏹️ Stop Recording</span>
      </button>

      <button
        @click="clearRecording"
        class="btn btn-secondary"
        :disabled="!recordedChunks.length || isRecording || isProcessing"
      >
        🗑️ Clear
      </button>

      <div class="time-display">
        {{ formatTime(recordingTime) }}
      </div>
    </div>

    <!-- Waveform Visualization -->
    <div v-if="recordedChunks.length > 0" class="waveform-container">
      <div ref="waveformDiv" class="waveform"></div>
    </div>

    <!-- Transcription Display -->
    <div v-if="transcription" class="transcription-box">
      <h4>Transcription</h4>
      <p class="transcription-text">{{ transcription }}</p>
    </div>

    <!-- Error Display -->
    <div v-if="error" class="error-box">
      <p>{{ error }}</p>
      <button @click="error = null" class="btn btn-small">Dismiss</button>
    </div>

    <!-- Processing Indicator -->
    <div v-if="isProcessing" class="processing-indicator">
      <div class="spinner"></div>
      <p>Processing audio...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import WaveSurfer from 'wavesurfer.js'
import RecordRTC from 'recordrtc'

// State
const isRecording = ref(false)
const isProcessing = ref(false)
const recordedChunks = ref([])
const recordingTime = ref(0)
const transcription = ref('')
const error = ref('')
const waveformDiv = ref(null)

// Audio and recording
let mediaRecorder = null
let waveSurfer = null
let recordingInterval = null
let audioContext = null
let analyser = null
let mediaStream = null

const props = defineProps({
  backendUrl: {
    type: String,
    default: 'http://127.0.0.1:8000'
  }
})

const emit = defineEmits(['recording-complete', 'transcription-complete'])

// Initialize recording
const initializeRecording = async () => {
  try {
    mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder = new RecordRTC(mediaStream, {
      type: 'audio',
      mimeType: 'audio/wav',
      sampleRate: 44100,
      numberOfAudioChannels: 1,
      recorderType: RecordRTC.StereoAudioRecorder,
      timeSlice: 100,
      ondataavailable: (blob) => {
        recordedChunks.value.push(blob)
      }
    })
  } catch (err) {
    error.value = 'Microphone access denied. Please allow microphone access.'
    console.error('Error accessing microphone:', err)
  }
}

// Toggle recording
const toggleRecording = async () => {
  if (!mediaRecorder) {
    await initializeRecording()
  }

  if (!isRecording.value) {
    // Start recording
    recordedChunks.value = []
    recordingTime.value = 0
    transcription.value = ''
    error.value = ''

    mediaRecorder.startRecording()
    isRecording.value = true

    recordingInterval = setInterval(() => {
      recordingTime.value++
    }, 1000)
  } else {
    // Stop recording
    isRecording.value = false
    clearInterval(recordingInterval)

    mediaRecorder.stopRecording(async (blob) => {
      await processRecording(blob)
    })
  }
}

// Process recorded audio
const processRecording = async (blob) => {
  try {
    // Update waveform
    updateWaveform(blob)

    // Emit the recorded audio
    emit('recording-complete', blob)

    // Auto-transcribe
    await transcribeAudio(blob)
  } catch (err) {
    error.value = 'Error processing recording'
    console.error(err)
  }
}

// Update waveform visualization
const updateWaveform = (blob) => {
  if (!waveformDiv.value) return

  if (!waveSurfer) {
    waveSurfer = WaveSurfer.create({
      container: waveformDiv.value,
      waveColor: '#3b82f6',
      progressColor: '#1e40af',
      height: 60,
      responsive: true
    })
  }

  const url = URL.createObjectURL(blob)
  waveSurfer.load(url)
}

// Transcribe audio
const transcribeAudio = async (blob) => {
  try {
    isProcessing.value = true
    error.value = ''

    const formData = new FormData()
    formData.append('file', blob, 'audio.wav')

    const response = await fetch(`${props.backendUrl}/voice/transcribe`, {
      method: 'POST',
      body: formData
    })

    const data = await response.json()

    if (response.ok && data.success) {
      transcription.value = data.transcription
      emit('transcription-complete', data.transcription)
    } else {
      error.value = data.message || 'Failed to transcribe audio'
    }
  } catch (err) {
    error.value = 'Error transcribing audio'
    console.error(err)
  } finally {
    isProcessing.value = false
  }
}

// Clear recording
const clearRecording = () => {
  recordedChunks.value = []
  recordingTime.value = 0
  transcription.value = ''
  error.value = ''

  if (waveSurfer) {
    waveSurfer.destroy()
    waveSurfer = null
  }
}

// Format time display
const formatTime = (seconds) => {
  const hrs = Math.floor(seconds / 3600)
  const mins = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60

  if (hrs > 0) {
    return `${hrs}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// Cleanup on unmount
onUnmounted(() => {
  if (recordingInterval) clearInterval(recordingInterval)
  if (mediaStream) {
    mediaStream.getTracks().forEach(track => track.stop())
  }
  if (waveSurfer) {
    waveSurfer.destroy()
  }
  if (mediaRecorder) {
    try {
      mediaRecorder.stopRecording()
    } catch (e) {
      // Already stopped
    }
  }
})

onMounted(async () => {
  await initializeRecording()
})
</script>

<style scoped>
.audio-recorder {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 20px;
  color: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.recorder-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
  padding-bottom: 12px;
}

.recorder-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.recording-status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.875rem;
  color: #e0e7ff;
}

.recording-status.recording {
  color: #fecaca;
  font-weight: 600;
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 50% {
    opacity: 1;
  }
  51%, 100% {
    opacity: 0.5;
  }
}

.recorder-controls {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #10b981;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #059669;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.4);
}

.btn-secondary {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background-color: rgba(255, 255, 255, 0.3);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-small {
  padding: 4px 12px;
  font-size: 0.75rem;
}

.time-display {
  margin-left: auto;
  font-size: 1rem;
  font-weight: 600;
  font-family: 'Courier New', monospace;
  background: rgba(255, 255, 255, 0.1);
  padding: 8px 12px;
  border-radius: 6px;
  min-width: 80px;
  text-align: right;
}

.waveform-container {
  margin-bottom: 20px;
  background: rgba(0, 0, 0, 0.2);
  padding: 12px;
  border-radius: 8px;
}

.waveform {
  width: 100%;
}

.transcription-box {
  background: rgba(0, 0, 0, 0.2);
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 12px;
}

.transcription-box h4 {
  margin: 0 0 8px 0;
  font-size: 0.875rem;
  color: #e0e7ff;
}

.transcription-text {
  margin: 0;
  font-size: 0.9375rem;
  line-height: 1.5;
  color: #ffffff;
}

.error-box {
  background-color: #fee2e2;
  color: #991b1b;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 12px;
}

.error-box p {
  margin: 0 0 8px 0;
  font-size: 0.875rem;
}

.processing-indicator {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(0, 0, 0, 0.2);
  padding: 12px;
  border-radius: 8px;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.processing-indicator p {
  margin: 0;
  font-size: 0.875rem;
}
</style>
