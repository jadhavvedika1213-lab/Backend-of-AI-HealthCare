from fastapi import APIRouter, Depends, UploadFile, File
from models.user import User
from dependencies.auth_dependency import get_current_active_user
from services.upload_service import UploadService
from core.config import settings
from utils.response import APIResponse

router = APIRouter()

@router.post("")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    path = await UploadService.save_uploaded_file(file, settings.UPLOAD_DIR)
    return APIResponse.success(
        message="File uploaded successfully",
        data={
            "filename": file.filename,
            "file_url": f"/{path}",
            "relative_path": path
        }
    )
