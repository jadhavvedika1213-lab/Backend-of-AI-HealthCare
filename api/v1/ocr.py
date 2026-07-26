from fastapi import APIRouter, Depends, UploadFile, File
from models.user import User
from dependencies.auth_dependency import get_current_active_user
from services.upload_service import UploadService
from services.ocr_service import OCRService
from core.config import settings
from utils.response import APIResponse

router = APIRouter()

@router.post("")
async def extract_text_ocr(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    path = await UploadService.save_uploaded_file(file, settings.TEMP_DIR)
    extracted_text = await OCRService.extract_text(path)
    
    return APIResponse.success(
        message="Text extraction completed.",
        data={
            "filename": file.filename,
            "extracted_text": extracted_text
        }
    )
