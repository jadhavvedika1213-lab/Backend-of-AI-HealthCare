from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class ReminderBase(BaseModel):
    title: str
    reminder_type: str  # medication, appointment, checkup
    time: str          # HH:MM format or ISO datetime string
    frequency: str      # daily, weekly, once
    is_active: bool = True
    email_notification: bool = True

class ReminderCreate(ReminderBase):
    pass

class ReminderUpdate(BaseModel):
    title: Optional[str] = None
    reminder_type: Optional[str] = None
    time: Optional[str] = None
    frequency: Optional[str] = None
    is_active: Optional[bool] = None
    status: Optional[str] = None
    email_notification: Optional[bool] = None

class ReminderResponse(ReminderBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    last_triggered: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
