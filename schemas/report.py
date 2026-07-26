from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class ReportBase(BaseModel):
    filename: str
    category: str

class ReportCreate(ReportBase):
    file_path: str
    ocr_content: Optional[str] = None
    summary: Optional[str] = None
    analysis_result: Optional[str] = None

class ReportResponse(ReportBase):
    id: int
    user_id: int
    file_path: str
    uploaded_at: datetime
    ocr_content: Optional[str] = None
    summary: Optional[str] = None
    analysis_result: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ReportAnalysisResponse(BaseModel):
    report_id: int
    filename: str
    summary: str
    recommendations: str
    structured_data: Optional[str] = None
