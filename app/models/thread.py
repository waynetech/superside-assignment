from .base import BaseDocument
from beanie import Link
from pymongo import TEXT, ASCENDING
from .user import User


class Thread(BaseDocument):
    name: str
    thread_id: str
    owner: Link[User]
    assistant_id: str

    def __str__(self):
        return str(self.id)

    class Settings:
        indexes = [
            [("thread_id", ASCENDING)],
            [("owner", ASCENDING)],
            [("assistant_id", ASCENDING)],
            [("name", TEXT)],
        ]
