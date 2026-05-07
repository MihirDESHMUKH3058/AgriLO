import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

async def cleanup():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]
    result = await db.users.delete_one({"email": "admin@gmail.com"})
    print(f"Deleted {result.deleted_count} user(s).")

asyncio.run(cleanup())
