from typing import List
import google.generativeai as genai
from core.config import settings
from core.logger import logger
import numpy as np

def get_text_embedding(text: str) -> List[float]:
    """
    Get 768-dimensional embedding vector for a piece of text using Gemini API.
    """
    if "YOUR_GEMINI_API_KEY" in settings.GEMINI_API_KEY or not settings.GEMINI_API_KEY:
        # Fallback to generating a simple deterministic mock vector based on text characters
        logger.warning("Gemini API key is not configured. Generating deterministic mock embedding vector.")
        hash_seed = sum(ord(char) for char in text[:100])
        np.random.seed(hash_seed)
        vector = np.random.uniform(-1.0, 1.0, 768).tolist()
        return vector

    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    except Exception as e:
        logger.error(f"Gemini embedding generation failed: {str(e)}")
        # Return a simple zero vector rather than failing the execution flow
        return [0.0] * 768
