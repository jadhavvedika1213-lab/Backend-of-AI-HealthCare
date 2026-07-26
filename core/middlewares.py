from fastapi import FastAPI
from middleware.cors import add_cors_middleware
from middleware.logging import LoggingMiddleware
from middleware.rate_limit import RateLimitMiddleware
from middleware.exception import ExceptionMiddleware
from middleware.request_time import RequestTimeMiddleware
from middleware.auth import AuthMiddleware

def register_middleware(app: FastAPI) -> None:
    # Order matters: middleware is executed in reverse order of addition
    # ExceptionMiddleware catches everything
    app.add_middleware(ExceptionMiddleware)
    # Custom Auth extractor
    app.add_middleware(AuthMiddleware)
    # Rate limiter
    app.add_middleware(RateLimitMiddleware)
    # Processing time header
    app.add_middleware(RequestTimeMiddleware)
    # Logging
    app.add_middleware(LoggingMiddleware)
    # CORS (uses FastAPI helper)
    add_cors_middleware(app)
