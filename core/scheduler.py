import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.database import get_db
from services.reminder_service import ReminderService
from core.logger import logger

# Async scheduler instance
scheduler = None

async def check_reminders_job():
    """
    Async entry point called by APScheduler.
    Runs the async reminder trigger in the main event loop.
    """
    try:
        db = await get_db()
        service = ReminderService(db)
        await service.trigger_pending_reminders()
    except Exception as e:
        logger.error(f"Error in background reminders check: {str(e)}")

def start_scheduler():
    global scheduler
    if scheduler is None:
        # Bind APScheduler to FastAPI's active loop. Without this, APScheduler can
        # run jobs on a different loop than Motor's MongoDB client.
        scheduler = AsyncIOScheduler(event_loop=asyncio.get_running_loop())
    if not scheduler.running:
        # Add job to run every minute
        scheduler.add_job(check_reminders_job, "cron", minute="*")
        scheduler.start()
        logger.info("Background Scheduler started successfully.")

def shutdown_scheduler():
    global scheduler
    if scheduler and scheduler.running:
        scheduler.shutdown()
        logger.info("Background Scheduler stopped successfully.")
