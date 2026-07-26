from datetime import datetime
from typing import Union

def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    return dt.strftime(format_str)

def parse_iso_datetime(iso_str: str) -> datetime:
    return datetime.fromisoformat(iso_str)

def format_file_size(size_in_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} TB"
