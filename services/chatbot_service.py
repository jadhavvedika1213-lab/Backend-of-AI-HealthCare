from models.chat import ChatSession, ChatMessage
from repositories.chat_repo import ChatRepository
import google.generativeai as genai
from core.config import settings
from utils.prompt import MedicalPrompts
from core.logger import logger
from utils.helpers import generate_uuid
from typing import List, Optional

class ChatbotService:
    def __init__(self, db):
        self.repo = ChatRepository(db)

    async def get_or_create_session(self, user_id: int, session_id: Optional[str] = None) -> ChatSession:
        if session_id:
            session = await self.repo.get_session(session_id)
            if session and session.user_id == user_id:
                return session
        
        # Create a new session
        new_id = generate_uuid()
        session = ChatSession(id=new_id, user_id=user_id, title="New Conversation")
        return await self.repo.create_session(session)

    async def send_chatbot_message(self, user_id: int, session_id: str, content: str) -> ChatMessage:
        session = await self.get_or_create_session(user_id, session_id)
        
        # Save User Message
        user_message = ChatMessage(session_id=session.id, role="user", content=content)
        await self.repo.add_message(user_message)
        
        # Fetch previous message history (ordered)
        history = await self.repo.get_messages(session.id)
        
        # Format history for Gemini API
        gemini_history = []
        # Add system prompt as standard instruction
        for msg in history[:-1]:  # exclude the newly added user message to pass as prompt
            gemini_history.append({
                "role": "user" if msg.role == "user" else "model",
                "parts": [msg.content]
            })

        # Synthesize reply
        assistant_reply = ""
        if "YOUR_GEMINI_API_KEY" in settings.GEMINI_API_KEY or not settings.GEMINI_API_KEY:
            assistant_reply = (
                f"[MOCK CHAT REPLY] HealthBuddy: I received your question '{content}'. "
                f"Please configure the Gemini API key in settings to activate me!"
            )
        else:
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                
                # We initialize chat with history and system instruction
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=MedicalPrompts.CHATBOT_SYSTEM
                )
                
                chat = model.start_chat(history=gemini_history)
                response = chat.send_message(content)
                assistant_reply = response.text
            except Exception as e:
                logger.error(f"Chatbot response generation failed: {str(e)}")
                assistant_reply = f"I apologize, but I encountered an error: {str(e)}. Please try again."

        # Save Assistant Message
        assistant_message = ChatMessage(session_id=session.id, role="assistant", content=assistant_reply)
        return await self.repo.add_message(assistant_message)

    async def list_sessions(self, user_id: int) -> List[ChatSession]:
        return await self.repo.get_sessions_by_user_id(user_id)

    async def get_messages(self, session_id: str, user_id: int) -> List[ChatMessage]:
        session = await self.repo.get_session(session_id)
        if not session or session.user_id != user_id:
            return []
        return await self.repo.get_messages(session_id)
        
    async def delete_session(self, session_id: str, user_id: int) -> bool:
        session = await self.repo.get_session(session_id)
        if not session or session.user_id != user_id:
            return False
        return await self.repo.delete_session(session_id)
class ChatbotServiceAlias(ChatbotService):
    pass
