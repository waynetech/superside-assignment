from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user import (
    UserResponseSchema,
)
from app.models.user import User
from app.dependencies import get_current_user

router = APIRouter()


@router.get(
    "/me",
    response_model=UserResponseSchema,
    summary="Get details of current logged-in user",
)
async def get_me(user: User = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
