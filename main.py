from __future__ import annotations

from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Hello To-Do API")

# --- Model ---


class ToDo(BaseModel):
    id: int
    title: str
    is_done: bool = False


class ToDoCreate(BaseModel):
    title: str
    is_done: bool = False


class ToDoUpdate(BaseModel):
    title: str
    is_done: bool = False


# --- Lưu trong RAM ---
todos: List[ToDo] = []
_next_id: int = 1


def _find_index(todo_id: int) -> Optional[int]:
    for i, t in enumerate(todos):
        if t.id == todo_id:
            return i
    return None


# --- Endpoints Cấp 0 ---


@app.get("/")
def root():
    """Trả message chào."""
    return {"message": "Chào mừng đến với Hello To-Do API!"}


@app.get("/health")
def health():
    """Kiểm tra trạng thái API."""
    return {"status": "ok"}


# --- Endpoints CRUD (Cấp 1) ---


@app.post("/todos", response_model=ToDo)
def create_todo(body: ToDoCreate):
    """Tạo todo mới."""
    global _next_id
    todo = ToDo(id=_next_id, title=body.title, is_done=body.is_done)
    todos.append(todo)
    _next_id += 1
    return todo


@app.get("/todos", response_model=List[ToDo])
def list_todos():
    """Lấy danh sách todo."""
    return todos


@app.get("/todos/{todo_id}", response_model=ToDo)
def get_todo(todo_id: int):
    """Lấy chi tiết một todo."""
    idx = _find_index(todo_id)
    if idx is None:
        raise HTTPException(status_code=404, detail="Todo không tồn tại")
    return todos[idx]


@app.put("/todos/{todo_id}", response_model=ToDo)
def update_todo(todo_id: int, body: ToDoUpdate):
    """Cập nhật toàn bộ todo."""
    idx = _find_index(todo_id)
    if idx is None:
        raise HTTPException(status_code=404, detail="Todo không tồn tại")
    todo = ToDo(id=todo_id, title=body.title, is_done=body.is_done)
    todos[idx] = todo
    return todo


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    """Xóa todo."""
    idx = _find_index(todo_id)
    if idx is None:
        raise HTTPException(status_code=404, detail="Todo không tồn tại")
    todos.pop(idx)
    return None
