import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """
    FastAPI test client used by endpoint tests.
    """
    return TestClient(app)