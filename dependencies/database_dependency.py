from core.database import get_db


async def get_async_db():
    yield await get_db()
