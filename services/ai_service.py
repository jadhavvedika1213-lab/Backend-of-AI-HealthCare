import google.generativeai as genai
from core.config import settings
from core.logger import logger
from utils.prompt import MedicalPrompts

class AIService:
    @staticmethod
    async def ask_general_question(prompt: str) -> str:
        """
        Ask a general healthcare question using Gemini LLM.
        """
        if "YOUR_GEMINI_API_KEY" in settings.GEMINI_API_KEY or not settings.GEMINI_API_KEY:
            return (
                "[MOCK ANSWER] This is a mock response from the AI Medical Assistant. "
                "Ensure your GEMINI_API_KEY is configured in the .env file to enable actual AI responses."
            )
            
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            # Use ChatBot system prompt as background instruction
            chat = model.start_chat(history=[])
            response = chat.send_message(
                f"{MedicalPrompts.CHATBOT_SYSTEM}\n\nUser Question: {prompt}"
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini API general question failed: {str(e)}")
            return f"Error communicating with AI service: {str(e)}"
