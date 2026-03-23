<template>
  <div class="voice-playback">
    <div class="playback-header">
      <h3>Voice Playback</h3>
      <span v-if="isPlaying" class="playing-indicator">🔊 Playing...</span>
    </div>

    <div v-if="audioUrl" class="playback-controls">
      <button
        @click="togglePlayback"
        class="btn btn-primary"
        :disabled="isLoading"
      >
        <span v-if="!isPlaying">▶️ Play</span>
        <span v-else>⏸️ Pause</span>
      </button>

      <div class="volume-control">
        <span class="label">Volume:</span>
        <input
          v-model="volume"
          @input="updateVolume"
          type="range"
          min="0"
          max="100"
          class="slider"
        />
        <span class="volume-value">{{ volume }}%</span>
      </div>

      <div class="time-info">
        {{ formatTime(currentTime) }} / {{ formatTime(duration) }}
      </div>
    </div>

    <!-- Waveform Visualization -->
    <div v-if="audioUrl" class="waveform-container">
      <div ref="playbackWaveform" class="waveform"></div>
      <div class="progress-bar-container">
        <div class="progress-bar" :style="{ width: progressPercent + '%' }"></div>
        <input
          @click="seek"
          type="range"
          min="0"
          max="100"
          :value="progressPercent"
          class="progress-slider"
        />
      </div>
    </div>

    <!-- Audio Element (hidden) -->
    <audio
      ref="audioElement"
      @play="isPlaying = true"
      @pause="isPlaying = false"
      @ended="onAudioEnded"
      @timeupdate="updateTime"
      @loadedmetadata="onMetadata"
      @error="onAudioError"
      class="hidden-audio"
    ></audio>

    <!-- Loading Indicator -->
    <div v-if="isLoading" class="loading-indicator">
      <div class="spinner"></div>
      <p>Loading audio...</p>
    </div>

    <!-- Error Display -->
    <div v-if="error" class="error-box">
      <p>{{ error }}</p>
      <button @click="error = null" class="btn btn-small">Dismiss</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import WaveSurfer from 'wavesurfer.js'

// State
const isPlaying = ref(false)
const isLoading = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const volume = ref(80)
const error = ref('')

// Refs
const audioElement = ref(null)
const playbackWaveform = ref(null)
let waveSurfer = null

