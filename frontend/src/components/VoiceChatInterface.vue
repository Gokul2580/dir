<template>
  <div class="voice-chat-container">
    <header class="chat-header">
      <h1>Voice Chat Assistant</h1>
      <p class="subtitle">Talk to the AI with voice input and get spoken responses</p>
    </header>

    <main class="chat-main">
      <!-- Chat History -->
      <section class="chat-history" ref="chatHistoryContainer">
        <div v-if="chatHistory.length === 0" class="empty-state">
          <div class="empty-icon">🎤</div>
          <p>Start a voice conversation</p>
          <p class="text-sm">Record a message to begin chatting</p>
        </div>

        <div v-for="(message, idx) in chatHistory" :key="idx" class="message" :class="message.role">
          <div class="message-content">
            <div class="message-speaker">
              {{ message.role === 'user' ? 'You' : 'AI Assistant' }}
            </div>
            <div class="message-text">{{ message.text }}</div>
            <div v-if="message.audioUrl" class="message-audio">
              <VoicePlayback :audioUrl="message.audioUrl" />
            </div>
          </div>
        </div>

        <div v-if="isProcessing" class="message assistant">
          <div class="message-content">
            <div class="message-speaker">AI Assistant</div>
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </section>

      <!-- Recording and Settings -->
      <section class="chat-controls">
        <!-- Voice Settings -->
        <div class="settings-panel">
          <details class="settings-dropdown">
            <summary>⚙️ Settings</summary>
            <div class="settings-content">
              <div class="setting-group">
                <label>Response Voice:</label>
                <select v-model="selectedVoice" class="input-select">
                  <option value="default">Default (Rachel)</option>
                  <option value="male">Male (Adam)</option>
                  <option value="female">Female (Rachel)</option>
                </select>
              </div>

              <div class="setting-group">
                <label>Auto-transcribe:</label>
                <input v-model="autoTranscribe" type="checkbox" class="input-checkbox" />
              </div>

              <div class="setting-group">
                <label>Auto-play responses:</label>
                <input v-model="autoPlayResponse" type="checkbox" class="input-checkbox" />
              </div>

              <div class="setting-group">
                <label>Backend URL:</label>
                <input v-model="backendUrl" type="text" class="input-text" />
              </div>

              <button @click="clearHistory" class="btn btn-secondary btn-small">
                Clear History
              </button>
            </div>
          </details>
        </div>

        <!-- Audio Recorder -->
        <AudioRecorder
          :key="recorderKey"
          :backendUrl="backendUrl"
          @recording-complete="handleRecordingComplete"
          @transcription-complete="handleTranscriptionComplete"
        />

        <!-- Error Display -->
        <div v-if="error" class="error-box">
          <p>{{ error }}</p>
          <button @click="error = ''" class="btn btn-small">Dismiss</button>
        </div>

        <!-- Success Message -->
        <div v-if="successMessage" class="success-box">
          <p>{{ successMessage }}</p>
          <button @click="successMessage = ''" class="btn btn-small">Dismiss</button>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted } from 'vue'
import AudioRecorder from './AudioRecorder.vue'
import VoicePlayback from './VoicePlayback.vue'

// State
const chatHistory = ref([])
const selectedVoice = ref('default')
const autoTranscribe = ref(true)
const autoPlayResponse = ref(true)
const backendUrl = ref('http://127.0.0.1:8000')
const isProcessing = ref(false)
const error = ref('')
const successMessage = ref('')
const recorderKey = ref(0)
const chatHistoryContainer = ref(null)
const currentRecordingBlob = ref(null)
const currentChatId = ref(null)

