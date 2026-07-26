from pathlib import Path
import google.generativeai as genai
from core.config import settings
from core.logger import logger

class VoiceService:
    @staticmethod
    async def transcribe_and_respond(audio_path_str: str) -> dict:
        """
        Transcribe uploaded audio file using Gemini API, and optionally provide a response to questions.
        """
        abs_path = settings.get_absolute_path(audio_path_str)
        if not abs_path.exists():
            return {"text": "Error: Audio file not found.", "reply": "No file found."}

        if "YOUR_GEMINI_API_KEY" in settings.GEMINI_API_KEY or not settings.GEMINI_API_KEY:
            logger.warning("Gemini API key is not configured. Returning Mock Voice Transcription.")
            return {
                "text": "Check my heart rate and cholesterol levels.",
                "reply": "Mock Voice Reply: To assess your metrics, please upload a recent lab report or view your vitals tab."
            }

        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            
            # Use gemini-1.5-flash for audio files
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            # Read audio bytes
            with open(abs_path, "rb") as f:
                audio_data = f.read()
                
            # Create standard upload format structure for genai
            # (Requires mime_type and data dict)
            mime_type = "audio/wav"
            if audio_path_str.endswith(".mp3"):
                mime_type = "audio/mp3"
            elif audio_path_str.endswith(".ogg"):
                mime_type = "audio/ogg"
                
            audio_part = {
                "mime_type": mime_type,
                "data": audio_data
            }

            prompt = (
                "You have been provided a voice note from a healthcare patient. "
                "First, transcribe their audio exactly. "
                "Second, if their audio was a medical or wellness question, provide a helpful and medically-safe answer. "
                "Output your response strictly as a JSON string matching this structure: "
                "{\n"
                "  \"text\": \"the transcription of the patient's words\",\n"
                "  \"reply\": \"your conversational medical assistant answer\"\n"
                "}"
            )
            
            response = model.generate_content([prompt, audio_part])
            
            # Clean up response text in case of markdown blocks
            res_text = response.text.strip()
            if res_text.startswith("```json"):
                res_text = res_text[7:]
            if res_text.endswith("```"):
                res_text = res_text[:-3]
            res_text = res_text.strip()
            
            import json
            parsed = json.loads(res_text)
            return {
                "text": parsed.get("text", ""),
                "reply": parsed.get("reply", "")
            }
        except Exception as e:
            logger.error(f"Voice processing via Gemini failed: {str(e)}")
            return {
                "text": "[Transcription error]",
                "reply": f"Could not process audio query: {str(e)}"
            }

    @staticmethod
    async def synthesize_speech(text: str) -> str:
        """
        Synthesize speech text. For simplicity and robustness on Windows (to avoid pyttsx3 binary conflicts),
        we return a simulated relative path to an audio track or offer a mock response.
        """
        # In a real environment, this might call Google Cloud TTS, pyttsx3, or edge-tts.
        # We save a mock response path to avoid build issues.
        logger.info(f"Synthesizing voice path for: '{text[:50]}...'")
        return "static/audio/simulated_speech.mp3"