const props = defineProps({
  audioUrl: {
    type: String,
    required: false
  },
  autoPlay: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['playback-ended', 'error'])

// Computed properties
const progressPercent = computed(() => {
  if (!duration.value) return 0
  return (currentTime.value / duration.value) * 100
})

// Load audio
const loadAudio = async (url) => {
  if (!url) return

  try {
    isLoading.value = true
    error.value = ''

    // Set audio source
    if (audioElement.value) {
      audioElement.value.src = url

      // Preload audio
      await new Promise((resolve) => {
        const onCanPlay = () => {
          audioElement.value.removeEventListener('canplay', onCanPlay)
          resolve()
        }
        audioElement.value.addEventListener('canplay', onCanPlay, { once: true })
        audioElement.value.load()
      })

      // Initialize waveform if available
      if (playbackWaveform.value && !waveSurfer) {
        waveSurfer = WaveSurfer.create({
          container: playbackWaveform.value,
          waveColor: '#3b82f6',
          progressColor: '#1e40af',
          height: 60,
          responsive: true,
          url: url
        })

        waveSurfer.on('timeupdate', (time) => {
          currentTime.value = time
        })
      }

      if (props.autoPlay) {
        setTimeout(() => play(), 100)
      }
    }
  } catch (err) {
    error.value = 'Failed to load audio'
    emit('error', err)
    console.error('Audio loading error:', err)
  } finally {
    isLoading.value = false
  }
}

// Playback control
const togglePlayback = () => {
  if (!audioElement.value) return

  if (isPlaying.value) {
    audioElement.value.pause()
  } else {
    audioElement.value.play().catch((err) => {
      error.value = 'Failed to play audio'
      console.error(err)
    })
  }
}

const play = () => {
  if (audioElement.value) {
    audioElement.value.play()
  }
}

const pause = () => {
  if (audioElement.value) {
    audioElement.value.pause()
  }
}

// Update volume
const updateVolume = () => {
  if (audioElement.value) {
    audioElement.value.volume = volume.value / 100
  }
}

// Seek to position
const seek = (event) => {
  if (!audioElement.value || !duration.value) return

  const percent = (event.target.value / 100)
  audioElement.value.currentTime = percent * duration.value
}

// Format time
const formatTime = (seconds) => {
  if (!isFinite(seconds)) return '0:00'

  const hrs = Math.floor(seconds / 3600)
  const mins = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)

  if (hrs > 0) {
    return `${hrs}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// Event handlers
const updateTime = () => {
  if (audioElement.value) {
    currentTime.value = audioElement.value.currentTime
  }
}

const onMetadata = () => {
  if (audioElement.value) {
    duration.value = audioElement.value.duration
  }
}

const onAudioEnded = () => {
  isPlaying.value = false
  emit('playback-ended')
}

const onAudioError = (event) => {
  error.value = 'Error playing audio'
  emit('error', event)
  console.error('Audio error:', event)
}

// Cleanup
onUnmounted(() => {
  if (audioElement.value) {
    audioElement.value.pause()
    audioElement.value.src = ''
  }
  if (waveSurfer) {
    waveSurfer.destroy()
  }
})

onMounted(() => {
  if (props.audioUrl) {
    loadAudio(props.audioUrl)
  }

  // Set initial volume
  if (audioElement.value) {
    audioElement.value.volume = volume.value / 100
  }
})

// Expose methods
defineExpose({
  loadAudio,
  play,
  pause,
  togglePlayback,
  seek
})
</script>

<style scoped>
.voice-playback {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 20px;
  color: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.playback-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
  padding-bottom: 12px;
}

.playback-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.playing-indicator {
  font-size: 0.875rem;
  color: #86efac;
  font-weight: 600;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

.playback-controls {
  display: flex;
  gap: 15px;
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

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-small {
  padding: 4px 12px;
  font-size: 0.75rem;
}

.volume-control {
  display: flex;
  align-items: center;
  gap: 8px;
}

.label {
  font-size: 0.875rem;
  white-space: nowrap;
}

.slider {
  width: 100px;
  height: 4px;
  -webkit-appearance: none;
  appearance: none;
  background: rgba(255, 255, 255, 0.3);
  outline: none;
  border-radius: 2px;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 14px;
  height: 14px;
  background: white;
  cursor: pointer;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.slider::-moz-range-thumb {
  width: 14px;
  height: 14px;
  background: white;
  cursor: pointer;
  border-radius: 50%;
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.volume-value {
  font-size: 0.875rem;
  min-width: 40px;
  text-align: right;
}

.time-info {
  margin-left: auto;
  font-size: 0.875rem;
  font-family: 'Courier New', monospace;
  background: rgba(255, 255, 255, 0.1);
  padding: 6px 10px;
  border-radius: 6px;
  white-space: nowrap;
}

.waveform-container {
  margin-bottom: 20px;
  background: rgba(0, 0, 0, 0.2);
  padding: 12px;
  border-radius: 8px;
}

.waveform {
  width: 100%;
  margin-bottom: 12px;
}

.progress-bar-container {
  position: relative;
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #10b981, #6366f1);
  transition: width 0.1s linear;
  pointer-events: none;
}

.progress-slider {
  position: absolute;
  top: 50%;
  left: 0;
  width: 100%;
  height: 20px;
  transform: translateY(-50%);
  -webkit-appearance: none;
  appearance: none;
  background: transparent;
  outline: none;
  cursor: pointer;
  z-index: 5;
}

.progress-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 12px;
  height: 12px;
  background: white;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.progress-slider::-moz-range-thumb {
  width: 12px;
  height: 12px;
  background: white;
  border-radius: 50%;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.loading-indicator {
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

.loading-indicator p {
  margin: 0;
  font-size: 0.875rem;
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

.hidden-audio {
  display: none;
}
</style>
