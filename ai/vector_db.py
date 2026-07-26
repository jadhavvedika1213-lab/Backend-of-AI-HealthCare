import sqlite3
import json
from typing import List, Dict, Any, Tuple
from pathlib import Path
from core.config import settings
from core.logger import logger
import math

class SQLiteVectorDB:
    def __init__(self, db_path: str = "./vector_store.db"):
        self.db_path = str(settings.get_absolute_path(db_path))
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS document_chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_id TEXT NOT NULL,
                text_chunk TEXT NOT NULL,
                embedding_json TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def add_chunks(self, doc_id: str, chunks: List[Tuple[str, List[float]]]):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        for text, emb in chunks:
            cursor.execute(
                "INSERT INTO document_chunks (doc_id, text_chunk, embedding_json) VALUES (?, ?, ?)",
                (doc_id, text, json.dumps(emb))
            )
        conn.commit()
        conn.close()

    def delete_document(self, doc_id: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM document_chunks WHERE doc_id = ?", (doc_id,))
        conn.commit()
        conn.close()

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude_v1 = math.sqrt(sum(a * a for a in vec1))
        magnitude_v2 = math.sqrt(sum(b * b for b in vec2))
        
        if magnitude_v1 == 0 or magnitude_v2 == 0:
            return 0.0
        return dot_product / (magnitude_v1 * magnitude_v2)

    def similarity_search(self, query_vector: List[float], k: int = 4) -> List[Dict[str, Any]]:
        """
        Query vector cosine similarity comparison across all chunks in the database.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT doc_id, text_chunk, embedding_json FROM document_chunks")
        rows = cursor.fetchall()
        conn.close()

        results = []
        for doc_id, text, emb_str in rows:
            try:
                emb = json.loads(emb_str)
                score = self._cosine_similarity(query_vector, emb)
                results.append({
                    "doc_id": doc_id,
                    "text": text,
                    "score": score
                })
            except Exception as e:
                logger.error(f"Error computing similarity: {str(e)}")
                continue

        # Sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:k]

# Global single instance of SQLiteVectorDB
vector_db_instance = SQLiteVectorDB()
