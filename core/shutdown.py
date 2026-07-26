from core.scheduler import shutdown_scheduler
from core.database import close_db
from core.logger import logger

async def run_shutdown_tasks() -> None:
    logger.info("Initializing application shutdown tasks...")
    
    # Stop background tasks scheduler
    shutdown_scheduler()
    await close_db()
    
    logger.info("Shutdown tasks completed.")
