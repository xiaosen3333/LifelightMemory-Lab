# Architecture Notes

- API layer handles validation and auth.
- Service layer orchestrates persistence + vector search.
- Database keeps source-of-truth records.
- Qdrant accelerates semantic retrieval.
- Redis is reserved for queueing/locks in next iterations.
