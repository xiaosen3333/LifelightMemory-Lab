from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class MemoryEntry(SQLModel, table=True):
    __tablename__ = "memory_entries"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    content: str
    language: str = Field(default="zh-CN")
    source: str = Field(default="manual")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)
