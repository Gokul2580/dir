import logging
import os
from typing import Optional
from director.agents.base import BaseAgent, AgentResponse, AgentStatus
from director.core.session import TextContent, MsgStatus
from openai import OpenAI

logger = logging.getLogger(__name__)


class VoiceChatAgent(BaseAgent):
    """Agent for handling voice chat interactions with speech-to-text and text-to-speech capabilities."""

    def __init__(self, session=None, **kwargs):
        self.agent_name = "voice_chat"
        self.description = (
            "This agent handles voice chat conversations with speech-to-text transcription "
            "and text-to-speech response generation. It converts audio input to text, processes "
            "the conversation, and generates audio responses."
        )
        self.parameters = self.get_parameters()
        super().__init__(session=session, **kwargs)
        
        # Initialize OpenAI client for Whisper and TTS
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

    def run(
        self,
        audio_input: Optional[bytes] = None,
        audio_file_path: Optional[str] = None,
        generate_speech_response: bool = True,
        response_text: Optional[str] = None,
        voice_id: str = "default"
    ) -> AgentResponse:
        """
        Process voice chat input and generate response.

        :param bytes audio_input: Raw audio bytes (WAV, MP3, OGG format)
        :param str audio_file_path: Path to audio file if using file instead of bytes
        :param bool generate_speech_response: Whether to generate speech response or just transcribe
        :param str response_text: Pre-generated response text to convert to speech
        :param str voice_id: Voice ID for text-to-speech (ElevenLabs)
        :return: AgentResponse with transcription and optional audio response
        :rtype: AgentResponse
        """
        try:
            self.output_message.actions.append("Processing voice input...")
            output_text_content = TextContent(
                agent_name=self.agent_name,
                status_message="Processing voice chat...",
            )
            self.output_message.content.append(output_text_content)
            self.output_message.push_update()

            # Step 1: Convert speech to text using Whisper
            transcription_text = self._transcribe_audio(audio_input, audio_file_path)
            
            if not transcription_text:
                return AgentResponse(
                    status=AgentStatus.ERROR,
                    message="Failed to transcribe audio",
                )

            # Step 2: Generate response (if provided or needed)
            audio_response_url = None
            if generate_speech_response and response_text:
                self.output_message.actions.append("Generating voice response...")
                self.output_message.push_update()
                
                audio_response_url = self._generate_speech(response_text, voice_id)
                
                if not audio_response_url:
                    logger.warning("Failed to generate speech response")

            output_text_content.text = f"Transcribed: {transcription_text}"
            output_text_content.status = MsgStatus.success
            output_text_content.status_message = "Voice processing complete"
            self.output_message.publish()

            return AgentResponse(
                status=AgentStatus.SUCCESS,
                message="Voice chat processed successfully",
                data={
                    "transcription": transcription_text,
                    "audio_response_url": audio_response_url,
                    "voice_id": voice_id,
                },
            )

        except Exception as e:
            logger.exception(f"Error in {self.agent_name} agent: {e}")
            return AgentResponse(
                status=AgentStatus.ERROR,
                message=f"Voice processing error: {str(e)}",
            )

    def _transcribe_audio(
        self,
        audio_input: Optional[bytes] = None,
        audio_file_path: Optional[str] = None
    ) -> Optional[str]:
        """
        Convert audio to text using OpenAI's Whisper API.

        :param bytes audio_input: Raw audio bytes
        :param str audio_file_path: Path to audio file
        :return: Transcribed text or None if failed
        :rtype: Optional[str]
        """
        try:
            if audio_file_path:
                # Read from file
                with open(audio_file_path, "rb") as audio_file:
                    transcript = self.openai_client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        language="en"
                    )
            elif audio_input:
                # Use provided bytes
                from io import BytesIO
                audio_file = BytesIO(audio_input)
                audio_file.name = "audio.wav"
                transcript = self.openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en"
                )
            else:
                logger.error("No audio input or file path provided")
                return None

            return transcript.text.strip()

        except Exception as e:
            logger.exception(f"Transcription error: {e}")
            return None

    def _generate_speech(self, text: str, voice_id: str = "default") -> Optional[str]:
        """
        Generate speech from text using ElevenLabs or OpenAI TTS.

        :param str text: Text to convert to speech
        :param str voice_id: Voice ID for the speech
        :return: URL to generated audio file or None if failed
        :rtype: Optional[str]
        """
        try:
            if self.elevenlabs_api_key:
                return self._generate_speech_elevenlabs(text, voice_id)
            else:
                # Fall back to OpenAI TTS
                return self._generate_speech_openai(text)

        except Exception as e:
            logger.exception(f"Speech generation error: {e}")
            return None

    def _generate_speech_elevenlabs(self, text: str, voice_id: str) -> Optional[str]:
        """
        Generate speech using ElevenLabs API.

        :param str text: Text to convert to speech
        :param str voice_id: ElevenLabs voice ID
        :return: URL to audio or path to saved file
        :rtype: Optional[str]
        """
        try:
            import requests
            
            # Map voice_id to ElevenLabs voice ID
            voice_mapping = {
                "default": "21m00Tcm4TlvDq8ikWAM",  # Rachel
                "male": "EXAVITQu4vr4xnSDxMaL",     # Adam
                "female": "21m00Tcm4TlvDq8ikWAM",   # Rachel
            }
            
            elevenlabs_voice_id = voice_mapping.get(voice_id, voice_mapping["default"])
            
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{elevenlabs_voice_id}"
            headers = {
                "xi-api-key": self.elevenlabs_api_key,
                "Content-Type": "application/json",
            }
            
            payload = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75,
                },
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                # Save audio file locally
                audio_dir = "audio_responses"
                os.makedirs(audio_dir, exist_ok=True)
                
                import uuid
                filename = f"response_{uuid.uuid4()}.mp3"
                filepath = os.path.join(audio_dir, filename)
                
                with open(filepath, "wb") as f:
                    f.write(response.content)
                
                return filepath
            else:
                logger.error(f"ElevenLabs error: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.exception(f"ElevenLabs speech generation error: {e}")
            return None

    def _generate_speech_openai(self, text: str) -> Optional[str]:
        """
        Generate speech using OpenAI's TTS API.

        :param str text: Text to convert to speech
        :return: Path to saved audio file
        :rtype: Optional[str]
        """
        try:
            response = self.openai_client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text,
                speed=1.0,
            )
            
            # Save audio file locally
            audio_dir = "audio_responses"
            os.makedirs(audio_dir, exist_ok=True)
            
            import uuid
            filename = f"response_{uuid.uuid4()}.mp3"
            filepath = os.path.join(audio_dir, filename)
            
            response.stream_to_file(filepath)
            
            return filepath

        except Exception as e:
            logger.exception(f"OpenAI TTS error: {e}")
            return None
