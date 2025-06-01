"""conftest.py: Pytest fixtures for testing the Fitness And Diet App."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """TestClient fixture for sending requests to the FastAPI app."""
    return TestClient(app)