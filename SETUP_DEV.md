# HƯỚNG DẪN SETUP CHO DEVELOPER

> Hướng dẫn cài đặt và chạy project BigZone trên máy local.

---

## MỤC LỤC

1. [Yêu cầu hệ thống](#1-yêu-cầu-hệ-thống)
2. [Cài đặt](#2-cài-đặt)
3. [Chạy ứng dụng](#3-chạy-ứng-dụng)
4. [Tài khoản mặc định](#4-tài-khoản-mặc-định)
5. [Cấu trúc project](#5-cấu-trúc-project)
6. [Các lệnh hữu ích](#6-các-lệnh-hữu- ích)
7. [Xử lý sự cố](#7-xử-lý-sự-cố)

---

## 1. YÊU CẦU HỆ THỐNG

| Thành phần | Phiên bản tối thiểu |
|------------|---------------------|
| Python | 3.9 trở lên |
| pip | Mới nhất |
| OS | Windows 10/11, macOS, Linux |

### Kiểm tra phiên bản Python
```bash
python --version
# Hoặc
python3 --version
```

---

## 2. CÀI ĐẶT

### Bước 2.1: Clone project
```bash
git clone https://github.com/tee-overthinker/build_pc_bigzone.git
cd build_pc_bigzone
```

### Bước 2.2: Tạo Virtual Environment (Khuyến nghị)
```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### Bước 2.3: Cài đặt dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Các thư viện cần cài đặt:
```
fastapi          - Framework web
uvicorn          - ASGI server
sqlalchemy       - ORM cho database
jinja2           - Template engine
python-multipart - Xử lý form data
passlib[bcrypt]  - Mã hóa password
python-jose      - JWT token
anthropic        - Chatbot AI (Claude API)
```

---

## 3. CHẠY ỨNG DỤNG

### Cách 1: Chạy trực tiếp bằng Python
```bash
cd backend
python main.py
```

### Cách 2: Chạy bằng Uvicorn (Khuyến nghị - có hot reload)
```bash
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Cách 3: Chạy với debug mode
```bash
cd backend
python -X dev main.py
```

### Kết quả mong đợi:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Truy cập website:
- **Website**: http://localhost:8000
- **Admin**: http://localhost:8000/admin
- **API Docs**: http://localhost:8000/docs

---

## 4. TÀI KHOẢN MẶC ĐỊNH

| Loại | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |

### Cách truy cập Admin:
1. Truy cập http://localhost:8000
2. Nhấn nút "Đăng nhập" ở góc phải header
3. Đăng nhập với tài khoản admin ở trên
4. Sẽ được chuyển hướng đến trang Admin

---

## 5. CẤU TRÚC PROJECT

```
build_pc_bigzone/
├── backend/
│   ├── main.py          # File chính của ứng dụng (FastAPI)
│   ├── database.py      # Cấu hình SQLAlchemy
│   ├── models.py        # Định nghĩa database models
│   ├── schemas.py       # Pydantic schemas cho API
│   ├── routers.py       # Các router cho admin/auth
│   ├── auth.py          # Xác thực và phân quyền
│   ├── chatbot.py       # Tích hợp Chatbot AI
│   ├── seed.py          # Script tạo dữ liệu mẫu
│   ├── requirements.txt  # Danh sách thư viện
│   └── pcmarket.db      # SQLite database (tự động tạo)
│
├── static/              # File tĩnh (CSS, JS, Images)
│   ├── css/
│   ├── images/
│   └── js/
│
├── templates/           # Jinja2 templates
│   ├── base.html
│   ├── pages/           # Các trang HTML
│   ├── components/      # Các component tái sử dụng
│   └── admin/           # Trang admin
│
├── document/            # Tài liệu dự án
│
├── logo-bigzone.png     # Logo website
├── .gitignore           # Git ignore file
└── SETUP_DEV.md         # File này
```

---

## 6. CÁC LỆNH HỮU ÍCH

### 6.1. Reset database và tạo dữ liệu mẫu
```bash
cd backend
python seed.py
```

**Lệnh này sẽ:**
- Xóa toàn bộ dữ liệu cũ
- Tạo lại các bảng database
- Tạo tài khoản admin
- Tạo 8 danh mục sản phẩm
- Tạo 30+ sản phẩm mẫu với hình ảnh

### 6.2. Kiểm tra database thủ công
```bash
cd backend
python -c "from database import SessionLocal; from models import Product; db = SessionLocal(); print('Products:', db.query(Product).count())"
```

### 6.3. Tạo admin user mới
```bash
cd backend
python -c "
from database import SessionLocal
import models
import auth

db = SessionLocal()
admin = models.User(username='admin2', password_hash=auth.get_password_hash('password123'), role='admin')
db.add(admin)
db.commit()
print('Admin created!')
"
```

### 6.4. Cập nhật packages
```bash
pip install -r requirements.txt --upgrade
```

---

## 7. XỬ LÝ SỰ CỐ

### Lỗi: `ModuleNotFoundError: No module named 'fastapi'`
**Giải pháp:**
```bash
pip install -r requirements.txt
```

### Lỗi: `sqlite3.OperationalError: database is locked`
**Giải pháp:** Đóng tất cả các kết nối đến database và thử lại. Hoặc khởi động lại server.

### Lỗi: Port 8000 đang được sử dụng
**Giải pháp:** Sử dụng port khác
```bash
uvicorn main:app --reload --port 8001
```

### Lỗi: Chatbot AI không hoạt động
**Giải pháp:** Kiểm tra biến môi trường `ANTHROPIC_API_KEY`
```bash
# Windows
set ANTHROPIC_API_KEY=sk-xxxxx

# macOS/Linux
export ANTHROPIC_API_KEY=sk-xxxxx
```

### Lỗi: Không thấy hình ảnh sản phẩm
**Giải pháp:** Kiểm tra kết nối internet (hình ảnh được load từ Unsplash CDN).

### Muốn xem logs chi tiết hơn
```bash
# Chạy với debug level
cd backend
python -c "import logging; logging.basicConfig(level=logging.DEBUG)" && python main.py
```

---

## LIÊN HỆ HỖ TRỢ

Nếu gặp vấn đề khác, vui lòng:
- Tạo Issue trên GitHub
- Liên hệ qua email: support@bigzone.vn
- Zalo: 0912345678

---

> **BigZone** — Happy Coding! 🎮