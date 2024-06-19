from fastapi import APIRouter, HTTPException, Depends

from app.models.user import User
from app.dependencies import get_current_user
from app.services.assistant import list_all_assistants
from app.schemas.thread import CreateThreadSchema, ThreadListSchema, ThreadSchema
from app.services.thread import (
    create_thread,
    list_all_threads_by_logged_in_user,
    delete_all_threads,
)

router = APIRouter()


@router.post(
    "/",
    response_model=ThreadSchema,
    summary="Create a thread using assistant id",
)
async def create_thread_using_assistant_id(
    thread_input: CreateThreadSchema, user: User = Depends(get_current_user)
):
    thread = await create_thread(user=user, assistant_id=thread_input.assistant_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return thread


@router.get(
    "/",
    response_model=ThreadListSchema,
    summary="Get all the threads created by logged-in user",
)
async def get_all_threads_by_user(user: User = Depends(get_current_user)):
    thread = await list_all_threads_by_logged_in_user(user=user)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return thread


@router.delete(
    "/",
    summary="Get all the threads created by logged-in user",
)
async def delete_threads(user: User = Depends(get_current_user)):

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    thread = await delete_all_threads(user=user)

    return {"status": "success"}
