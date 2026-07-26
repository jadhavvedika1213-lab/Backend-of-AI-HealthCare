from core.constants import MedicalDocCategory
from models.base import Document, now


class Report(Document):
    @classmethod
    def defaults(cls):
        return {"category": MedicalDocCategory.LAB_REPORT, "uploaded_at": now,
                "ocr_content": None, "summary": None, "analysis_result": None}
