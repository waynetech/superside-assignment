from beanie import Document
from datetime import datetime
from pydantic import Field


class BaseDocument(Document):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
