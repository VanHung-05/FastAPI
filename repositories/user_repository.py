from __future__ import annotations

from typing import Optional

from sqlalchemy import select

from models.user import UserModel
from sqlalchemy.orm import Session


class UserRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_id(self, user_id: int) -> Optional[UserModel]:
        return self._db.get(UserModel, user_id)

    def get_by_email(self, email: str) -> Optional[UserModel]:
        stmt = select(UserModel).where(UserModel.email == email)
        return self._db.execute(stmt).scalars().one_or_none()

    def create(self, email: str, hashed_password: str) -> UserModel:
        user = UserModel(email=email, hashed_password=hashed_password)
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user
