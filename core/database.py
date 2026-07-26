from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from core.config import settings

client = None
db = None

async def get_db() -> AsyncIOMotorDatabase:
    global db
    return db

async def next_id(collection: str) -> int:
    global db
    counter = await db.counters.find_one_and_update(
        {"_id": collection}, {"$inc": {"value": 1}}, upsert=True, return_document=True
    )
    return counter["value"]


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def clean_document(document: Mapping[str, Any] | None) -> dict[str, Any] | None:
    if document is None:
        return None
    return {key: value for key, value in document.items() if key != "_id"}


async def init_db() -> None:
    global client, db
    client = AsyncIOMotorClient(settings.MONGODB_URL, serverSelectionTimeoutMS=5000)
    db = client[settings.DATABASE_NAME]

    await client.admin.command("ping")
    await db.users.create_index("email", unique=True)
    await db.users.create_index("id", unique=True)
    for collection in ("reports", "reminders", "histories", "prescriptions", "notifications", "feedbacks"):
        await db[collection].create_index("user_id")
    await db.chat_messages.create_index([("session_id", 1), ("created_at", 1)])
    await db.analytics_events.create_index("created_at")


async def close_db() -> None:
    client.close()
