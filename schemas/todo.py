from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

TITLE_MIN = 3
TITLE_MAX = 100
DESCRIPTION_MAX = 2000


class ToDo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str] = None
    is_done: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ToDoCreate(BaseModel):
    title: str = Field(..., min_length=TITLE_MIN, max_length=TITLE_MAX)
    description: Optional[str] = Field(None, max_length=DESCRIPTION_MAX)
    is_done: bool = False


class ToDoUpdate(BaseModel):
    title: str = Field(..., min_length=TITLE_MIN, max_length=TITLE_MAX)
    description: Optional[str] = Field(None, max_length=DESCRIPTION_MAX)
    is_done: bool = False


class ToDoPatch(BaseModel):
    """Cập nhật một phần (PATCH). Tất cả field tùy chọn."""

    title: Optional[str] = Field(None, min_length=TITLE_MIN, max_length=TITLE_MAX)
    description: Optional[str] = Field(None, max_length=DESCRIPTION_MAX)
    is_done: Optional[bool] = None


class TodoListResponse(BaseModel):
    items: List[ToDo]
    total: int
    limit: int
    offset: int
