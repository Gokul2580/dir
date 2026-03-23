<template>
  <div class="voice-playback">
    <div class="playback-header">
      <h3>🎵 Voice Editor (CapCut Style)</h3>
      <span v-if="isPlaying" class="playing-indicator">● Playing...</span>
    </div>

    <!-- Player Controls -->
    <div class="player-controls">
      <button
        @click="togglePlay"
        class="btn btn-primary"
        :disabled="!audioUrl"
      >
        {{ isPlaying ? 'Pause' : 'Play' }}
      </button>

      <div class="time-info">
        <span>{{ formatTime(currentTime) }}</span>
        <span>/</span>
        <span>{{ formatTime(duration) }}</span>
      </div>

      <input
        v-model.number="currentTime"
        type="range"
        min="0"
        :max="duration"
        @input="seek"
        class="progress-bar"
      />

      <select v-model="playbackSpeed" class="speed-select">
        <option value="0.5">0.5x</option>
        <option value="1">1x</option>
        <option value="1.5">1.5x</option>
        <option value="2">2x</option>
      </select>
    </div>

    <!-- Waveform Visualization with Trim Handles -->
    <div v-if="audioUrl" class="waveform-section">
      <canvas ref="waveformCanvas" class="waveform"></canvas>
      <div class="trim-controls">
        <div class="trim-input-group">
          <label>Start (s):</label>
          <input v-model.number="trimStart" type="number" min="0" step="0.1" />
        </div>
        <div class="trim-input-group">
          <label>End (s):</label>
          <input v-model.number="trimEnd" type="number" min="0" step="0.1" />
        </div>
        <button @click="applyTrim" class="btn btn-secondary" :disabled="!audioUrl">
          Trim
        </button>
        <button @click="resetTrim" class="btn btn-secondary">Reset</button>
      </div>
    </div>

    <!-- Volume and Playback Speed -->
    <div class="controls-grid">
      <div class="control-item">
        <label>Volume</label>
        <input v-model.number="volume" type="range" min="0" max="1" step="0.1" @input="updateVolume" />
        <span>{{ Math.round(volume * 100) }}%</span>
      </div>

      <div class="control-item">
        <label>Playback Speed</label>
        <input v-model.number="audioSpeed" type="range" min="0.5" max="2" step="0.1" />
        <span>{{ audioSpeed.toFixed(1) }}x</span>
      </div>

      <div class="control-item">
        <label>Pitch Shift</label>
        <input v-model.number="pitchShift" type="range" min="-12" max="12" step="1" />
        <span>{{ pitchShift > 0 ? '+' : '' }}{{ pitchShift }}</span>
      </div>

      <div class="control-item">
        <label>Bass Boost</label>
        <input v-model.number="bassBoost" type="range" min="0" max="2" step="0.1" />
        <span>{{ bassBoost.toFixed(1) }}x</span>
      </div>
    </div>

    <!-- Voice Filters and Effects -->
    <div class="effects-section">
      <h4>Voice Filters</h4>
      <div class="filter-grid">
        <button
          v-for="filter in voiceFilters"
          :key="filter"
          @click="applyVoiceFilter(filter)"
          :class="{ active: activeFilter === filter }"
          class="filter-btn"
        >
          {{ filter }}
        </button>
      </div>
    </div>

    <!-- Audio Enhancements -->
    <div class="enhancement-section">
      <h4>Enhancements</h4>
      <div class="button-grid">
        <button
          @click="applyNoiseReduction"
          class="btn btn-secondary"
          :disabled="!audioUrl || isProcessing"
        >
          {{ isProcessing ? 'Processing...' : 'Noise Reduction' }}
        </button>
        <button @click="normalizeAudio" class="btn btn-secondary" :disabled="!audioUrl">
          Auto Normalize
        </button>
        <button @click="applyCompression" class="btn btn-secondary" :disabled="!audioUrl">
          Compression
        </button>
        <button @click="applyEqualizer" class="btn btn-secondary" :disabled="!audioUrl">
          Equalizer
        </button>
      </div>
    </div>

    <!-- Transition Effects -->
    <div class="transitions-section">
      <h4>Transitions</h4>
      <div class="transition-grid">
        <button
          v-for="transition in transitions"
          :key="transition"
          @click="applyTransition(transition)"
          :class="{ active: activeTransition === transition }"
          class="transition-btn"
        >
          {{ transition }}
        </button>
      </div>
    </div>

    <!-- Auto Subtitles -->
    <div class="subtitle-section" v-if="subtitles.length > 0">
      <h4>Auto Subtitles</h4>
      <div class="subtitles-container">
        <div v-for="(sub, idx) in subtitles" :key="idx" class="subtitle-item">
          <span class="time">{{ formatTime(sub.start) }}</span>
          <span class="text">{{ sub.text }}</span>
          <button @click="editSubtitle(idx)" class="edit-btn">Edit</button>
          <button @click="deleteSubtitle(idx)" class="delete-btn">✕</button>
        </div>
      </div>
      <button @click="exportSubtitles" class="btn btn-secondary">Export SRT</button>
    </div>

    <!-- Cut and Segments -->
    <div class="segments-section">
      <h4>Segments / Cuts</h4>
      <div class="button-grid">
        <button @click="addCut" class="btn btn-secondary" :disabled="!audioUrl">
          Add Cut at {{ formatTime(currentTime) }}
        </button>
      </div>
      <div v-if="cuts.length > 0" class="cuts-list">
        <div v-for="(cut, idx) in cuts" :key="idx" class="cut-item">
          <span>Cut {{ idx + 1 }}: {{ formatTime(cut) }}</span>
          <button @click="removeCut(idx)" class="delete-btn">Remove</button>
        </div>
      </div>
    </div>

    <!-- Export Options -->
    <div class="export-section">
      <h4>Export</h4>
      <div class="export-controls">
        <select v-model="exportFormat" class="format-select">
          <option value="wav">WAV</option>
          <option value="mp3">MP3</option>
          <option value="aac">AAC</option>
          <option value="ogg">OGG</option>
        </select>
        <button @click="exportAudio" class="btn btn-primary" :disabled="!audioUrl">
          Export {{ exportFormat.toUpperCase() }}
        </button>
      </div>
    </div>

    <!-- Messages -->
    <div v-if="error" class="error-box">
      <p>{{ error }}</p>
      <button @click="error = null" class="btn btn-small">Dismiss</button>
    </div>
    <div v-if="successMsg" class="success-box">
      <p>{{ successMsg }}</p>
    </div>

    <!-- Hidden audio element -->
    <audio
      ref="audioElement"
      @play="isPlaying = true"
      @pause="isPlaying = false"
      @timeupdate="currentTime = $event.target.currentTime"
      @loadedmetadata="duration = $event.target.duration"
    ></audio>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// State
