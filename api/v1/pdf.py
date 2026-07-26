from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from models.user import User
from dependencies.auth_dependency import get_current_active_user
from services.upload_service import UploadService
from services.report_service import ReportService
from services.pdf_service import PDFService
from core.config import settings
from core.database import get_db
from utils.response import APIResponse
from schemas.report import ReportResponse

router = APIRouter()

@router.post("/analyze-file")
async def upload_and_analyze_pdf(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported by this endpoint.")
        
    # Save file
    path = await UploadService.save_uploaded_file(file, settings.REPORTS_DIR)
    
    # Create record
    report_service = ReportService(db)
    report = await report_service.create_report_record(
        user_id=current_user.id,
        filename=file.filename,
        file_path=path,
        category="lab_report"
    )
    
    # Analyze
    pdf_service = PDFService(db)
    analyzed_report = await pdf_service.process_and_analyze_report(report.id)
    
    return APIResponse.success(
        message="PDF uploaded and analyzed successfully.",
        data=ReportResponse.model_validate(analyzed_report)
    )

@router.post("/analyze-id/{report_id}")
async def analyze_existing_report(
    report_id: int,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    report_service = ReportService(db)
    report = await report_service.get_report(report_id, current_user.id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found or permission denied.")
        
    pdf_service = PDFService(db)
    analyzed_report = await pdf_service.process_and_analyze_report(report_id)
    return APIResponse.success(
        message="Medical report analyzed successfully.",
        data=ReportResponse.model_validate(analyzed_report)
    )
