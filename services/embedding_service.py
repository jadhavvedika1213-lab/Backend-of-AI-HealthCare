from typing import List
from ai.embeddings import get_text_embedding

class EmbeddingService:
    @staticmethod
    def generate_embedding(text: str) -> List[float]:
        return get_text_embedding(text)
        
    @staticmethod
    def generate_batch_embeddings(texts: List[str]) -> List[List[float]]:
        return [get_text_embedding(t) for t in texts]
