from pydantic import BaseModel
from typing import List


class AssistantSchema(BaseModel):
    name: str
    id: str


class AssistantListSchema(BaseModel):
    assistants: List[AssistantSchema]
