"""Test todos: tạo thành công, validation fail, 404, auth fail."""
import pytest
from fastapi.testclient import TestClient


def test_create_todo_success(client: TestClient, auth_headers: dict):
    """Tạo todo thành công — 200, trả về todo có id, title, ..."""
    r = client.post(
        "/api/v1/todos",
        headers=auth_headers,
        json={
            "title": "Todo test",
            "description": "Mô tả",
            "is_done": False,
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "Todo test"
    assert data["description"] == "Mô tả"
    assert "id" in data
    assert data["is_done"] is False


def test_create_todo_validation_fail(client: TestClient, auth_headers: dict):
    """Validation fail — title quá ngắn (< 3 ký tự) trả 422."""
    r = client.post(
        "/api/v1/todos",
        headers=auth_headers,
        json={"title": "ab", "description": "ok"},
    )
    assert r.status_code == 422


def test_get_todo_404(client: TestClient, auth_headers: dict):
    """404 — lấy todo không tồn tại (id rất lớn)."""
    r = client.get("/api/v1/todos/999999", headers=auth_headers)
    assert r.status_code == 404
    assert "detail" in r.json()


def test_todos_without_token_auth_fail(client: TestClient):
    """Auth fail — gọi API todo không gửi token trả 401."""
    r = client.get("/api/v1/todos")
    assert r.status_code == 401
    assert "detail" in r.json()

    r2 = client.post(
        "/api/v1/todos",
        json={"title": "Test", "description": None},
    )
    assert r2.status_code == 401
