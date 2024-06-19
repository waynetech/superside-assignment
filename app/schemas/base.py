from pydantic import BaseModel
from pydantic.functional_validators import BeforeValidator
from typing import Annotated, Optional
from beanie import PydanticObjectId
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]


class BaseSchema(BaseModel):
    id: PydanticObjectId
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
