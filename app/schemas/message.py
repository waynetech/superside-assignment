from pydantic import BaseModel
from beanie import PydanticObjectId
from typing import List


class CreateMessageSchema(BaseModel):
    thread_id: str
    message: str


class OwnerSchema(BaseModel):
    id: PydanticObjectId
    first_name: str
    last_name: str


class MessageResponseSchema(BaseModel):
    thread_id: str
    owner: OwnerSchema
    message: str
    role: str


class MessageListSchema(BaseModel):
    messages: List[MessageResponseSchema]
