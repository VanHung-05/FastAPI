from fastapi import APIRouter

router = APIRouter(tags=["root"])


@router.get("/")
def root():
    """Trả message chào."""
    return {"message": "Chào mừng đến với Hello To-Do API!"}


@router.get("/health")
def health():
    """Kiểm tra trạng thái API."""
    return {"status": "ok"}
