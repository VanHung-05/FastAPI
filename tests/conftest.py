"""Pytest fixtures — TestClient và token cho test có auth."""
import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    """TestClient dùng chung cho mọi test."""
    return TestClient(app)


@pytest.fixture
def auth_headers(client):
    """
    Đăng ký + đăng nhập, trả về header Authorization để gọi API cần token.
    Mỗi test dùng fixture này sẽ có user mới (email unique).
    """
    import uuid
    email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    password = "password123"
    client.post("/api/v1/auth/register", json={"email": email, "password": password})
    r = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
