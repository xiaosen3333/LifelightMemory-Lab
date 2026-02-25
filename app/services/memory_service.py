from typing import List

from sqlmodel import Session, select

from app.api.schemas import MemoryHit
from app.core.config import get_settings
from app.db.models import MemoryEntry
from app.services.embedder import embed_text
from app.services.vector_store import vector_store


class MemoryService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.settings = get_settings()

    def ingest(self, user_id: str, content: str, language: str) -> int:
        entry = MemoryEntry(user_id=user_id, content=content, language=language)
        self.session.add(entry)
        self.session.commit()
        self.session.refresh(entry)

        vector = embed_text(content, self.settings.vector_size)
        vector_store.upsert(
            point_id=entry.id,
            vector=vector,
            payload={
                "user_id": user_id,
                "content": content,
                "language": language,
                "created_at": entry.created_at.isoformat(),
            },
        )

        return int(entry.id)

    def search(self, user_id: str, query: str, limit: int) -> List[MemoryHit]:
        vector = embed_text(query, self.settings.vector_size)
        semantic_hits = vector_store.search(query_vector=vector, user_id=user_id, limit=limit)

        if semantic_hits:
            ids = [item["entry_id"] for item in semantic_hits]
            rows = self.session.exec(select(MemoryEntry).where(MemoryEntry.id.in_(ids))).all()
            by_id = {int(row.id): row for row in rows if row.id is not None}

            output: List[MemoryHit] = []
            for hit in semantic_hits:
                row = by_id.get(hit["entry_id"])
                if not row:
                    continue
                output.append(
                    MemoryHit(
                        entry_id=hit["entry_id"],
                        score=hit["score"],
                        content=row.content,
                        language=row.language,
                        created_at=row.created_at,
                    )
                )
            return output

        lexical_rows = self.session.exec(
            select(MemoryEntry)
            .where(MemoryEntry.user_id == user_id)
            .where(MemoryEntry.content.contains(query))
            .order_by(MemoryEntry.created_at.desc())
            .limit(limit)
        ).all()

        return [
            MemoryHit(
                entry_id=int(row.id),
                score=0.3,
                content=row.content,
                language=row.language,
                created_at=row.created_at,
            )
            for row in lexical_rows
            if row.id is not None
        ]
