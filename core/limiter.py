import time
from collections import defaultdict
from typing import Dict, List, Tuple
import threading
from fastapi import HTTPException, Request, status

class InMemoryLimiter:
    def __init__(self, requests_limit: int = 60, window_seconds: int = 60):
        self.requests_limit = requests_limit
        self.window_seconds = window_seconds
        # Stores client_identifier -> list of timestamps
        self.history: Dict[str, List[float]] = defaultdict(list)
        self.lock = threading.Lock()

    def is_allowed(self, identifier: str) -> Tuple[bool, int]:
        """
        Check if request is allowed. Returns (is_allowed, seconds_to_wait)
        """
        current_time = time.time()
        with self.lock:
            timestamps = self.history[identifier]
            
            # Filter out timestamps older than the sliding window
            cutoff = current_time - self.window_seconds
            timestamps = [t for t in timestamps if t > cutoff]
            self.history[identifier] = timestamps
            
            if len(timestamps) < self.requests_limit:
                timestamps.append(current_time)
                return True, 0
            
            # If not allowed, calculate time until the oldest timestamp falls out of the window
            if timestamps:
                oldest_timestamp = timestamps[0]
                wait_time = int(self.window_seconds - (current_time - oldest_timestamp))
                return False, max(wait_time, 1)
            return False, 1

# Instantiate a global default rate limiter (e.g., 100 requests per minute)
global_limiter = InMemoryLimiter(requests_limit=100, window_seconds=60)

async def rate_limit_dependency(request: Request):
    # Use client IP as the default identifier, fall back to empty string
    client_ip = request.client.host if request.client else "unknown"
    allowed, wait_time = global_limiter.is_allowed(client_ip)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many requests. Please retry in {wait_time} seconds."
        )
