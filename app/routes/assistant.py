from fastapi import APIRouter, HTTPException, Depends

from app.models.user import User
from app.dependencies import get_current_user
from app.services.assistant import list_all_assistants
from app.schemas.assistant import AssistantListSchema

router = APIRouter()


@router.get(
    "/",
    response_model=AssistantListSchema,
    summary="Get list of available assistants",
)
async def get_all_assistants(user: User = Depends(get_current_user)):
    assistants = await list_all_assistants()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return assistants