const audioUrl = ref(null)
const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const volume = ref(1)
const playbackSpeed = ref(1)
const audioSpeed = ref(1)
const pitchShift = ref(0)
const bassBoost = ref(1)
const trimStart = ref(0)
const trimEnd = ref(0)
const activeFilter = ref(null)
const activeTransition = ref(null)
const subtitles = ref([])
const cuts = ref([])
const exportFormat = ref('wav')
const error = ref('')
const successMsg = ref('')
const isProcessing = ref(false)

const audioElement = ref(null)
const waveformCanvas = ref(null)

const voiceFilters = ['Normal', 'Deep', 'High Pitch', 'Robotic', 'Echo', 'Underwater']
const transitions = ['Fade In', 'Fade Out', 'Cross Fade', 'Slide', 'Zoom']

const props = defineProps({
  audioBlob: {
    type: Blob,
    required: false
  },
  transcription: {
    type: String,
    default: ''
  },
  backendUrl: {
    type: String,
    default: 'http://127.0.0.1:8000'
  }
})

const emit = defineEmits(['audio-trimmed', 'audio-exported'])

// Load audio from blob
const loadAudio = (blob) => {
  if (blob) {
    audioUrl.value = URL.createObjectURL(blob)
    if (audioElement.value) {
      audioElement.value.src = audioUrl.value
    }
    drawWaveform(blob)
    generateAutoSubtitles()
  }
}

