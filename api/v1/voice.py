from fastapi import APIRouter, Depends, UploadFile, File
from models.user import User
from dependencies.auth_dependency import get_current_active_user
from services.upload_service import UploadService
from services.voice_service import VoiceService
from core.config import settings
from utils.response import APIResponse
from schemas.voice import TTSRequest

router = APIRouter()

@router.post("/query-voice")
async def query_voice_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    # Save audio clip
    path = await UploadService.save_uploaded_file(file, settings.AUDIO_DIR)
    
    # Process audio through VoiceService
    result = await VoiceService.transcribe_and_respond(path)
    
    return APIResponse.success(
        message="Voice note processed successfully.",
        data={
            "audio_url": f"/{path}",
            "transcription": result.get("text"),
            "reply": result.get("reply")
        }
    )

@router.post("/text-to-speech")
async def text_to_speech(
    payload: TTSRequest,
    current_user: User = Depends(get_current_active_user)
):
    audio_path = await VoiceService.synthesize_speech(payload.text)
    return APIResponse.success(
        message="TTS speech synthesized successfully.",
        data={"audio_url": f"/{audio_path}"}
    )
