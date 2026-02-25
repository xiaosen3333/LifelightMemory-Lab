from fastapi import APIRouter
from sqlmodel import text

from app.core.config import get_settings
from app.db.session import engine
from app.services.vector_store import vector_store

router = APIRouter(tags=["health"])


def _db_ok() -> bool:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


def _redis_ok() -> bool:
    settings = get_settings()
    try:
        import redis

        client = redis.from_url(settings.redis_url)
        return bool(client.ping())
    except Exception:
        return False


@router.get("/v1/health")
def health() -> dict:
    return {
        "status": "ok",
        "dependencies": {
            "db": _db_ok(),
            "redis": _redis_ok(),
            "qdrant": vector_store.available,
        },
    }
