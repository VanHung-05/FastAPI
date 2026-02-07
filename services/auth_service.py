from __future__ import annotations

from typing import Optional

from schemas.user import UserCreate, UserResponse
from repositories.user_repository import UserRepository
from core.security import hash_password, verify_password, create_access_token
from models.user import UserModel


def _user_to_response(user: UserModel) -> UserResponse:
    return UserResponse.model_validate(user)


class AuthService:
    def __init__(self, user_repo: UserRepository) -> None:
        self._repo = user_repo

    def register(self, body: UserCreate) -> Optional[UserResponse]:
        if self._repo.get_by_email(body.email) is not None:
            return None
        user = self._repo.create(
            email=body.email,
            hashed_password=hash_password(body.password),
        )
        return _user_to_response(user)

    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        user = self._repo.get_by_id(user_id)
        return _user_to_response(user) if user else None

    def authenticate(self, email: str, password: str) -> Optional[tuple[UserModel, str]]:
        user = self._repo.get_by_email(email)
        if user is None or not user.is_active:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        token = create_access_token(subject=user.id)
        return (user, token)
