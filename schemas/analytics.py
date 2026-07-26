from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class AnalyticsEventCreate(BaseModel):
    event_name: str
    metadata_json: Optional[str] = None

class AnalyticsResponse(BaseModel):
    id: int
    event_name: str
    user_id: Optional[int] = None
    metadata_json: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
