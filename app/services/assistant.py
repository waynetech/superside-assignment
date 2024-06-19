from app.core.openai_client import openai
from fastapi import HTTPException


async def list_all_assistants():
    assistants = []
    try:
        assistants = openai.beta.assistants.list()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"assistants": assistants}


async def get_assistant(assistant_id: str):
    assistant = None
    try:
        assistant = openai.beta.assistants.retrieve(assistant_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return assistant
