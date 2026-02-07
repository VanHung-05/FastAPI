from __future__ import annotations

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY

from models.base import Base


class TodoModel(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_done = Column(Boolean, default=False, nullable=False)
    due_date = Column(Date, nullable=True)
    tags = Column(ARRAY(Text), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at = Column(DateTime(timezone=True), nullable=True)
