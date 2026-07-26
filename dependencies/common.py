from fastapi import Query
from pydantic import BaseModel

class CommonPagination(BaseModel):
    skip: int = 0
    limit: int = 100

async def get_pagination_params(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Max number of records to return")
) -> CommonPagination:
    return CommonPagination(skip=skip, limit=limit)