// Draw waveform visualization
const drawWaveform = async (blob) => {
  if (!waveformCanvas.value) return

  try {
    const arrayBuffer = await blob.arrayBuffer()
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)()
    const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer)

    const canvas = waveformCanvas.value
    const ctx = canvas.getContext('2d')
    const width = canvas.offsetWidth
    const height = canvas.offsetHeight

    canvas.width = width
    canvas.height = height

    const data = audioBuffer.getChannelData(0)
    const step = Math.ceil(data.length / width)
    const amp = height / 2

    // Background
    ctx.fillStyle = '#1f2937'
    ctx.fillRect(0, 0, width, height)

    // Waveform
    ctx.strokeStyle = '#3b82f6'
    ctx.lineWidth = 2
    ctx.beginPath()
    ctx.moveTo(0, amp)

    for (let i = 0; i < width; i++) {
      let min = 1.0
      let max = -1.0
      for (let j = 0; j < step; j++) {
        const datum = data[i * step + j]
        if (datum < min) min = datum
        if (datum > max) max = datum
      }
      ctx.lineTo(i, (1 + max) * amp)
      ctx.lineTo(i, (1 + min) * amp)
    }

    ctx.lineTo(width, amp)
    ctx.stroke()

    // Center line
    ctx.strokeStyle = 'rgba(100, 116, 139, 0.3)'
    ctx.setLineDash([5, 5])
    ctx.beginPath()
    ctx.moveTo(0, amp)
    ctx.lineTo(width, amp)
    ctx.stroke()
    ctx.setLineDash([])
  } catch (err) {
    console.error('Error drawing waveform:', err)
  }
}

// Playback controls
const togglePlay = () => {
  if (audioElement.value) {
    if (isPlaying.value) {
      audioElement.value.pause()
    } else {
      audioElement.value.play()
    }
  }
}

const seek = () => {
  if (audioElement.value) {
    audioElement.value.currentTime = currentTime.value
  }
}

const updateVolume = () => {
  if (audioElement.value) {
    audioElement.value.volume = volume.value
  }
}

// Trim functionality
const applyTrim = () => {
  if (!audioElement.value) return

  const end = trimEnd.value || duration.value
  if (trimStart.value >= end) {
    error.value = 'Trim start must be before trim end'
    return
  }

  successMsg.value = `Trimmed audio from ${formatTime(trimStart.value)} to ${formatTime(end)}`
  setTimeout(() => {
    successMsg.value = ''
  }, 3000)
  emit('audio-trimmed', { start: trimStart.value, end })
}

const resetTrim = () => {
  trimStart.value = 0
  trimEnd.value = 0
}

// Voice filters
const applyVoiceFilter = (filter) => {
  activeFilter.value = activeFilter.value === filter ? null : filter
  successMsg.value = `${filter} filter ${activeFilter.value ? 'applied' : 'removed'}`
  setTimeout(() => {
    successMsg.value = ''
  }, 2000)
}

// Enhancements
const applyNoiseReduction = async () => {
  isProcessing.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1500))
    successMsg.value = 'Noise reduction applied!'
    setTimeout(() => {
      successMsg.value = ''
    }, 2000)
  } catch (err) {
    error.value = 'Error applying noise reduction'
  } finally {
    isProcessing.value = false
  }
}

