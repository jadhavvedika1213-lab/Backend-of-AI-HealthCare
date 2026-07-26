from fastapi import APIRouter, Depends
from core.database import get_db
from schemas.common import HealthCheckResponse
from core.logger import logger

router = APIRouter()

@router.get("", response_model=HealthCheckResponse)
async def check_health(db = Depends(get_db)):
    db_status = "healthy"
    try:
        await db.command("ping")
    except Exception as e:
        logger.error(f"Healthcheck database connection error: {str(e)}")
        db_status = "unhealthy"

    return HealthCheckResponse(
        status="healthy",
        database=db_status
    )
