from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.schemas import (
    MemoryIngestRequest,
    MemoryIngestResponse,
    MemorySearchRequest,
    MemorySearchResponse,
)
from app.core.security import verify_api_key
from app.db.session import get_session
from app.services.memory_service import MemoryService

router = APIRouter(prefix="/v1/memory", tags=["memory"], dependencies=[Depends(verify_api_key)])


@router.post("/ingest", response_model=MemoryIngestResponse)
def ingest_memory(request: MemoryIngestRequest, session: Session = Depends(get_session)) -> MemoryIngestResponse:
    service = MemoryService(session)
    entry_id = service.ingest(
        user_id=request.user_id,
        content=request.content,
        language=request.language,
    )
    return MemoryIngestResponse(entry_id=entry_id, message="memory stored")


@router.post("/search", response_model=MemorySearchResponse)
def search_memory(request: MemorySearchRequest, session: Session = Depends(get_session)) -> MemorySearchResponse:
    service = MemoryService(session)
    hits = service.search(user_id=request.user_id, query=request.query, limit=request.limit)
    return MemorySearchResponse(hits=hits)
