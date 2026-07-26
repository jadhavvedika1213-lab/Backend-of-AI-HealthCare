from ai.rag_pipeline import RAGPipeline
from models.report import Report
from repositories.report_repo import ReportRepository

class RAGService:
    def __init__(self, db):
        self.report_repo = ReportRepository(db)

    async def ingest_report_by_id(self, report_id: int) -> int:
        """
        Fetch report, check if it has extracted OCR text, and index it into the vector store.
        """
        report = await self.report_repo.get_by_id(report_id)
        if not report or not report.ocr_content:
            return 0
            
        doc_id = f"report_{report_id}"
        return await RAGPipeline.ingest_document(doc_id, report.ocr_content)

    async def query(self, question: str, limit: int = 4) -> str:
        return await RAGPipeline.query_rag(question, k=limit)
