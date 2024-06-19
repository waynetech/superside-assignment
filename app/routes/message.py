from fastapi import APIRouter, HTTPException, Depends

from app.models.user import User
from app.dependencies import get_current_user
from app.schemas.message import (
    MessageListSchema,
    MessageResponseSchema,
    CreateMessageSchema,
)
from app.services.message import create_message, list_all_messages_by_thread_id

router = APIRouter()


@router.post(
    "/",
    response_model=MessageResponseSchema,
    summary="Create a new message using thread_id and message",
)
async def create_new_message(
    payload: CreateMessageSchema, user: User = Depends(get_current_user)
):
    message = await create_message(user, payload.thread_id, payload.message)
    if message is None:
        raise HTTPException(status_code=404, detail="User not found")
    return message


@router.get(
    "/",
    response_model=MessageListSchema,
    summary="Get all message using thread_id",
)
async def get_all_messages(thread_id: str, user: User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    messages = await list_all_messages_by_thread_id(thread_id)
    if messages is None:
        raise HTTPException(status_code=404, detail="User not found")
    return messages
