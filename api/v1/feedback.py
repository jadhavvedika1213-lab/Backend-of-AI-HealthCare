from fastapi import APIRouter, Depends
from models.user import User
from dependencies.auth_dependency import get_current_active_user
from services.analytics_service import AnalyticsService
from models.feedback import Feedback
from core.database import get_db
from schemas.feedback import FeedbackCreate, FeedbackResponse
from utils.response import APIResponse

router = APIRouter()

@router.post("", response_model=FeedbackResponse)
async def create_feedback(
    feedback_in: FeedbackCreate,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db)
):
    feedback = Feedback(
        user_id=current_user.id,
        rating=feedback_in.rating,
        category=feedback_in.category,
        comment=feedback_in.comment
    )
    db.add(feedback)
    await db.commit()
    await db.refresh(feedback)
    
    # Log event
    analytics = AnalyticsService(db)
    await analytics.record_event("feedback_submitted", current_user.id, {"rating": feedback_in.rating})
    
    return feedback
