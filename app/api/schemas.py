from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class MemoryIngestRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    language: str = Field(default="zh-CN")


class MemoryIngestResponse(BaseModel):
    entry_id: int
    message: str


class MemorySearchRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    query: str = Field(..., min_length=1)
    limit: int = Field(default=5, ge=1, le=20)


class MemoryHit(BaseModel):
    entry_id: int
    score: float
    content: str
    language: str
    created_at: datetime


class MemorySearchResponse(BaseModel):
    hits: List[MemoryHit]
