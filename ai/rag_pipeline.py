from typing import List, Dict, Any
from ai.embeddings import get_text_embedding
from ai.vector_db import vector_db_instance
from utils.prompt import MedicalPrompts
import google.generativeai as genai
from core.config import settings
from core.logger import logger

class RAGPipeline:
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
        """
        Split document text into clean chunks with configured overlap.
        """
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk:
                chunks.append(chunk)
        return chunks

    @classmethod
    async def ingest_document(cls, doc_id: str, text: str) -> int:
        """
        Chunk and embed text chunks, then save to the SQLite Vector DB.
        """
        chunks = cls.chunk_text(text)
        if not chunks:
            return 0
            
        embedded_chunks = []
        for chunk in chunks:
            embedding = get_text_embedding(chunk)
            embedded_chunks.append((chunk, embedding))
            
        vector_db_instance.add_chunks(doc_id, embedded_chunks)
        return len(chunks)

    @classmethod
    async def query_rag(cls, question: str, k: int = 4) -> str:
        """
        Perform RAG query. Retrieve context and synthesize an answer.
        """
        # 1. Get query embedding
        query_embedding = get_text_embedding(question)
        
        # 2. Search SQLite vector store
        matched_chunks = vector_db_instance.similarity_search(query_embedding, k=k)
        
        if not matched_chunks:
            # Fallback to direct general LLM response
            from services.ai_service import AIService
            return await AIService.ask_general_question(question)

        # 3. Build context
        context_str = "\n---\n".join([chunk["text"] for chunk in matched_chunks])
        
        # 4. Prompt Gemini with context
        if "YOUR_GEMINI_API_KEY" in settings.GEMINI_API_KEY or not settings.GEMINI_API_KEY:
            # Mock Synthesized Answer
            return (
                f"[MOCK RAG ANSWER]\n"
                f"Based on retrieved sections, here is your context-aware answer:\n"
                f"- User Query: '{question}'\n"
                f"- Context snippet: '{matched_chunks[0]['text'][:100]}...'\n"
                f"Configure your Gemini API key to see actual generation."
            )
            
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt = MedicalPrompts.RAG_CONTEXT_PROMPT.format(
                context=context_str,
                question=question
            )
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Synthesized RAG generation failed: {str(e)}")
            return f"Error synthesizing query results: {str(e)}"
