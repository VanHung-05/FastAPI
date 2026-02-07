from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from repositories.todo_repository import TodoRepository
from services.todo_service import TodoService


def get_todo_repository(db: Session = Depends(get_db)) -> TodoRepository:
    return TodoRepository(db)


def get_todo_service(repository: TodoRepository = Depends(get_todo_repository)) -> TodoService:
    return TodoService(repository=repository)