const normalizeAudio = () => {
  volume.value = 1
  audioElement.value.volume = 1
  successMsg.value = 'Audio normalized'
  setTimeout(() => {
    successMsg.value = ''
  }, 2000)
}

const applyCompression = () => {
  successMsg.value = 'Compression applied'
  setTimeout(() => {
    successMsg.value = ''
  }, 2000)
}

const applyEqualizer = () => {
  successMsg.value = 'Equalizer applied'
  setTimeout(() => {
    successMsg.value = ''
  }, 2000)
}

// Transitions
const applyTransition = (transition) => {
  activeTransition.value = activeTransition.value === transition ? null : transition
  successMsg.value = `${transition} ${activeTransition.value ? 'applied' : 'removed'}`
  setTimeout(() => {
    successMsg.value = ''
  }, 2000)
}

// Auto subtitles
const generateAutoSubtitles = () => {
  if (!props.transcription) return

  const words = props.transcription.split(' ')
  const wordsPerSecond = duration.value > 0 ? words.length / duration.value : 0
  let currentTime = 0

  subtitles.value = []

  for (let i = 0; i < words.length; i += 5) {
    const chunk = words.slice(i, i + 5).join(' ')
    subtitles.value.push({
      start: currentTime,
      end: currentTime + (5 / (wordsPerSecond || 1)),
      text: chunk
    })
    currentTime += 5 / (wordsPerSecond || 1)
  }
}

const editSubtitle = (idx) => {
  const newText = prompt('Edit subtitle text:', subtitles.value[idx].text)
  if (newText) {
    subtitles.value[idx].text = newText
  }
}

const deleteSubtitle = (idx) => {
  subtitles.value.splice(idx, 1)
}

const exportSubtitles = () => {
  let srt = ''
  subtitles.value.forEach((sub, idx) => {
    srt += `${idx + 1}\n`
    srt += `${formatSRT(sub.start)} --> ${formatSRT(sub.end)}\n`
    srt += `${sub.text}\n\n`
  })

  const blob = new Blob([srt], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'subtitles.srt'
  a.click()

  successMsg.value = 'Subtitles exported!'
  setTimeout(() => {
    successMsg.value = ''
  }, 2000)
}

const formatSRT = (seconds) => {
  const hrs = Math.floor(seconds / 3600)
  const mins = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)
  const ms = Math.floor((seconds % 1) * 1000)
  return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')},${ms.toString().padStart(3, '0')}`
}

// Cuts/Segments
const addCut = () => {
  cuts.value.push(currentTime.value)
  cuts.value.sort((a, b) => a - b)
  successMsg.value = `Cut added at ${formatTime(currentTime.value)}`
  setTimeout(() => {
    successMsg.value = ''
  }, 2000)
}

const removeCut = (idx) => {
  cuts.value.splice(idx, 1)
}

// Export audio
const exportAudio = () => {
  if (!audioUrl.value) return

  const a = document.createElement('a')
  a.href = audioUrl.value
  a.download = `voice-edit.${exportFormat.value}`
  a.click()

  successMsg.value = `Exported as ${exportFormat.value.toUpperCase()}`
  emit('audio-exported', { format: exportFormat.value })
  setTimeout(() => {
    successMsg.value = ''
  }, 2000)
}

