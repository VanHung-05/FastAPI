# Hello To-Do API (FastAPI)

## Cấp 0 — Làm quen FastAPI

Mục tiêu: tạo API tối thiểu chạy được.

### Yêu cầu

- Tạo project FastAPI
- **Endpoint:**
  - `GET /health` → trả `{ "status": "ok" }`
  - `GET /` → trả message chào

### Tiêu chí đạt

- Chạy uvicorn và gọi được 2 endpoint.

---

## Cấp 1 — CRUD cơ bản (dữ liệu trong RAM)

Mục tiêu: CRUD với list/dict trong bộ nhớ (chưa dùng DB).

### Model ToDo

- `id`: int
- `title`: str
- `is_done`: bool = False

### Endpoints

| Method | Path | Mô tả |
|--------|------|--------|
| POST | `/todos` | Tạo todo |
| GET | `/todos` | Lấy danh sách |
| GET | `/todos/{id}` | Lấy chi tiết |
| PUT | `/todos/{id}` | Cập nhật toàn bộ |
| DELETE | `/todos/{id}` | Xóa |

### Tiêu chí đạt

- Validate dữ liệu bằng Pydantic
- Trả lỗi 404 khi không tìm thấy

### Swagger UI (Cấp 1)

Mở [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) để xem và gọi thử API:

![Swagger UI - CRUD ToDo](docs/cap1-swagger-ui.png)

---

## Cấu trúc project

```
FastAPI/
├── main.py           # Ứng dụng FastAPI và các endpoint
├── requirements.txt  # Dependencies
├── test_cap1.py      # Script kiểm tra Cấp 1
├── docs/             # Ảnh minh họa
└── README.md
```

## Cài đặt và chạy

1. **Cài dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Chạy server:**

   ```bash
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

3. **Kiểm tra:**
   - Trang chủ: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Health: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
   - Tài liệu API (Swagger UI): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Chạy test Cấp 1: `python3 test_cap1.py`
