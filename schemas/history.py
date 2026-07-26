from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class HistoryBase(BaseModel):
    event_type: str
    description: str
    details: Optional[str] = None

class HistoryCreate(HistoryBase):
    pass

class HistoryResponse(HistoryBase):
    id: int
    user_id: int
    recorded_at: datetime

    model_config = ConfigDict(from_attributes=True)
