import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:///./test_lifelight_lab.db"
os.environ["VECTOR_ENABLED"] = "false"
os.environ["API_KEY"] = "test-api-key"

from app.main import app  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def cleanup_db_file() -> None:
    db_path = Path("test_lifelight_lab.db")
    if db_path.exists():
        db_path.unlink()
    yield
    if db_path.exists():
        db_path.unlink()


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as client:
        yield client
