from core.database import init_db
from core.scheduler import start_scheduler
from core.config import settings
from utils.helpers import ensure_dir_exists
from core.logger import logger

async def run_startup_tasks() -> None:
    logger.info("Initializing health application startup tasks...")
    
    # 1. Initialize DB tables
    await init_db()
    
    # 2. Ensure storage folders exist
    ensure_dir_exists(settings.UPLOAD_DIR)
    ensure_dir_exists(settings.PRESCRIPTION_DIR)
    ensure_dir_exists(settings.REPORTS_DIR)
    ensure_dir_exists(settings.IMAGES_DIR)
    ensure_dir_exists(settings.AUDIO_DIR)
    ensure_dir_exists(settings.TEMP_DIR)
    
    # 3. Start background scheduler
    start_scheduler()
    
    logger.info("Startup tasks completed successfully.")
