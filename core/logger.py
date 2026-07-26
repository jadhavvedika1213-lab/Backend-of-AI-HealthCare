import os
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler

# Ensure log directory exists
log_dir = Path("logs")
log_dir.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("healthcare_backend")
logger.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# App log file handler
app_log_path = log_dir / "app.log"
file_handler = RotatingFileHandler(
    app_log_path, maxBytes=10485760, backupCount=5, encoding="utf-8"
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Error log file handler
error_log_path = log_dir / "error.log"
err_handler = RotatingFileHandler(
    error_log_path, maxBytes=10485760, backupCount=5, encoding="utf-8"
)
err_handler.setLevel(logging.ERROR)
err_handler.setFormatter(formatter)
logger.addHandler(err_handler)
