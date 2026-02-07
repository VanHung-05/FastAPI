from routers.root import router as root_router
from routers.todo import router as todo_router
from routers.auth import router as auth_router

__all__ = ["root_router", "todo_router", "auth_router"]
