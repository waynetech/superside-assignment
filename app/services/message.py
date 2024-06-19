from app.core.openai_client import openai
from fastapi import HTTPException
from app.models.user import User
from app.models.thread import Thread
from app.services.assistant import get_assistant
from pymongo.errors import DuplicateKeyError
from pydantic import ValidationError
from .thread import get_thread
from app.models.message import Message


async def create_message(user: User, thread_id: str, message: str):
    thread = await get_thread(thread_id)
    message_obj = None
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    try:
        user_message_obj = Message(
            role="user", message=message, thread_id=thread.thread_id, owner=user
        )
        await user_message_obj.insert()
        message_response = openai.beta.threads.messages.create(
            thread_id=thread.thread_id, role="user", content=message
        )
        # print("message_response: ", message_response)
        run = openai.beta.threads.runs.create_and_poll(
            thread_id=thread.thread_id, assistant_id=thread.assistant_id
        )
        if run.status == "completed":
            # messages = openai.beta.threads.messages.list(thread_id=thread.thread_id, limit=1)
            messages = openai.beta.threads.messages.list(
                run_id=run.id, thread_id=thread.thread_id, limit=1
            )
            # print("messages: ", messages)
            for _message in messages:
                assert _message.content[0].type == "text"
                # print(
                #     {"role": _message.role, "message": _message.content[0].text.value}
                # )
                message_obj = Message(
                    role=_message.role,
                    message=_message.content[0].text.value,
                    thread_id=thread.thread_id,
                    owner=user,
                )
                await message_obj.insert()
    except DuplicateKeyError as e:
        print(e)
        raise HTTPException(status_code=422, detail="Thread already exists")
    except ValidationError:
        print(ValidationError)
        raise HTTPException(status_code=422, detail=ValidationError.errors())
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Server error")
    return message_obj


async def list_all_threads_by_logged_in_user(user: User):
    threads = []
    try:
        threads = (
            await Thread.find(Thread.owner.id == user.id, fetch_links=True)
            .sort(-Thread.created_at)
            .to_list()
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"threads": threads}


async def list_all_messages_by_thread_id(thread_id: str):
    messages = []
    try:
        messages = (
            await Message.find(Message.thread_id == thread_id, fetch_links=True)
            .sort(Message.created_at)
            .to_list()
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"messages": messages}
