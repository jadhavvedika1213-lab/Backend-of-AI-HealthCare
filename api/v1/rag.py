from fastapi import APIRouter, Depends, HTTPException
from models.user import User
from dependencies.auth_dependency import get_current_active_user
from services.rag_service import RAGService
from core.database import get_db
from utils.response import APIResponse
from pydantic import BaseModel

router = APIRouter()

class RAGQueryRequest(BaseModel):
    question: str

@router.post("/ingest/{report_id}")
async def ingest_report(
    report_id: int,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    service = RAGService(db)
    chunks_created = await service.ingest_report_by_id(report_id)
    if chunks_created > 0:
        return APIResponse.success(
            message=f"Successfully indexed document. Generated {chunks_created} vector chunks."
        )
    raise HTTPException(
        status_code=400,
        detail="Ingestion failed. Ensure report exists, belongs to you, and contains extracted OCR content."
    )

@router.post("/query")
async def query_rag_knowledge(
    payload: RAGQueryRequest,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    service = RAGService(db)
    answer = await service.query(payload.question)
    return APIResponse.success(
        message="RAG query completed.",
        data={"answer": answer}
    )
