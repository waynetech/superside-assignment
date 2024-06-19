from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserSignUpSchema
from app.services.user import create_new_user
from app.schemas.auth import (
    TokenSchema,
)
from app.utils.auth import create_access_token, create_refresh_token
from app.services.auth import login_user
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


@router.post(
    "/sign-up",
    summary="Create a new user using sign up form",
    response_model=TokenSchema,
)
async def signup_user(user: UserSignUpSchema):
    user_obj = await create_new_user(user=user)
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Something went wrong while creating user",
        )
    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }


@router.post(
    "/login",
    summary="Create access and refresh tokens for user",
    response_model=TokenSchema,
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await login_user(form_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }
