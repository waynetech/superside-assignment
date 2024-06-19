from pydantic import BaseModel, Field, EmailStr


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayloadSchema(BaseModel):
    sub: str
    exp: int


