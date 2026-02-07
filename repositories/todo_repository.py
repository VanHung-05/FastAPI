from __future__ import annotations

from typing import List, Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models.todo import TodoModel


class TodoRepository:
    """Truy cập dữ liệu todo (PostgreSQL)."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def get_list(
        self,
        is_done: Optional[bool] = None,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> Tuple[List[TodoModel], int]:
        stmt = select(TodoModel)
        count_stmt = select(func.count()).select_from(TodoModel)

        if is_done is not None:
            stmt = stmt.where(TodoModel.is_done == is_done)
            count_stmt = count_stmt.where(TodoModel.is_done == is_done)
        if q is not None and q.strip():
            q_lower = f"%{q.strip().lower()}%"
            stmt = stmt.where(func.lower(TodoModel.title).like(q_lower))
            count_stmt = count_stmt.where(func.lower(TodoModel.title).like(q_lower))

        total = self._db.execute(count_stmt).scalar() or 0

        if sort == "-created_at":
            stmt = stmt.order_by(TodoModel.created_at.desc())
        elif sort == "created_at":
            stmt = stmt.order_by(TodoModel.created_at.asc())
        elif sort == "-updated_at":
            stmt = stmt.order_by(TodoModel.updated_at.desc())
        elif sort == "updated_at":
            stmt = stmt.order_by(TodoModel.updated_at.asc())

        stmt = stmt.limit(limit).offset(offset)
        rows = list(self._db.execute(stmt).scalars().all())
        return rows, total

    def get_by_id(self, todo_id: int) -> Optional[TodoModel]:
        stmt = select(TodoModel).where(TodoModel.id == todo_id)
        return self._db.execute(stmt).scalars().one_or_none()

    def create(self, title: str, description: Optional[str] = None, is_done: bool = False) -> TodoModel:
        todo = TodoModel(title=title, description=description, is_done=is_done)
        self._db.add(todo)
        self._db.commit()
        self._db.refresh(todo)
        return todo

    def update(
        self,
        todo_id: int,
        title: str,
        description: Optional[str] = None,
        is_done: bool = False,
    ) -> Optional[TodoModel]:
        todo = self.get_by_id(todo_id)
        if todo is None:
            return None
        todo.title = title
        todo.description = description
        todo.is_done = is_done
        self._db.commit()
        self._db.refresh(todo)
        return todo

    def partial_update(self, todo_id: int, **kwargs: object) -> Optional[TodoModel]:
        todo = self.get_by_id(todo_id)
        if todo is None:
            return None
        for key, value in kwargs.items():
            if hasattr(todo, key):
                setattr(todo, key, value)
        self._db.commit()
        self._db.refresh(todo)
        return todo

    def set_complete(self, todo_id: int, is_done: bool = True) -> Optional[TodoModel]:
        return self.partial_update(todo_id, is_done=is_done)

    def delete(self, todo_id: int) -> bool:
        todo = self.get_by_id(todo_id)
        if todo is None:
            return False
        self._db.delete(todo)
        self._db.commit()
        return True
