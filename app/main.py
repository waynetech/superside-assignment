from dotenv import load_dotenv

load_dotenv()
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import initialize_db, close_db
from app.routes.router import router as api_router
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    await initialize_db()
    yield
    # on shutdown
    await close_db()


origin = [
    "*",
]
app = FastAPI(lifespan=lifespan, title="Superside GraphRAG")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)


@app.get("/health")
def read_root():
    return {"status": "Good"}
