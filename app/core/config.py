from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "")
    jwt_refresh_secret_key: str = os.getenv("JWT_REFRESH_SECRET_KEY", "")
    access_token_expire_minutes: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24)
    refresh_token_expire_minutes: int = os.getenv("JWT_REFRESH_SECRET_KEY", 60 * 24 * 7)
    bot_protection_secret: str = os.getenv("BOT_PROTECTION_SECRET", "31ar31")


settings = Settings()
