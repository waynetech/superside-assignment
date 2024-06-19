from .base import BaseSchema
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr | None = Field(default=None)
    password: str = Field(min_length=8)
    
    
class UserSignUpSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr | None = Field(default=None)
    password: str = Field(min_length=8)
    signup_code: str


class UserUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponseSchema(BaseSchema):
    first_name: str
    last_name: str
    email: EmailStr | None = Field(default=None)
    is_active: bool


class UserListSchema(BaseModel):
    users: List[UserResponseSchema]


