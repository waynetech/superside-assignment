from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .config import settings

from app.models.user import User


class DataBase:
    client: AsyncIOMotorClient = None  # type: ignore


DB = DataBase()


async def initialize_db():
    DB.client = AsyncIOMotorClient(settings.database_url)
    await init_beanie(
        database=DB.client.get_default_database(),
        document_models=[
            User,
        ],
    )


async def close_db():
    DB.client.close()
