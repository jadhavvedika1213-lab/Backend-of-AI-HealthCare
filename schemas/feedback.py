from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class FeedbackCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Rating must be between 1 and 5")
    category: str = "general"  # bug, feature_request, ai_accuracy, general
    comment: Optional[str] = None

class FeedbackResponse(FeedbackCreate):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
