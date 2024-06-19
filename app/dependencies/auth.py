from typing import Union
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.utils.auth import ALGORITHM, JWT_SECRET_KEY

from jose import jwt
from pydantic import ValidationError
from app.schemas.auth import TokenPayloadSchema
from app.models.user import User
from app.services.user import get_user_by_email


reuseable_oauth = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login", scheme_name="JWT")


async def get_current_user(token: str = Depends(reuseable_oauth)) -> User:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayloadSchema(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user: Union[User, None] = await get_user_by_email(token_data.sub)
    if user.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user


async def get_inactive_user(token: str = Depends(reuseable_oauth)) -> User:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayloadSchema(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user: Union[User, None] = await get_user_by_email(token_data.sub)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user
