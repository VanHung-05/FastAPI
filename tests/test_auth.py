"""Test auth: đăng ký, đăng nhập, auth fail."""
import pytest
from fastapi.testclient import TestClient


def test_register_success(client: TestClient):
    """Đăng ký thành công — 200, trả về user (id, email, ...)."""
    import uuid
    email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    r = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "pass1234"},
    )
    assert r.status_code == 200
    data = r.json()
    assert "id" in data
    assert data["email"] == email
    assert "created_at" in data
    assert "hashed_password" not in data


def test_register_validation_fail(client: TestClient):
    """Validation fail — email hoặc password không hợp lệ."""
    # Password quá ngắn (< 6)
    r = client.post(
        "/api/v1/auth/register",
        json={"email": "a@b.com", "password": "12345"},
    )
    assert r.status_code == 422


def test_login_success(client: TestClient):
    """Đăng nhập thành công — 200, trả về access_token."""
    import uuid
    email = f"login_{uuid.uuid4().hex[:8]}@example.com"
    client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "pass1234"},
    )
    r = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "pass1234"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data.get("token_type") == "bearer"
    assert "access_token" in data and len(data["access_token"]) > 0


def test_login_auth_fail(client: TestClient):
    """Auth fail — sai email hoặc mật khẩu trả 401."""
    r = client.post(
        "/api/v1/auth/login",
        json={"email": "nonexistent@example.com", "password": "wrong"},
    )
    assert r.status_code == 401
    assert "detail" in r.json()


def test_me_without_token_auth_fail(client: TestClient):
    """GET /auth/me không gửi token — 401."""
    r = client.get("/api/v1/auth/me")
    assert r.status_code == 401
    assert "detail" in r.json()
