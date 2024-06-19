from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .config import settings

from app.models.user import User
from app.models.thread import Thread


class DataBase:
    client: AsyncIOMotorClient = None  # type: ignore


DB = DataBase()


async def initialize_db():
    DB.client = AsyncIOMotorClient(settings.database_url)
    await init_beanie(
        database=DB.client.superside_db,
        document_models=[User, Thread],
    )


async def close_db():
    DB.client.close()
