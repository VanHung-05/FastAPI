from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from schemas.todo import ToDo, ToDoCreate, ToDoUpdate, ToDoPatch, TodoListResponse
from services.todo_service import TodoService
from core.deps import get_todo_service, get_current_user
from models.user import UserModel

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("", response_model=ToDo)
def create_todo(
    body: ToDoCreate,
    current_user: UserModel = Depends(get_current_user),
    service: TodoService = Depends(get_todo_service),
):
    """Tạo todo mới (thuộc user đăng nhập)."""
    return service.create(current_user.id, body)


@router.get("", response_model=TodoListResponse)
def list_todos(
    current_user: UserModel = Depends(get_current_user),
    service: TodoService = Depends(get_todo_service),
    is_done: Optional[bool] = Query(None, description="Lọc theo trạng thái: true/false"),
    q: Optional[str] = Query(None, description="Tìm theo keyword trong title"),
    sort: Optional[str] = Query(None, description="Sắp xếp: created_at hoặc -created_at"),
    limit: int = Query(10, ge=1, le=100, description="Số bản ghi mỗi trang"),
    offset: int = Query(0, ge=0, description="Vị trí bắt đầu"),
):
    """Lấy danh sách todo của user đăng nhập (filter, search, sort, pagination)."""
    return service.list_todos(
        owner_id=current_user.id,
        is_done=is_done,
        q=q,
        sort=sort,
        limit=limit,
        offset=offset,
    )


@router.get("/{todo_id}", response_model=ToDo)
def get_todo(
    todo_id: int,
    current_user: UserModel = Depends(get_current_user),
    service: TodoService = Depends(get_todo_service),
):
    """Lấy chi tiết một todo (chỉ todo của user đăng nhập)."""
    todo = service.get_by_id(todo_id, current_user.id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo không tồn tại")
    return todo


@router.put("/{todo_id}", response_model=ToDo)
def update_todo(
    todo_id: int,
    body: ToDoUpdate,
    current_user: UserModel = Depends(get_current_user),
    service: TodoService = Depends(get_todo_service),
):
    """Cập nhật toàn bộ todo (chỉ todo của user đăng nhập)."""
    todo = service.update(todo_id, current_user.id, body)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo không tồn tại")
    return todo


@router.patch("/{todo_id}", response_model=ToDo)
def patch_todo(
    todo_id: int,
    body: ToDoPatch,
    current_user: UserModel = Depends(get_current_user),
    service: TodoService = Depends(get_todo_service),
):
    """Cập nhật một phần (vd: chỉ is_done). Chỉ todo của user đăng nhập."""
    todo = service.partial_update(todo_id, current_user.id, body)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo không tồn tại")
    return todo


@router.post("/{todo_id}/complete", response_model=ToDo)
def complete_todo(
    todo_id: int,
    current_user: UserModel = Depends(get_current_user),
    service: TodoService = Depends(get_todo_service),
):
    """Đánh dấu todo hoàn thành. Chỉ todo của user đăng nhập."""
    todo = service.complete(todo_id, current_user.id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo không tồn tại")
    return todo


@router.delete("/{todo_id}", status_code=204)
def delete_todo(
    todo_id: int,
    current_user: UserModel = Depends(get_current_user),
    service: TodoService = Depends(get_todo_service),
):
    """Xóa todo (chỉ todo của user đăng nhập)."""
    if not service.delete(todo_id, current_user.id):
        raise HTTPException(status_code=404, detail="Todo không tồn tại")
    return None
