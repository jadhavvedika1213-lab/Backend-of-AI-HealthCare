from typing import Any, Optional
from pydantic import BaseModel, ConfigDict

class GenericAPIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

class HealthCheckResponse(BaseModel):
    status: str
    database: str
    version: str = "1.0.0"
