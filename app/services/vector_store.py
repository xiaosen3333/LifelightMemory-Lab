from __future__ import annotations

import logging
from typing import Any, Dict, List

from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class VectorStore:
    def __init__(self) -> None:
        settings = get_settings()
        self.available = False
        self.collection = settings.qdrant_collection
        self.vector_size = settings.vector_size

        if not settings.vector_enabled:
            logger.info("Vector store disabled by configuration")
            return

        try:
            self.client = QdrantClient(url=settings.qdrant_url)
            collections = self.client.get_collections().collections
            existing = {item.name for item in collections}
            if self.collection not in existing:
                self.client.create_collection(
                    collection_name=self.collection,
                    vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE),
                )
            self.available = True
        except Exception as exc:
            logger.warning("Qdrant is unavailable. Fallback mode enabled: %s", exc)
            self.available = False

    def upsert(self, point_id: int, vector: List[float], payload: Dict[str, Any]) -> None:
        if not self.available:
            return

        point = PointStruct(id=point_id, vector=vector, payload=payload)
        self.client.upsert(collection_name=self.collection, points=[point], wait=True)

    def search(self, query_vector: List[float], user_id: str, limit: int) -> List[Dict[str, Any]]:
        if not self.available:
            return []

        query_filter = Filter(
            must=[FieldCondition(key="user_id", match=MatchValue(value=user_id))]
        )
        result = self.client.search(
            collection_name=self.collection,
            query_vector=query_vector,
            query_filter=query_filter,
            with_payload=True,
            limit=limit,
        )
        return [
            {
                "entry_id": int(item.id),
                "score": float(item.score),
                "payload": item.payload or {},
            }
            for item in result
        ]


vector_store = VectorStore()
