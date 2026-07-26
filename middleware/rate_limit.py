from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from core.limiter import global_limiter

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Exclude docs and internal routes from rate limiting if desired
        if request.url.path.startswith(("/docs", "/redoc", "/openapi.json")):
            return await call_next(request)
            
        client_ip = request.client.host if request.client else "unknown"
        allowed, wait_time = global_limiter.is_allowed(client_ip)
        if not allowed:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "success": False,
                    "detail": f"Too many requests. Please retry in {wait_time} seconds."
                }
            )
        return await call_next(request)
