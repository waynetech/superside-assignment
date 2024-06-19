from .base import BaseDocument
from beanie import Indexed, Link
from pydantic import Field, EmailStr
from typing import List
from pymongo import TEXT, ASCENDING


class User(BaseDocument):
    first_name: str
    last_name: str
    email: Indexed(EmailStr, unique=True, index_type=ASCENDING)
    password: str = None
    is_active: bool = Field(default=False)
    is_superuser: bool = Field(default=False)

    def __str__(self):
        return str(self.id)

    class Settings:
        indexes = [
            [("first_name", TEXT), ("last_name", TEXT)],
        ]
