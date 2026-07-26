from typing import Optional
from pydantic import BaseModel

class VoiceTranscriptionResponse(BaseModel):
    text: str
    confidence: float

class TTSRequest(BaseModel):
    text: str
    voice_type: Optional[str] = "male"  # male/female/neutral

class TTSResponse(BaseModel):
    audio_url: str
