from fastapi import FastAPI

from core.config import settings
from routers import root_router, todo_router

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.include_router(root_router)
app.include_router(todo_router, prefix=settings.API_V1_PREFIX)
