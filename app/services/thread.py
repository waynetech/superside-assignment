from app.core.openai_client import openai
from fastapi import HTTPException
from app.models.user import User
from app.models.thread import Thread
from app.models.message import Message
from app.services.assistant import get_assistant
from pymongo.errors import DuplicateKeyError
from pydantic import ValidationError


async def create_thread(user: User, assistant_id: str):
    assistant = await get_assistant(assistant_id)
    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")
    try:
        thread = openai.beta.threads.create()
        thread_obj = Thread(
            name=assistant.name + "-" + thread.id,
            thread_id=thread.id,
            owner=user,
            assistant_id=assistant_id,
        )
        await thread_obj.insert()
    except DuplicateKeyError as e:
        print(e)
        raise HTTPException(status_code=422, detail="Thread already exists")
    except ValidationError:
        print(ValidationError)
        raise HTTPException(status_code=422, detail=ValidationError.errors())
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Server error")
    return thread_obj


async def list_all_threads_by_logged_in_user(user: User):
    threads = []
    try:
        threads = (
            await Thread.find(Thread.owner.id == user.id, fetch_links=True, limit=20)
            .sort(-Thread.created_at)
            .to_list()
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"threads": threads}


async def get_thread(thread_id: str):
    thread = None
    try:
        thread = await Thread.find_one(Thread.thread_id == thread_id)
        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    return thread


async def delete_all_threads(user: User):
    try:
        rt = await Thread.find(Thread.owner.id == user.id).delete()
        rm = await Message.find(Message.owner.id == user.id).delete()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": "All threads deleted successfully"}
