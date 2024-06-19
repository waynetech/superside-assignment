from fastapi import APIRouter
from .user import router as user_router
from .auth import router as auth_router
from .assistant import router as assistant_router
from .thread import router as thread_router

router = APIRouter(prefix="/api/v1")

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(assistant_router, prefix="/assistants", tags=["assistants"])
router.include_router(thread_router, prefix="/threads", tags=["threads"])
