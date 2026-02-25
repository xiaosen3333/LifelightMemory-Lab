import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes_health import router as health_router
from app.api.routes_memory import router as memory_router
from app.core.config import get_settings
from app.db.session import init_db

settings = get_settings()
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Public-safe abstraction of a production memory backend",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(memory_router)


@app.get("/")
def root() -> dict:
    return {
        "name": settings.app_name,
        "env": settings.app_env,
        "docs": "/docs",
    }
