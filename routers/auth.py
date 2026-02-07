from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from schemas.user import UserCreate, UserResponse, Token, LoginRequest
from services.auth_service import AuthService
from repositories.user_repository import UserRepository
from core.deps import get_current_user, get_user_repository
from models.user import UserModel

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service(repo: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repo=repo)


@router.post("/register", response_model=UserResponse)
def register(body: UserCreate, service: AuthService = Depends(get_auth_service)):
    """Đăng ký user mới."""
    user = service.register(body)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email đã được sử dụng",
        )
    return user


@router.post("/login", response_model=Token)
def login(body: LoginRequest, service: AuthService = Depends(get_auth_service)):
    """Đăng nhập (JSON body), trả về JWT."""
    result = service.authenticate(body.email, body.password)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không đúng",
        )
    _user, token = result
    return Token(access_token=token)


@router.post("/token", response_model=Token)
def token(form: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends(get_auth_service)):
    """Đăng nhập (form, cho Swagger Authorize). Dùng username = email."""
    result = service.authenticate(form.username, form.password)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không đúng",
        )
    _user, token = result
    return Token(access_token=token)


@router.get("/me", response_model=UserResponse)
def me(current_user: UserModel = Depends(get_current_user)):
    """Lấy thông tin user đang đăng nhập."""
    return UserResponse.model_validate(current_user)
