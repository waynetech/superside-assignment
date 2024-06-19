from pydantic import BaseModel
from typing import List


class CreateThreadSchema(BaseModel):
    assistant_id: str


class ThreadSchema(BaseModel):
    thread_id: str
    assistant_id: str
    name: str


class ThreadListSchema(BaseModel):
    threads: List[ThreadSchema]


# class AssistantListSchema(BaseModel):
#     assistants: List[AssistantSchema]
