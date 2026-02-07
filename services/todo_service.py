from __future__ import annotations

from typing import List, Optional

from schemas.todo import ToDo, ToDoCreate, ToDoUpdate, ToDoPatch, TodoListResponse
from repositories.todo_repository import TodoRepository
from models.todo import TodoModel


def _orm_to_schema(row: TodoModel) -> ToDo:
    return ToDo.model_validate(row)


class TodoService:
    """Nghiệp vụ todo (filter, sort, pagination từ DB)."""

    def __init__(self, repository: TodoRepository) -> None:
        self._repo = repository

    def list_todos(
        self,
        owner_id: int,
        is_done: Optional[bool] = None,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> TodoListResponse:
        rows, total = self._repo.get_list(
            owner_id=owner_id, is_done=is_done, q=q, sort=sort, limit=limit, offset=offset
        )
        items = [_orm_to_schema(r) for r in rows]
        return TodoListResponse(items=items, total=total, limit=limit, offset=offset)

    def create(self, owner_id: int, body: ToDoCreate) -> ToDo:
        row = self._repo.create(
            owner_id=owner_id,
            title=body.title,
            description=body.description,
            is_done=body.is_done,
            due_date=body.due_date,
            tags=body.tags,
        )
        return _orm_to_schema(row)

    def get_by_id(self, todo_id: int, owner_id: int) -> Optional[ToDo]:
        row = self._repo.get_by_id(todo_id, owner_id)
        return _orm_to_schema(row) if row else None

    def update(self, todo_id: int, owner_id: int, body: ToDoUpdate) -> Optional[ToDo]:
        row = self._repo.update(
            todo_id,
            owner_id=owner_id,
            title=body.title,
            description=body.description,
            is_done=body.is_done,
            due_date=body.due_date,
            tags=body.tags,
        )
        return _orm_to_schema(row) if row else None

    def list_overdue(
        self,
        owner_id: int,
        limit: int = 10,
        offset: int = 0,
    ) -> TodoListResponse:
        rows, total = self._repo.get_overdue(owner_id=owner_id, limit=limit, offset=offset)
        items = [_orm_to_schema(r) for r in rows]
        return TodoListResponse(items=items, total=total, limit=limit, offset=offset)

    def list_today(
        self,
        owner_id: int,
        limit: int = 10,
        offset: int = 0,
    ) -> TodoListResponse:
        rows, total = self._repo.get_today(owner_id=owner_id, limit=limit, offset=offset)
        items = [_orm_to_schema(r) for r in rows]
        return TodoListResponse(items=items, total=total, limit=limit, offset=offset)

    def partial_update(self, todo_id: int, owner_id: int, body: ToDoPatch) -> Optional[ToDo]:
        data = body.model_dump(exclude_unset=True)
        row = self._repo.partial_update(todo_id, owner_id, **data)
        return _orm_to_schema(row) if row else None

    def complete(self, todo_id: int, owner_id: int) -> Optional[ToDo]:
        row = self._repo.set_complete(todo_id, owner_id, is_done=True)
        return _orm_to_schema(row) if row else None

    def delete(self, todo_id: int, owner_id: int) -> bool:
        return self._repo.delete(todo_id, owner_id)