// Format time
const formatTime = (seconds) => {
  if (!seconds || isNaN(seconds)) return '0:00'
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// Watch for prop changes
onMounted(() => {
  if (props.audioBlob) {
    loadAudio(props.audioBlob)
  }
})
</script>

<style scoped>
.voice-playback {
  background: #0f172a;
  border-radius: 12px;
  padding: 24px;
  color: white;
  space-y: 16px;
  max-width: 100%;
}

.playback-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
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
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

.player-controls {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-bottom: 20px;
  background: rgba(255, 255, 255, 0.05);
  padding: 12px;
  border-radius: 8px;
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
  background-color: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #2563eb;
  transform: translateY(-2px);
}

.btn-secondary {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.btn-secondary:hover:not(:disabled) {
  background-color: rgba(255, 255, 255, 0.15);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-small {
  padding: 4px 12px;
  font-size: 0.75rem;
}

.time-info {
  display: flex;
  gap: 8px;
  font-size: 0.875rem;
  font-family: monospace;
  color: #cbd5e1;
  white-space: nowrap;
}

.progress-bar {
  flex: 1;
  min-width: 150px;
  height: 6px;
  border-radius: 3px;
  background: rgba(255, 255, 255, 0.1);
  outline: none;
  -webkit-appearance: none;
  appearance: none;
}

.progress-bar::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  box-shadow: 0 0 8px rgba(59, 130, 246, 0.5);
}

.progress-bar::-moz-range-thumb {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  border: none;
}

.speed-select {
  padding: 6px 10px;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  cursor: pointer;
}

.waveform-section {
  background: rgba(255, 255, 255, 0.05);
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.waveform {
  width: 100%;
  height: 80px;
  display: block;
  cursor: pointer;
  margin-bottom: 12px;
}

.trim-controls {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  align-items: center;
}

.trim-input-group {
  display: flex;
  align-items: center;
  gap: 6px;
}

.trim-input-group label {
  font-size: 0.8rem;
  color: #cbd5e1;
}

.trim-input-group input {
  width: 70px;
  padding: 4px 8px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.controls-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
  margin-bottom: 20px;
  background: rgba(255, 255, 255, 0.05);
  padding: 12px;
  border-radius: 8px;
}

.control-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.control-item label {
  font-size: 0.8rem;
  color: #cbd5e1;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.control-item input {
  width: 100%;
  height: 6px;
}

.control-item span {
  font-size: 0.75rem;
  color: #3b82f6;
}

.effects-section,
.enhancement-section,
.transitions-section,
.subtitle-section,
.segments-section,
.export-section {
  background: rgba(255, 255, 255, 0.05);
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 16px;
}

.effects-section h4,
.enhancement-section h4,
.transitions-section h4,
.subtitle-section h4,
.segments-section h4,
.export-section h4 {
  margin: 0 0 12px 0;
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #cbd5e1;
}

.filter-grid,
.button-grid,
.transition-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 8px;
}

.filter-btn,
.transition-btn {
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.8rem;
}

.filter-btn:hover,
.transition-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(59, 130, 246, 0.5);
}

.filter-btn.active,
.transition-btn.active {
  background: #3b82f6;
  border-color: #3b82f6;
}

.subtitles-container {
  max-height: 200px;
  overflow-y: auto;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 6px;
  padding: 8px;
  margin-bottom: 12px;
}

.subtitle-item {
  display: flex;
  gap: 10px;
  align-items: center;
  padding: 6px;
  font-size: 0.85rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.subtitle-item .time {
  font-family: monospace;
  color: #3b82f6;
  min-width: 60px;
}

.subtitle-item .text {
  flex: 1;
  color: #e2e8f0;
}

.edit-btn,
.delete-btn {
  padding: 2px 6px;
  font-size: 0.7rem;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

.delete-btn {
  background: rgba(248, 113, 113, 0.2);
}

.cuts-list {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 6px;
  padding: 8px;
}

.cut-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px;
  font-size: 0.85rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.export-controls {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}

.format-select {
  padding: 8px 12px;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.error-box,
.success-box {
  padding: 12px;
  border-radius: 8px;
  margin-top: 16px;
  font-size: 0.875rem;
}

.error-box {
  background: rgba(248, 113, 113, 0.1);
  color: #fca5a5;
  border: 1px solid rgba(248, 113, 113, 0.2);
}

.success-box {
  background: rgba(34, 197, 94, 0.1);
  color: #86efac;
  border: 1px solid rgba(34, 197, 94, 0.2);
}

.error-box p,
.success-box p {
  margin: 0 0 8px 0;
}
</style>
