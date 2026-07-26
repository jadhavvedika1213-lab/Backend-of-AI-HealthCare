from typing import Any, Optional
from fastapi.responses import JSONResponse
from fastapi import status

class APIResponse:
    @staticmethod
    def success(message: str = "Request successful", data: Optional[Any] = None, status_code: int = status.HTTP_200_OK) -> JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content={
                "success": True,
                "message": message,
                "data": data
            }
        )

    @staticmethod
    def error(message: str = "An error occurred", errors: Optional[Any] = None, status_code: int = status.HTTP_400_BAD_REQUEST) -> JSONResponse:
        content = {
            "success": False,
            "message": message
        }
        if errors is not None:
            content["errors"] = errors
            
        return JSONResponse(
            status_code=status_code,
            content=content
        )
