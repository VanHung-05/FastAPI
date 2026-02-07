from fastapi import FastAPI

app = FastAPI(title="Hello To-Do API")


@app.get("/")
def root():
    """Trả message chào."""
    return {"message": "Chào mừng đến với Hello To-Do API!"}


@app.get("/health")
def health():
    """Kiểm tra trạng thái API."""
    return {"status": "ok"}
