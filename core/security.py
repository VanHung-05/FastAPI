from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import bcrypt
import jwt

from core.config import settings

# Bcrypt chỉ chấp nhận tối đa 72 byte
BCRYPT_MAX_PASSWORD_BYTES = 72


def _truncate_password(plain: str) -> bytes:
    """Cắt password xuống tối đa 72 byte (giới hạn của bcrypt)."""
    return plain.encode("utf-8")[:BCRYPT_MAX_PASSWORD_BYTES]


def hash_password(plain: str) -> str:
    pw = _truncate_password(plain)
    return bcrypt.hashpw(pw, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    pw = _truncate_password(plain)
    return bcrypt.checkpw(pw, hashed.encode("utf-8"))


def create_access_token(subject: Any, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )


def decode_access_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub = payload.get("sub")
        return str(sub) if sub is not None else None
    except jwt.PyJWTError:
        return None
