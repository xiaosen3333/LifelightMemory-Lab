def test_memory_endpoint_requires_api_key(client):
    response = client.post(
        "/v1/memory/ingest",
        json={
            "user_id": "u-1",
            "content": "hello memory",
            "language": "en-US",
        },
    )
    assert response.status_code == 401


def test_ingest_and_search_flow(client):
    headers = {"X-API-Key": "test-api-key"}

    ingest_response = client.post(
        "/v1/memory/ingest",
        headers=headers,
        json={
            "user_id": "u-1",
            "content": "I practiced backend architecture and Docker today",
            "language": "en-US",
        },
    )
    assert ingest_response.status_code == 200
    assert ingest_response.json()["entry_id"] > 0

    search_response = client.post(
        "/v1/memory/search",
        headers=headers,
        json={
            "user_id": "u-1",
            "query": "Docker",
            "limit": 5,
        },
    )
    assert search_response.status_code == 200
    hits = search_response.json()["hits"]
    assert len(hits) >= 1
    assert "Docker" in hits[0]["content"]
