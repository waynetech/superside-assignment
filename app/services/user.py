from app.models.user import User
from app.schemas.user import UserSignUpSchema
from fastapi import HTTPException
from app.utils.auth import get_hashed_password
from pydantic import ValidationError
from pymongo.errors import DuplicateKeyError
from datetime import datetime
from app.core.config import settings


async def create_new_user(user: UserSignUpSchema):
    if user.signup_code != settings.bot_protection_secret:
        raise HTTPException(status_code=422, detail="Invalid signup code")

    user_obj = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=get_hashed_password(user.password),
        is_active=True,
    )

    try:
        await user_obj.insert()
        user_obj.updated_at = datetime.utcnow()
        await user_obj.save()
    except DuplicateKeyError as e:
        print(e)
        raise HTTPException(status_code=422, detail="User already exists")
    except ValidationError:
        print(ValidationError)
        raise HTTPException(status_code=422, detail=ValidationError.errors())
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Server error")
    return user_obj


async def get_user_by_email(email: str):
    user = await User.find(User.email == email, fetch_links=True).first_or_none()
    return user