// Initialize chat
const initializeChat = async () => {
  try {
    const chatId = `chat_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    currentChatId.value = chatId
    successMessage.value = 'New chat created'
    setTimeout(() => {
      successMessage.value = ''
    }, 2000)
  } catch (err) {
    error.value = 'Failed to initialize chat'
    console.error(err)
  }
}

// Send voice message to backend
const sendVoiceMessage = async (audioBlob, userTranscription) => {
  try {
    isProcessing.value = true
    error.value = ''

    // Use local blob URL
    const audioUrl = URL.createObjectURL(audioBlob)

    // Add user message to chat
    const userMessage = {
      role: 'user',
      text: userTranscription,
      audioUrl: audioUrl,
      timestamp: new Date().toISOString()
    }
    chatHistory.value.push(userMessage)

    // Scroll to bottom
    scrollToBottom()

    // Call the backend voice chat endpoint
    const formData = new FormData()
    formData.append('audio', audioBlob, 'user-audio.wav')
    formData.append('response_text', `Respond to this: ${userTranscription}`)
    formData.append('voice_id', selectedVoice.value)
    formData.append('generate_speech', 'true')

    const response = await fetch(`${backendUrl.value}/voice/chat`, {
      method: 'POST',
      body: formData
    })

    const data = await response.json()

    if (response.ok && data.success) {
      const responseData = data.data

      // Add AI response to chat
      const aiMessage = {
        role: 'assistant',
        text: responseData.transcription || 'Response processed',
        audioUrl: responseData.audio_response_url ? `${backendUrl.value}/${responseData.audio_response_url}` : null,
        timestamp: new Date().toISOString()
      }
      chatHistory.value.push(aiMessage)

      // Auto-play response if enabled
      if (autoPlayResponse.value && responseData.audio_response_url) {
        successMessage.value = 'Response received!'
        setTimeout(() => {
          successMessage.value = ''
        }, 3000)
      }

      scrollToBottom()
    } else {
      error.value = data.message || 'Failed to process voice message'
      // Remove the user message if backend failed
      chatHistory.value.pop()
    }
  } catch (err) {
    error.value = `Error: ${err.message}`
    console.error('Error sending voice message:', err)
    // Remove the user message if request failed
    chatHistory.value.pop()
  } finally {
    isProcessing.value = false
    recorderKey.value++
  }
}

// Handle recording complete
const handleRecordingComplete = (audioBlob) => {
  currentRecordingBlob.value = audioBlob
}

// Handle transcription complete
const handleTranscriptionComplete = (transcription) => {
  if (autoTranscribe.value && currentRecordingBlob.value) {
    sendVoiceMessage(currentRecordingBlob.value, transcription)
  }
}

// Clear chat history
const clearHistory = () => {
  if (confirm('Are you sure you want to clear all chat history?')) {
    chatHistory.value = []
    successMessage.value = 'Chat history cleared'
    setTimeout(() => {
      successMessage.value = ''
    }, 2000)
  }
}

// Scroll to bottom
const scrollToBottom = () => {
  nextTick(() => {
    if (chatHistoryContainer.value) {
      chatHistoryContainer.value.scrollTop = chatHistoryContainer.value.scrollHeight
    }
  })
}

// Initialize on mount
onMounted(() => {
  initializeChat()
})
</script>

<style scoped>
.voice-chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  color: #ffffff;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
}

.chat-header {
  padding: 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(0, 0, 0, 0.2);
}

.chat-header h1 {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 700;
}

.subtitle {
  margin: 8px 0 0 0;
  color: #a0a0a0;
  font-size: 0.95rem;
}

.chat-main {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
}

.chat-history {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
  color: #666666;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.empty-state p {
  margin: 4px 0;
  font-size: 0.95rem;
}

.text-sm {
  font-size: 0.85rem;
  color: #888888;
}

.message {
  display: flex;
  margin-bottom: 8px;
}

.message.user {
  justify-content: flex-end;
}

.message.user .message-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px 0 12px 12px;
}

.message.assistant .message-content {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0 12px 12px 12px;
}

.message-content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 12px;
}

.message-speaker {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 4px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.message-text {
  font-size: 0.95rem;
  line-height: 1.5;
  margin-bottom: 8px;
  word-wrap: break-word;
}

.message-audio {
  margin-top: 12px;
}

.typing-indicator {
  display: flex;
  gap: 4px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 50%;
  animation: bounce 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(1);
    opacity: 0.6;
  }
  40% {
    transform: scale(1.2);
    opacity: 1;
  }
}

.chat-controls {
  padding: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-height: 50vh;
  overflow-y: auto;
}

.settings-panel {
  margin-bottom: 12px;
}

.settings-dropdown {
  cursor: pointer;
  user-select: none;
  font-weight: 500;
}

.settings-dropdown summary {
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  transition: all 0.3s ease;
}

.settings-dropdown summary:hover {
  background: rgba(255, 255, 255, 0.15);
}

.settings-content {
  margin-top: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.setting-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.setting-group label {
  flex: 0 0 auto;
  min-width: 120px;
  font-size: 0.875rem;
}

.input-select,
.input-text {
  flex: 1;
  padding: 6px 10px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  color: white;
  font-size: 0.875rem;
}

.input-select:focus,
.input-text:focus {
  outline: none;
  border-color: #667eea;
  background: rgba(255, 255, 255, 0.15);
}

.input-checkbox {
  width: 18px;
  height: 18px;
  cursor: pointer;
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

.btn-secondary {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
}

.btn-secondary:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

.btn-small {
  padding: 4px 12px;
  font-size: 0.75rem;
}

.error-box {
  background-color: rgba(239, 68, 68, 0.2);
  border: 1px solid rgba(239, 68, 68, 0.5);
  color: #fca5a5;
  padding: 12px;
  border-radius: 8px;
}

.error-box p {
  margin: 0 0 8px 0;
  font-size: 0.875rem;
}

.success-box {
  background-color: rgba(34, 197, 94, 0.2);
  border: 1px solid rgba(34, 197, 94, 0.5);
  color: #86efac;
  padding: 12px;
  border-radius: 8px;
}

.success-box p {
  margin: 0 0 8px 0;
  font-size: 0.875rem;
}

/* Scrollbar styling */
.chat-history::-webkit-scrollbar {
  width: 8px;
}

.chat-history::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
}

.chat-history::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}

.chat-history::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}
</style>
