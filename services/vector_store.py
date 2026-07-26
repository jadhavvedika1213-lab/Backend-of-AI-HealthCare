from typing import List, Dict, Any, Tuple
from ai.vector_db import vector_db_instance

class VectorStoreService:
    @staticmethod
    def add_document_vectors(doc_id: str, chunks_with_embeddings: List[Tuple[str, List[float]]]) -> None:
        vector_db_instance.add_chunks(doc_id, chunks_with_embeddings)

    @staticmethod
    def delete_document_vectors(doc_id: str) -> None:
        vector_db_instance.delete_document(doc_id)

    @staticmethod
    def search_vectors(query_vector: List[float], limit: int = 4) -> List[Dict[str, Any]]:
        return vector_db_instance.similarity_search(query_vector, k=limit)
