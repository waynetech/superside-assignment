from .base import BaseDocument
from beanie import Link
from pymongo import TEXT, ASCENDING
from .user import User


class Message(BaseDocument):
    thread_id: str
    owner: Link[User]
    message: str
    role: str

    def __str__(self):
        return str(self.id)

    class Settings:
        indexes = [
            [("thread_id", ASCENDING)],
            [("owner", ASCENDING)],
        ]
