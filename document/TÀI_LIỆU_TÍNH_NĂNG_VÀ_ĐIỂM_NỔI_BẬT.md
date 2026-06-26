# TÀI LIỆU TỔNG HỢP - WEBSITE BIGZONE
## Thương Mại Điện Tử PC/Laptop Tích Hợp Chatbot AI

---

## MỤC LỤC

1. [Tổng quan dự án](#1-tổng-quan-dự-án)
2. [Kiến trúc hệ thống](#2-kiến-trúc-hệ-thống)
3. [Tính năng người dùng (Frontend)](#3-tính-năng-người-dùng-frontend)
4. [Tính năng quản trị (Admin)](#4-tính-năng-quản-trị-admin)
5. [API & Tích hợp](#5-api--tích-hợp)
6. [Chatbot AI tư vấn](#6-chatbot-ai-tư-vấn)
7. [Bảo mật & Tối ưu](#7-bảo-mật--tối-ưu)
8. [Điểm nổi bật của dự án](#8-điểm-nổi-bật-của-dự-án)
9. [Công nghệ sử dụng](#9-công-nghệ-sử-dụng)
10. [Cấu trúc dự án](#10-cấu-trúc-dự-án)

---

## 1. TỔNG QUAN DỰ ÁN

### 1.1 Giới thiệu

**BigZone** là website thương mại điện tử chuyên bán PC, laptop, linh kiện máy tính và gaming gear. Dự án được phát triển với mục tiêu:

- Cung cấp trải nghiệm mua sắm trực tuyến tiện lợi, hiệu quả
- Tư vấn tự động thông minh bằng Chatbot AI dựa trên nhu cầu và ngân sách khách hàng
- Giảm tải công việc tư vấn cho nhân viên

### 1.2 Phạm vi

| Giai đoạn | Mô tả | Trạng thái |
|-----------|-------|------------|
| Giai đoạn 1 | Nền tảng TMĐT (Frontend + Admin + API) | ✅ Hoàn thành |
| Giai đoạn 2 | Tích hợp Chatbot AI tư vấn | ✅ Hoàn thành |
| Giai đoạn 3 | Kiểm thử, tối ưu, triển khai | 🔄 Đang thực hiện |

### 1.3 Đối tượng sử dụng

- **Khách hàng**: Mua sắm PC, laptop, linh kiện online
- **Quản trị viên (Admin)**: Quản lý sản phẩm, đơn hàng
- **Khách vãng lai**: Xem sản phẩm, tìm kiếm, không cần đăng nhập

---

## 2. KIẾN TRÚC HỆ THỐNG

### 2.1 Sơ đồ kiến trúc

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENT (Browser)                       │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌──────────┐  │
│  │   HTML   │  │   CSS   │  │   JS    │  │  Jinja2   │  │
│  │ Templates│  │ (Modular)│  │(Vanilla)│  │ Templates │  │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬─────┘  │
└───────┼────────────┼────────────┼─────────────┼────────┘
        │            │            │             │
        └────────────┴────────────┴─────────────┘
                          │
                     FastAPI Server
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   ┌────▼────┐     ┌─────▼────┐     ┌─────▼────┐
   │ Routers │     │  Models  │     │ Schemas  │
   │  (API)  │     │  (SQLAl) │     │(Pydantic)│
   └────┬────┘     └────┬─────┘     └─────┬────┘
        │                │                 │
        └────────────────┼─────────────────┘
                         │
              ┌──────────▼──────────┐
              │   SQLite Database   │
              │    (pcmarket.db)     │
              └──────────────────────┘
                         │
        ┌─────────────────┴─────────────────┐
        │                                   │
   ┌────▼──────────────────────────┐ ┌────▼───────────┐
   │     Chatbot AI (Claude API)    │ │  JWT Auth      │
   │     - Tool use search_products │ │  - bcrypt      │
   │     - Streaming SSE response   │ │  - HttpOnly    │
   └────────────────────────────────┘ └────────────────┘
```

### 2.2 Database Schema

```
┌─────────────┐       ┌─────────────┐
│    User     │       │  Category   │
├─────────────┤       ├─────────────┤
│ id (PK)     │       │ id (PK)     │
│ username    │       │ name        │
│ password    │       │ icon        │───────┐
│ role        │       └──────┬──────┘       │
└─────────────┘              │              │
     1:N                     │         1:N  │
     ┊                   ┌───▼───┐           │
     ┊                   │Product│           │
     ┊              ┌────│       │◄──────────┘
     ┊              │    └───────┘
     ┊              │        │
     ┊              │        │
┌────▼────┐    ┌────▼────────▼─────┐
│  Order  │    │    OrderItem      │
├─────────┤    ├───────────────────┤
│ id (PK) │───►│ id (PK)           │
│ customer│    │ order_id (FK)     │
│ address │    │ product_id        │
│ total   │    │ product_title     │
│ status  │    │ price             │
│ payment │    │ quantity          │
│ created │    └───────────────────┘
└─────────┘
```

---

## 3. TÍNH NĂNG NGƯỜI DÙNG (FRONTEND)

### 3.1 Trang chủ (Home Page)

| Tính năng | Mô tả chi tiết |
|-----------|----------------|
| **Hero Banner** | Slider quảng cáo khuyến mãi nổi bật |
| **8 Danh mục sản phẩm** | Hiển thị với icon Phosphor, hover effect |
| **Khu vực HOT SALE** | Tối đa 10 sản phẩm giảm giá sốc (section="HOT_SALE") |
| **Khu vực PC GAMING** | Tối đa 10 sản phẩm gaming nổi bật (section="PC_GAMING") |
| **Header** | Logo, search, hotline, giỏ hàng, đăng nhập |
| **Footer** | Thông tin liên hệ, newsletter, social links |

### 3.2 Danh mục sản phẩm (Category Page)

| Tính năng | Mô tả chi tiết |
|-----------|----------------|
| **Lưới sản phẩm** | 12 sản phẩm/trang, responsive grid |
| **Thông tin sản phẩm** | Hình ảnh, tên, thương hiệu, giá, % giảm |
| **Sắp xếp** | 4 tùy chọn: Mặc định, Giá ↑, Giá ↓, Giảm nhiều nhất |
| **Phân trang** | Tự động chia trang, nút Trước/Sau |
| **Filter theo section** | Lọc HOT_SALE, PC_GAMING, hoặc tất cả |

### 3.3 Chi tiết sản phẩm (Product Page)

| Tính năng | Mô tả chi tiết |
|-----------|----------------|
| **Hình ảnh** | Ảnh lớn rõ nét |
| **Thông tin giá** | Giá hiện tại, giá cũ (gạch ngang), % giảm |
| **Tồn kho** | Còn hàng / Hết hàng |
| **Thêm vào giỏ** | Nút + số lượng, toast notification, visual feedback |
| **Mô tả** | Thông số kỹ thuật chi tiết |
| **Sản phẩm liên quan** | Tối đa 5 sản phẩm cùng danh mục |
| **Thông tin bổ sung** | Miễn phí vận chuyển, bảo hành |

### 3.4 Tìm kiếm (Search)

| Tính năng | Mô tả chi tiết |
|-----------|----------------|
| **Tìm kiếm đa trường** | Tên, thương hiệu, mô tả sản phẩm |
| **Kết quả** | Lưới sản phẩm với phân trang |
| **Sắp xếp** | Hỗ trợ tất cả 4 tùy chọn sắp xếp |
| **Highlight** | Từ khóa tìm kiếm được hiển thị |

### 3.5 Giỏ hàng (Cart)

| Tính năng | Mô tả chi tiết |
|-----------|----------------|
| **Lưu trữ** | localStorage (không cần đăng nhập) |
| **Thêm sản phẩm** | Từ trang sản phẩm hoặc card nhanh |
| **Chỉnh sửa số lượng** | Nút +/-, tối thiểu 1 |
| **Xóa sản phẩm** | Xóa từng sản phẩm hoặc xóa tất cả |
| **Tính tổng** | Tự động tính thành tiền |
| **Điều hướng** | Tiếp tục mua / Thanh toán |

### 3.6 Thanh toán (Checkout)

| Tính năng | Mô tả chi tiết |
|-----------|----------------|
| **Form thông tin** | Họ tên, SĐT, email, địa chỉ đầy đủ |
| **Danh sách 56 tỉnh/thành** | Dropdown chọn Tỉnh/Thành phố VN |
| **Phương thức thanh toán** | COD (mặc định), Chuyển khoản ngân hàng |
| **Thông tin ngân hàng** | Vietcombank, nội dung: PCM + SĐT |
| **Validation** | Kiểm tra đầy đủ, định dạng SĐT, email |
| **Xác nhận** | Kiểm tra tồn kho, tính lại giá từ server |

### 3.7 Xác nhận đơn hàng (Order Success)

| Tính năng | Mô tả chi tiết |
|-----------|----------------|
| **Mã đơn hàng** | Order ID để theo dõi |
| **Thông tin người nhận** | Tên, SĐT, email, địa chỉ |
| **Danh sách sản phẩm** | Tên, số lượng, đơn giá |
| **Trạng thái** | pending → confirmed → shipping → done |
| **Tổng tiền** | Tổng cộng cuối cùng |

### 3.8 Đăng nhập / Đăng xuất

| Tính năng | Mô tả chi tiết |
|-----------|----------------|
| **Form đăng nhập** | Username + password |
| **Token JWT** | Lưu trong cookie HttpOnly, 7 ngày |
| **Chuyển hướng** | User → trang chủ, Admin → /admin |
| **Hiển thị user** | Tên user trên header khi đăng nhập |
| **Đăng xuất** | Xóa cookie, quay về trang chủ |

### 3.9 Các tính năng bổ sung

| Tính năng | Mô tả chi tiết |
|-----------|----------------|
| **Floating buttons** | Zalo, Messenger, Hotline, Lên đầu trang |
| **Newsletter** | Đăng ký nhận tin khuyến mãi |
| **Toast notifications** | Thông báo thành công/lỗi |
| **Responsive design** | Desktop/Tablet/Mobile |
| **Scroll effects** | Header blur, shadow khi cuộn |
| **Mobile menu** | Slide menu hamburger |

---

## 4. TÍNH NĂNG QUẢN TRỊ (ADMIN)

### 4.1 Dashboard

| Tính năng | Mô tả chi tiết |
|-----------|----------------|
| **Thống kê** | Tổng sản phẩm, tổng đơn hàng |
| **Thẻ thống kê** | Card với icon và màu sắc |
| **Điều hướng** | Link đến các trang quản lý |

### 4.2 Quản lý sản phẩm (CRUD)

| Thao tác | Mô tả |
|----------|-------|
| **Xem danh sách** | Bảng với hình ảnh, tên, giá, tồn kho |
| **Thêm sản phẩm** | Form với tất cả trường |
| **Sửa sản phẩm** | Tải dữ liệu cũ, chỉnh sửa |
| **Xóa sản phẩm** | Xóa vĩnh viễn khỏi hệ thống |

**Trường thông tin sản phẩm:**

| Trường | Bắt buộc | Mô tả |
|--------|----------|-------|
| Tên sản phẩm | ✅ | Tên đầy đủ |
| Danh mục | ✅ | 1 trong 8 danh mục |
| Thương hiệu | ❌ | Ví dụ: ASUS, Intel |
| Khu vực nổi bật | ❌ | HOT_SALE / PC_GAMING / empty |
| Giá hiện tại | ✅ | VNĐ |
| Giá cũ | ❌ | VNĐ (để tính % giảm) |
| % giảm giá | ❌ | Số nguyên 0-100 |
| Hình ảnh | ❌ | URL ảnh |
| Mô tả | ❌ | Text dài |
| Tồn kho | ❌ | Mặc định 0 |

### 4.3 Phân quyền

| Role | Quyền truy cập |
|------|----------------|
| **user** | Trang người dùng, giỏ hàng, đặt hàng |
| **admin** | Tất cả + /admin/* |

---

## 5. API & TÍCH HỢP

### 5.1 Public API

| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/api/categories` | GET | Danh sách danh mục |
| `/api/products` | GET | Danh sách sản phẩm (filter được) |
| `/api/products?category_id=1` | GET | Filter theo danh mục |
| `/api/products?section=HOT_SALE` | GET | Filter theo section |
| `/api/products?q=asus` | GET | Tìm kiếm |
| `/api/orders` | POST | Tạo đơn hàng mới |
| `/api/chat` | POST | Chatbot AI (Streaming SSE) |

### 5.2 API Response Examples

**GET /api/categories**
```json
[
  {"id": 1, "name": "Máy Tính Chơi Game", "icon": "ph-desktop"},
  {"id": 2, "name": "Màn Hình Máy Tính", "icon": "ph-monitor"}
]
```

**GET /api/products**
```json
[
  {
    "id": 1,
    "title": "PC Gaming Intel Core i5-13400F / RTX 4060 8GB",
    "brand": "Bigzone Custom",
    "price_current": 18990000,
    "price_old": 21500000,
    "discount_percent": 12,
    "image_url": "https://...",
    "stock": 15,
    "category_id": 1
  }
]
```

**POST /api/orders - Request**
```json
{
  "customer": {
    "name": "Nguyễn Văn A",
    "phone": "0912345678",
    "email": "a@example.com",
    "address": "123 Nguyễn Trãi, Q1, TP.HCM",
    "note": "Giao giờ hành chính",
    "payment": "cod"
  },
  "items": [
    {"id": 1, "title": "PC Gaming...", "price": 18990000, "quantity": 1}
  ],
  "total": 18990000
}
```

**POST /api/orders - Response**
```json
{"status": "success", "order_id": 1}
```

---

## 6. CHATBOT AI TƯ VẤN

### 6.1 Kiến trúc Chatbot

```
┌──────────────┐    ┌───────────────┐    ┌──────────────┐
│   User       │───►│  FastAPI      │───►│  Claude API  │
│   Message    │    │  /api/chat    │    │  (Opus 4)    │
└──────────────┘    └───────────────┘    └──────────────┘
                          │                    │
                          │              ┌─────▼─────┐
                          │              │ Tool:     │
                          │              │ search_   │
                          │              │ products  │
                          │              └─────┬─────┘
                          │                    │
                     ┌────▼────┐               │
                     │ SQLite  │◄──────────────┘
                     │   DB    │
                     └─────────┘
```

### 6.2 Tính năng Chatbot

| Tính năng | Mô tả |
|-----------|-------|
| **AI Model** | Claude Opus 4 (claude-opus-4-8) |
| **Tool Use** | Gọi search_products để lấy dữ liệu thật |
| **Streaming** | SSE (Server-Sent Events) phản hồi từng từ |
| **System Prompt** | Hướng dẫn AI tư vấn sản phẩm BigZone |
| **Ràng buộc** | Không bịa sản phẩm, luôn dùng dữ liệu DB |

### 6.3 Luồng hoạt động

1. User nhắn tin → gửi messages lên `/api/chat`
2. Server gọi Claude API với system prompt + history
3. Claude quyết định gọi `search_products` tool
4. Server thực thi SQL query, trả kết quả về Claude
5. Claude tổng hợp → stream text về client
6. Client hiển thị tin nhắn AI theo thời gian thực

### 6.4 Search Products Tool Schema

```json
{
  "name": "search_products",
  "description": "Tìm sản phẩm trong cửa hàng Bigzone...",
  "input_schema": {
    "type": "object",
    "properties": {
      "category_id": {"type": "integer"},
      "keyword": {"type": "string"},
      "min_price": {"type": "integer"},
      "max_price": {"type": "integer"},
      "max_results": {"type": "integer"}
    }
  }
}
```

### 6.5 Giao diện Chatbot

| Thành phần | Mô tả |
|------------|-------|
| **Widget** | Nút nổi góc phải màn hình |
| **Chat box** | Slide up khi click |
| **Messages** | User (phải), AI (trái) |
| **Typing indicator** | "Đang nhập..." khi chờ |
| **Product links** | Markdown link đến /product/{id} |

---

## 7. BẢO MẬT & TỐI ƯU

### 7.1 Bảo mật

| Tính năng | Mô tả chi tiết |
|-----------|----------------|
| **Mã hóa mật khẩu** | bcrypt với salt tự động |
| **JWT Token** | Lưu HttpOnly cookie, 7 ngày |
| **Xác thực giá server** | Không tin giá client, tính lại từ DB |
| **Kiểm tra tồn kho** | Server kiểm tra trước khi tạo đơn |
| **Phân quyền** | Route admin yêu cầu role='admin' |
| **XSS Protection** | HTML escape trong JavaScript |
| **Input Validation** | Pydantic validation ở tầng API |

### 7.2 Tối ưu hiệu năng

| Kỹ thuật | Mô tả |
|----------|-------|
| **SQLAlchemy ORM** | Query builder, tránh SQL injection |
| **Index trên trường tìm kiếm** | username, title, brand |
| **Pagination** | Giới hạn 12 sản phẩm/trang |
| **Lazy loading** | Chỉ load data khi cần |
| **Caching** | Static files mount trực tiếp |
| **Streaming response** | Chatbot SSE không block |

### 7.3 Database Index

```python
# User
username = Column(String, unique=True, index=True)

# Product  
title = Column(String, index=True)

# Category
name = Column(String, index=True)
```

---

## 8. ĐIỂM NỔI BẬT CỦA DỰ ÁN

### 8.1 Điểm nổi bật chính

#### 🎯 **1. Chatbot AI Tư Vấn Thông Minh**
- Sử dụng Claude Opus 4 - model AI mạnh nhất hiện nay
- **Tool Use**: Chatbot có thể truy vấn database thực tế
- **Không bịa đặt**: Luôn lấy dữ liệu sản phẩm từ DB
- **Streaming response**: Trả lời từng từ, không chờ load lâu
- **Context-aware**: Hiểu ngân sách, nhu cầu khách hàng

#### 🔒 **2. Bảo Mật Đa Lớp**
- Mật khẩu bcrypt (không lưu plain text)
- JWT HttpOnly cookie (chống XSS)
- Xác thực giá phía server (chống can thiệp)
- Kiểm tra tồn kho trước đặt hàng
- Phân quyền rõ ràng User/Admin

#### ⚡ **3. Performance Tối Ưu**
- FastAPI async - xử lý request nhanh
- Streaming SSE cho chatbot
- Pagination thông minh
- Static files served trực tiếp

#### 📱 **4. Giao Diện Responsive**
- Desktop: Grid 4-5 cột sản phẩm
- Tablet: Grid 2-3 cột
- Mobile: Grid 1-2 cột, hamburger menu
- Mobile-first CSS approach

#### 🎨 **5. UX Trải Nghiệm Người Dùng**
- Toast notifications cho mọi action
- Visual feedback khi thêm giỏ hàng
- Loading states rõ ràng
- Error messages thân thiện
- Floating contact buttons

### 8.2 Điểm khác biệt với các website TMĐT thông thường

| Tiêu chí | Website TMĐT thông thường | BigZone |
|----------|---------------------------|---------|
| **Chatbot** | ❌ Không có | ✅ AI tư vấn thông minh |
| **Tư vấn theo ngân sách** | ❌ Không | ✅ Claude hiểu và gợi ý |
| **Xác thực giá** | ⚠️ Thường dùng giá client | ✅ Server verify |
| **Tool Use AI** | ❌ Không | ✅ Truy vấn DB thật |
| **Streaming AI** | ❌ Không | ✅ Phản hồi real-time |

### 8.3 Các con số ấn tượng

| Chỉ số | Giá trị |
|--------|---------|
| Số danh mục | 8 |
| Số sản phẩm mẫu | 39 |
| Số tính năng chính | 25+ |
| Số trang HTML | 10+ |
| Dòng code JavaScript | 443 |
| Số API endpoint | 8+ |

---

## 9. CÔNG NGHỆ SỬ DỤNG

### 9.1 Backend Stack

| Công nghệ | Phiên bản | Mục đích |
|-----------|-----------|----------|
| **Python** | 3.10+ | Ngôn ngữ lập trình |
| **FastAPI** | Latest | Web framework async |
| **SQLAlchemy** | Latest | ORM |
| **Pydantic** | Latest | Data validation |
| **Uvicorn** | Latest | ASGI server |
| **python-jose** | Latest | JWT handling |
| **bcrypt** | Latest | Password hashing |

### 9.2 AI Stack

| Công nghệ | Mục đích |
|-----------|----------|
| **Anthropic Claude API** | AI model (Opus 4) |
| **Tool Use** | Gọi search_products từ AI |
| **SSE Streaming** | Real-time response |

### 9.3 Frontend Stack

| Công nghệ | Mục đích |
|-----------|----------|
| **HTML5** | Semantic markup |
| **CSS3** | Styling (12 module files) |
| **JavaScript (Vanilla)** | Interactivity, 0 dependencies |
| **Jinja2** | Server-side templating |
| **Phosphor Icons** | Icon library |
| **Google Fonts** | Inter font family |

### 9.4 Database

| Công nghệ | Mô tả |
|-----------|-------|
| **SQLite** | Embedded database |
| **SQLAlchemy** | ORM abstraction |

---

## 10. CẤU TRÚC DỰ ÁN

```
build_pc_bigzone/
│
├── backend/                    # FastAPI Backend
│   ├── __init__.py
│   ├── main.py                 # App init, public routes
│   ├── routers.py              # Auth & Admin routes
│   ├── models.py               # SQLAlchemy models
│   ├── schemas.py              # Pydantic schemas
│   ├── auth.py                 # JWT & bcrypt functions
│   ├── database.py             # SQLite connection
│   ├── chatbot.py              # Claude AI integration
│   ├── seed.py                 # Sample data generator
│   ├── requirements.txt        # Python dependencies
│   └── pcmarket.db             # SQLite database
│
├── templates/                  # Jinja2 HTML Templates
│   ├── base.html               # Base template
│   ├── pages/                  # User-facing pages
│   │   ├── home.html           # Homepage
│   │   ├── category.html       # Category listing
│   │   ├── product.html        # Product detail
│   │   ├── cart.html           # Shopping cart
│   │   ├── checkout.html       # Checkout form
│   │   ├── search.html         # Search results
│   │   ├── login.html          # Login page
│   │   ├── register.html       # Register page
│   │   └── order_success.html # Order confirmation
│   ├── admin/                  # Admin pages
│   │   ├── base.html           # Admin base
│   │   ├── dashboard.html      # Admin dashboard
│   │   ├── products_list.html  # Products management
│   │   └── product_form.html   # Add/Edit product
│   └── components/             # Reusable components
│       ├── header.html         # Site header
│       └── footer.html         # Site footer
│
├── static/                      # Static assets
│   ├── css/                    # 12 CSS module files
│   │   ├── reset.css           # CSS reset
│   │   ├── variables.css        # CSS custom properties
│   │   ├── layout.css          # Layout utilities
│   │   ├── components.css      # Reusable components
│   │   ├── header.css          # Header styles
│   │   ├── home.css            # Homepage styles
│   │   ├── category.css        # Category page styles
│   │   ├── product.css          # Product page styles
│   │   ├── cart.css            # Cart styles
│   │   ├── checkout.css        # Checkout styles
│   │   ├── footer.css           # Footer styles
│   │   └── chatbot.css         # Chatbot widget styles
│   ├── js/                     # JavaScript files
│   │   ├── main.js             # Core logic (443 lines)
│   │   └── chatbot.js         # Chatbot interaction
│   └── images/                # Static images
│
├── document/                   # Documentation
│   ├── BẢNG_CÁO_GỬI_THẦY.md  # Progress report
│   ├── BAO_CAO_TIEN_DO_DATN.md # Thesis progress
│   ├── HUONG_DAN_SU_DUNG.md    # User guide
│   ├── Đề Cương ĐATN...docx    # Thesis outline
│   └── TÀI_LIỆU_TÍNH_NĂNG...md # This file
│
├── logo-bigzone.png            # Logo image
├── .gitignore                  # Git ignore rules
└── README.md                   # Project readme
```

---

## PHỤ LỤC

### A. Tài khoản mẫu

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | admin |

### B. Chạy dự án

```bash
# 1. Cài đặt dependencies
cd backend
pip install -r requirements.txt

# 2. Tạo dữ liệu mẫu
python seed.py

# 3. Khởi động server
uvicorn main:app --reload

# 4. Truy cập
# http://localhost:8000
# http://localhost:8000/admin
```

### C. Cấu hình biến môi trường

```bash
# Backend (.env hoặc system)
ANTHROPIC_API_KEY=your_api_key_here
```

### D. Các file CSS modules

1. `reset.css` - Reset CSS browser defaults
2. `variables.css` - CSS custom properties (colors, spacing)
3. `layout.css` - Container, grid, utilities
4. `components.css` - Buttons, cards, badges
5. `header.css` - Header navigation styles
6. `home.css` - Homepage specific styles
7. `category.css` - Category listing styles
8. `product.css` - Product detail styles
9. `cart.css` - Shopping cart styles
10. `checkout.css` - Checkout form styles
11. `footer.css` - Footer styles
12. `chatbot.css` - Chat widget styles

---

**Tài liệu được tạo**: 2026-06-18
**Phiên bản dự án**: 1.0
**Trạng thái**: Hoàn thành

---

> **BigZone** — Xây dựng PC trong mơ của bạn!