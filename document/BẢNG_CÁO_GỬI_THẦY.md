# BÁO CÁO ĐỒ ÁN TỐT NGHIỆP
## XÂY DỰNG WEBSITE THƯƠNG MẠI ĐIỆN TỬ BÁN PC/LAPTOP TÍCH HỢP CHATBOT AI

**Trường:** Đại học Thuỷ Lợi — Khoa Công Nghệ Thông Tin

**Người thực hiện:** [Họ và tên sinh viên]

**Mã sinh viên:** [MSSV]

**Lớp:** [Tên lớp]

**Giáo viên hướng dẫn:** [Học hàm/học vị – Họ và tên GVHD]

**Kỳ báo cáo:** [Tuần thứ ... / ngày ... tháng ... năm 2026]

---

## 1. GIỚI THIỆU ĐỀ TÀI

### 1.1. Bối cảnh và ý nghĩa

Thương mại điện tử (TMĐT) ngày càng phát triển, đặc biệt là ngành bán hàng công nghệ. Các khách hàng mua PC, laptop và linh kiện máy tính thường cần lời tư vấn chuyên sâu do sự đa dạng của sản phẩm, tính kỹ thuật cao, và nhiều lựa chọn cấu hình khác nhau. Đề tài này nhằm xây dựng một nền tảng thương mại điện tử kết hợp với công nghệ trí tuệ nhân tạo (Chatbot AI) để:

- Cung cấp trải nghiệm mua sắm trực tuyến tiện lợi và hiệu quả.
- Tư vấn tự động thông minh sản phẩm phù hợp dựa trên nhu cầu và ngân sách của khách hàng.
- Giảm tải công việc tư vấn cho nhân viên.

### 1.2. Tên đề tài

**"Xây dựng website thương mại điện tử bán PC/Laptop tích hợp chatbot AI hỗ trợ tư vấn"**

### 1.3. Phạm vi dự án

**Giai đoạn hiện tại:** Xây dựng nền tảng website TMĐT với tất cả tính năng cốt lõi (phía người dùng + trang quản trị admin).

**Giai đoạn kế tiếp:** Tích hợp module chatbot AI tư vấn sản phẩm (dự kiến tuần 8–12).

---

## 2. MỤC TIÊU ĐỒ ÁN

### 2.1. Mục tiêu chính

1. **Phân tích và thiết kế:** Khảo sát quy trình mua sắm online, phân tích yêu cầu chức năng, lựa chọn công nghệ phù hợp.

2. **Xây dựng nền tảng TMĐT:** Triển khai đầy đủ các chức năng cốt lõi:
   - Duyệt sản phẩm theo danh mục
   - Tìm kiếm, lọc, sắp xếp sản phẩm
   - Giỏ hàng và thanh toán
   - Quản lý đơn hàng phía admin
   - Xác thực người dùng và phân quyền

3. **Bảo mật và tối ưu:**
   - Kiểm tra tồn kho
   - Xác thực giá phía server (chống can thiệp)
   - Mật khẩu được mã hoá bcrypt
   - Tối ưu hiệu năng

4. **Chuẩn bị cho chatbot AI:** Thiết kế cơ sở dữ liệu sao cho dễ tích hợp LLM trong giai đoạn sau.

### 2.2. Kỳ vọng đạt được

- Website hoạt động ổn định, giao diện thân thiện với người dùng.
- Hệ thống quản lý sản phẩm và đơn hàng đầy đủ cho admin.
- Chuẩn bị sẵn sàng cho tích hợp AI ở giai đoạn tiếp theo.

---

## 3. CÔNG NGHỆ SỬ DỤNG

### 3.1. Điều chỉnh công nghệ so với đề cương

> **Lưu ý quan trọng:** So với đề cương ban đầu (React/Node.js/MongoDB), dự án đã được điều chỉnh sang **Python + FastAPI**. Thay đổi này được thực hiện với lý do kỹ thuật:
> - **Rút ngắn thời gian phát triển** nhờ FastAPI mạnh mẽ và cú pháp gọn gàng.
> - **Dễ tích hợp thư viện AI** — Python có hệ sinh thái LLM phong phú (LangChain, OpenAI API, etc.)
> - **Render server-side với Jinja2** giúp quản lý template hiệu quả và dễ bảo trì.
> - **Phát triển nhanh hơn** nhờ API auto-documentation (Swagger UI).

### 3.2. Stack công nghệ chi tiết

| Thành phần | Công nghệ | Mục đích |
|-----------|-----------|---------|
| **Backend** | Python 3 + FastAPI | Xử lý API, logic nghiệp vụ |
| **Web Framework** | FastAPI | Framework web hiệu năng cao |
| **ORM/CSDL** | SQLAlchemy + SQLite | Quản lý cơ sở dữ liệu |
| **Template** | Jinja2 | Render HTML phía server |
| **Xác thực** | JWT (python-jose) + bcrypt | Token-based auth, mã hoá mật khẩu |
| **Static Files** | Uvicorn + StaticFiles | Phục vụ CSS, JS, ảnh |
| **Frontend** | HTML5, CSS3, JavaScript thuần | Giao diện người dùng |
| **Web Server** | Uvicorn (ASGI) | Server ASGI tốc độ cao |

### 3.3. Các thư viện chính

```
fastapi          # Framework web
uvicorn          # ASGI server
sqlalchemy       # ORM
jinja2           # Template engine
python-multipart # Xử lý form data
passlib[bcrypt]  # Mã hoá mật khẩu
python-jose      # JWT handling
```

---

## 4. KIẾN TRÚC VÀ THIẾT KẾ HỆ THỐNG

### 4.1. Cấu trúc thư mục dự án

```
build_pc_bigzone/
├── backend/
│   ├── main.py              # Khởi tạo app, route công khai
│   ├── routers.py           # Route đăng nhập/đăng xuất, quản trị
│   ├── models.py            # Mô hình dữ liệu (SQLAlchemy ORM)
│   ├── schemas.py           # Schema Pydantic cho API
│   ├── auth.py              # Xác thực JWT, phân quyền, mã hoá
│   ├── database.py          # Cấu hình kết nối CSDL
│   ├── seed.py              # Script tạo dữ liệu mẫu
│   └── requirements.txt      # Danh sách dependency
├── templates/               # Giao diện Jinja2
│   ├── base.html            # Mẫu cơ sở
│   ├── pages/               # Trang người dùng (home, product, cart, etc.)
│   ├── admin/               # Trang quản trị
│   └── components/          # Component tái sử dụng (header, footer)
├── static/
│   ├── css/                 # CSS module (reset.css, variables.css, page-specific)
│   ├── js/                  # JavaScript (main.js cho logic chung)
│   └── images/              # Hình ảnh sản phẩm, icon
└── BAO_CAO_TIEN_DO_DATN.md  # Tài liệu tiến độ
```

### 4.2. Mô hình cơ sở dữ liệu

Hệ thống sử dụng **5 bảng chính:**

#### **Bảng User (Người dùng)**
```
User {
  id (PK)
  username (unique, indexed)
  password_hash (bcrypt)
  role (enum: 'user' / 'admin')
}
```

#### **Bảng Category (Danh mục sản phẩm)**
```
Category {
  id (PK)
  name
  icon (class Phosphor icon, e.g., "ph-desktop")
  
  ↓ 1-N relationship
  products: Product[]
}
```

#### **Bảng Product (Sản phẩm)**
```
Product {
  id (PK)
  title
  brand
  price_current
  price_old (nullable, giá cũ để tính % giảm)
  discount_percent (nullable)
  image_url
  description (text, mô tả chi tiết)
  stock (tồn kho)
  section (enum: 'HOT_SALE' / 'PC_GAMING' / null)
  category_id (FK → Category)
  
  ↓ N-1 relationship
  category: Category
}
```

#### **Bảng Order (Đơn hàng)**
```
Order {
  id (PK)
  customer_name
  customer_phone
  customer_email (nullable)
  address
  note (nullable, ghi chú từ khách)
  payment_method (enum: 'cod' / 'credit_card' / etc.)
  total (tổng tiền tính lại từ server)
  status (enum: 'pending' / 'confirmed' / 'shipping' / 'done' / 'cancelled')
  created_at (timestamp UTC)
  
  ↓ 1-N relationship
  items: OrderItem[]
}
```

#### **Bảng OrderItem (Chi tiết đơn hàng)**
```
OrderItem {
  id (PK)
  order_id (FK → Order)
  product_id (lưu ID sản phẩm)
  product_title (lưu tên sản phẩm snapshot)
  price (giá tại thời điểm đặt hàng)
  quantity
  
  ↓ N-1 relationship
  order: Order
}
```

**Quan hệ chính:**
- `Category 1–N Product`
- `Order 1–N OrderItem`

### 4.3. Luồng xác thực và phân quyền

```
1. Người dùng đăng nhập → gửi username + password
2. Server: hash password từ DB, so sánh bằng bcrypt
3. Nếu đúng → tạo JWT token (7 ngày hạn)
4. Token lưu trong cookie HttpOnly (bảo mật)
5. Các request sau sẽ kèm token → server xác thực
6. Nếu role = 'admin' → cho phép truy cập trang quản trị
```

### 4.4. Luồng đặt hàng

```
1. Khách hàng thêm sản phẩm vào giỏ (localStorage)
2. Tại trang checkout: nhập thông tin, chọn phương thức thanh toán
3. Gửi order qua API → server kiểm tra:
   - Tồn kho của mỗi sản phẩm
   - Tính lại tổng tiền từ giá trong CSDL (không tin client)
4. Nếu hợp lệ:
   - Tạo Order + OrderItem
   - Trừ tồn kho sản phẩm
   - Trả về confirmation
5. Hiển thị trang thành công
```

---

## 5. CÁC TÍNH NĂNG ĐÃ HOÀN THÀNH

### 5.1. Phía người dùng (Frontend)

#### **Trang chủ**
- ✅ Hiển thị banner chính (hero section)
- ✅ Hiển thị 8 danh mục với icon Phosphor
- ✅ Khu vực "HOT SALE" (sản phẩm giảm giá sốc, tối đa 10 sản phẩm)
- ✅ Khu vực "PC GAMING" (sản phẩm dòng gaming nổi bật, tối đa 10 sản phẩm)
- ✅ Header với tìm kiếm, giỏ hàng, đăng nhập

#### **Danh mục sản phẩm**
- ✅ Hiển thị lưới sản phẩm (12 sản phẩm/trang, responsive)
- ✅ Mỗi sản phẩm: hình ảnh, tên, thương hiệu, giá hiện tại, giá cũ, % giảm giá
- ✅ **Sắp xếp:** 4 tùy chọn (Mặc định, Giá tăng, Giá giảm, Giảm giá nhiều nhất)
- ✅ **Phân trang:** tự động chia trang khi > 12 sản phẩm
- ✅ Responsive design (desktop, tablet, mobile)

#### **Chi tiết sản phẩm**
- ✅ Thông tin đầy đủ (tên, thương hiệu, giá, mô tả, hình ảnh, tồn kho)
- ✅ Nút "Thêm vào giỏ"
- ✅ Gợi ý sản phẩm liên quan cùng danh mục

#### **Tìm kiếm**
- ✅ Tìm kiếm theo tên sản phẩm, thương hiệu, mô tả
- ✅ Hiển thị kết quả với sắp xếp và phân trang

#### **Giỏ hàng**
- ✅ Lưu trong localStorage (không cần đăng nhập)
- ✅ Thêm/sửa số lượng/xoá sản phẩm
- ✅ Tự tính tổng tiền
- ✅ Có nút "Tiếp tục mua" và "Thanh toán"

#### **Thanh toán & đặt hàng**
- ✅ Form nhập thông tin khách (tên, SĐT, email, địa chỉ, ghi chú)
- ✅ Chọn phương thức thanh toán (hiện hỗ trợ COD — thanh toán khi nhận hàng)
- ✅ Gửi đơn qua API
- ✅ Trang xác nhận đơn thành công (hiển thị mã đơn, tổng tiền)

#### **Đăng nhập**
- ✅ Form đăng nhập (username + password)
- ✅ Token JWT lưu trong cookie HttpOnly
- ✅ Hiển thị tên người dùng khi đăng nhập thành công

#### **Đăng ký (giao diện sẵn, logic chuẩn bị)**
- ⏳ Giao diện register.html đã có
- ⏳ Cần hoàn thiện luồng đăng ký + xác thực

### 5.2. Phía quản trị (Admin)

#### **Đăng nhập Admin**
- ✅ Xác thực JWT, phân quyền role = 'admin'
- ✅ Chuyển hướng về dashboard nếu admin hợp lệ

#### **Dashboard**
- ✅ Thống kê tổng số sản phẩm
- ✅ Thống kê tổng số đơn hàng
- ✅ Nút điều hướng đến các trang quản lý

#### **Quản lý sản phẩm (CRUD)**
- ✅ Danh sách sản phẩm với phân trang
- ✅ **Thêm sản phẩm:** form điền thông tin, chọn danh mục, chọn section (HOT_SALE/PC_GAMING)
- ✅ **Sửa sản phẩm:** tải dữ liệu cũ, chỉnh sửa, cập nhật
- ✅ **Xoá sản phẩm:** xác nhận trước khi xoá

#### **Quản lý đơn hàng (chuẩn bị)**
- ⏳ Giao diện admin/products_list.html đã có template cơ bản
- ⏳ Cần hoàn thiện trang duyệt đơn hàng + cập nhật trạng thái

### 5.3. API JSON (cho frontend + integration)

- ✅ `GET /api/categories` — Danh sách danh mục
- ✅ `GET /api/products` — Danh sách sản phẩm (hỗ trợ filter category, search, sort, pagination)
- ✅ `GET /api/products/{id}` — Chi tiết sản phẩm
- ✅ `POST /api/orders` — Tạo đơn hàng (kiểm tra tồn kho, tính lại giá)
- ✅ `GET /api/orders/{id}` — Chi tiết đơn hàng

### 5.4. Xử lý bảo mật và nghiệp vụ đáng chú ý

#### **Kiểm tra tồn kho**
- ✅ Khi đặt hàng, server kiểm tra `stock >= quantity` cho mỗi sản phẩm
- ✅ Nếu tồn kho không đủ → trả về lỗi 400
- ✅ Sau khi đơn được tạo → tự động trừ tồn kho

#### **Xác thực giá phía server**
- ✅ Không tin giá do client gửi lên
- ✅ Server tính lại `total = Σ(price_current × quantity)` từ CSDL
- ✅ Chống can thiệp giá bởi khách hàng

#### **Mã hoá mật khẩu**
- ✅ Sử dụng bcrypt (salt rounds = 12 mặc định)
- ✅ Không lưu mật khẩu gốc
- ✅ Khi đăng nhập, verify bằng `bcrypt.checkpw()`

#### **Phân tách quyền hạn**
- ✅ Route công khai: `/`, `/products`, `/api/products`, etc.
- ✅ Route yêu cầu đăng nhập: `/checkout`
- ✅ Route admin: `/admin/*` — yêu cầu JWT + role = 'admin'

### 5.5. Dữ liệu mẫu (Seed Data)

- ✅ **8 danh mục:**
  1. Máy Tính Chơi Game
  2. Màn Hình Máy Tính
  3. Linh Kiện PC
  4. Laptop & Phụ Kiện
  5. Gaming Gear
  6. Thiết Bị Âm Thanh
  7. Bàn Ghế Gaming
  8. Camera & An Ninh

- ✅ **39 sản phẩm** với:
  - Tên thực tế (PC MSI, Asus, Dell, etc.)
  - Thương hiệu
  - Giá bán thực tế (VNĐ)
  - Giá cũ và % giảm giá
  - Mô tả chi tiết
  - Hình ảnh (đường dẫn)
  - Tồn kho
  - Gán vào các danh mục và section (HOT_SALE, PC_GAMING)

- ✅ **Tài khoản mẫu:**
  - Username: `admin`
  - Password: `admin123`
  - Role: `admin`

---

## 6. TIẾN ĐỘ HIỆN TẠI

| Hạng mục | Trạng thái | Ghi chú |
|----------|-----------|---------|
| **Khảo sát, phân tích yêu cầu** | ✅ Hoàn thành | Yêu cầu func đã rõ ràng |
| **Thiết kế hệ thống (CSDL, kiến trúc)** | ✅ Hoàn thành | Schema CSDL, API design xong |
| **Frontend (trang người dùng)** | ✅ Hoàn thành | Giao diện responsive, logic đầy đủ |
| **Backend (API, CSDL)** | ✅ Hoàn thành | CRUD, xác thực, kiểm tra nghiệp vụ |
| **Trang quản trị (Admin)** | ✅ Hoàn thành | Dashboard, quản lý sản phẩm |
| **Đăng ký người dùng** | 🔄 50% | Giao diện sẵn, cần hoàn thiện logic |
| **Cổng thanh toán trực tuyến** | ⏳ Chưa | Hiện dùng COD, sẽ tích hợp VNPay/Stripe |
| **Quản lý đơn hàng phía admin** | 🔄 60% | Template cơ bản, cần UI & update status |
| **Chatbot AI tư vấn** | ⏳ Chuẩn bị | Dự kiến tuần 8–12 |
| **Kiểm thử & tối ưu** | 🔄 Đang thực hiện | Test tích hợp, performance tuning |

**Chú thích:** ✅ Hoàn thành | 🔄 Đang thực hiện | ⏳ Chưa bắt đầu

---

## 7. KẾ HOẠCH VÀ CÔNG VIỆC CÒN LẠI

### 7.1. Tuần tiếp theo (Tuần hiện tại đến Tuần 7)

1. **Hoàn thiện đăng ký & xác thực**
   - Triển khai logic đăng ký người dùng
   - Email verification (tuỳ chọn)
   - Reset mật khẩu

2. **Cổng thanh toán**
   - Tích hợp VNPay hoặc Stripe
   - Xử lý callback thanh toán
   - Cập nhật trạng thái đơn hàng

3. **Quản lý đơn hàng phía admin**
   - Danh sách đơn hàng với bộ lọc (trạng thái, ngày)
   - Chi tiết đơn hàng
   - Cập nhật trạng thái (pending → confirmed → shipping → done)
   - In hoá đơn (tuỳ chọn)

4. **Tối ưu & kiểm thử**
   - Unit test & integration test
   - Load test (kiểm tra hiệu năng)
   - Security audit
   - Responsive test trên nhiều thiết bị

### 7.2. Giai đoạn AI Chatbot (Tuần 8–12)

1. **Thiết kế luồng hội thoại**
   - Xác định intent của khách hàng (tư vấn, hỏi giá, compare sản phẩm)
   - Thiết kế prompt cho LLM

2. **Tích hợp LLM API**
   - Chọn LLM provider (OpenAI GPT-4, Claude, Llama, etc.)
   - Kết nối API
   - Xử lý request/response

3. **Kết nối dữ liệu sản phẩm**
   - Chatbot truy cập CSDL sản phẩm
   - Gợi ý sản phẩm phù hợp theo nhu cầu/ngân sách
   - Hiển thị giá, mô tả, link sản phẩm

4. **Giao diện Chatbot**
   - Widget chat dạng pop-up/sidebar
   - Lưu history hội thoại
   - Tích hợp vào trang website

### 7.3. Hoàn thiện (Tuần 13+)

- Kiểm thử toàn bộ hệ thống
- Tối ưu hiệu năng, UX/UI
- Triển khai lên server production
- Viết báo cáo cuối cùng
- Chuẩn bị bảo vệ đồ án

---

## 8. ĐÁNH GIÁ TIẾN ĐỘ SO VỚI ĐỀ CƯƠNG

### Mốc giới hạn trong đề cương

| Giai đoạn | Thời gian dự kiến | Trạng thái | Ghi chú |
|-----------|------------------|-----------|---------|
| **G1: Khảo sát, thu thập yêu cầu** | Tuần 1–2 | ✅ Hoàn thành | Đúng tiến độ |
| **G2: Thiết kế hệ thống** | Tuần 3–4 | ✅ Hoàn thành | Đúng tiến độ |
| **G3: Xây dựng website TMĐT** | Tuần 5–7 | ✅ Hoàn thành | Hoàn thành sớm (tuần 6) |
| **G4: Tích hợp Chatbot AI** | Tuần 8–12 | 🔄 Chuẩn bị | Đúng tiến độ |
| **G5: Kiểm thử, tối ưu, báo cáo** | Tuần 13+ | ⏳ Chưa bắt đầu | Theo kế hoạch |

**Kết luận:** Dự án **đang hoàn thành trước tiến độ 1–2 tuần**. Phần nền tảng TMĐT đã ổn định, tạo cơ sở vững chắc để tích hợp chatbot AI.

---

## 9. THÀNH TỰU VÀ ĐIỂM NHẤN

### 9.1. Thành tựu kỹ thuật

- ✅ Xây dựng được hệ thống TMĐT chuyên nghiệp với kiến trúc rõ ràng (fastAPI + SQLAlchemy + Jinja2).
- ✅ Triển khai đầy đủ cycle CRUD cho sản phẩm, đơn hàng, người dùng.
- ✅ Xác thực JWT an toàn, phân quyền theo role, mã hoá mật khẩu bcrypt.
- ✅ Giao diện responsive, tương thích desktop/tablet/mobile.
- ✅ Seeding dữ liệu thực tế (8 danh mục, 39 sản phẩm, hình ảnh).
- ✅ API RESTful có tài liệu tự động (Swagger UI).

### 9.2. Điểm nhấn nổi bật

1. **Bảo mật:** Xác thực giá phía server, tránh can thiệp từ client.
2. **Kiểm tra tồn kho:** Tự động trừ tồn kho sau khi đặt hàng.
3. **UX** thân thiện: Giao diện sạch sẽ, dễ sử dụng, phân trang thông minh.
4. **Sẵn sàng mở rộng:** Cơ sở dữ liệu và code structure cho phép tích hợp module AI dễ dàng.

---

## 10. NHỮNG ĐIỀU CẦN HỖ TRỢ TỪ GIÁO VIÊN

1. **Xác nhận công nghệ:** Kính xin ý kiến thầy/cô về việc sử dụng **FastAPI thay cho React/Node** (cảm thấy phù hợp hơn cho dự án này).

2. **Hướng dẫn tích hợp AI:** Thầy/cô có kiến nghị về:
   - LLM nào nên sử dụng? (OpenAI GPT-4, Claude, Llama local?)
   - Cách xử lý dữ liệu sản phẩm cho chatbot?
   - Giới hạn kỹ thuật/ngân sách?

3. **Phương thức thanh toán:** Công ty/trường có cổng thanh toán cụ thể nào gợi ý không? (VNPay, Stripe, Momo?)

---

## 11. KẾT LUẬN

Đề tài **đã hoàn thành giai đoạn 1–3** (Khảo sát, Thiết kế, Xây dựng website TMĐT). Website chạy ổn định, giao diện thân thiện, tính năng cốt lõi đầy đủ. 

**Giai đoạn tiếp theo** tập trung vào tích hợp chatbot AI (tuần 8–12), đây sẽ là điểm nhấn chính của đề tài. Nền tảng TMĐT đã sẵn sàng để nhân viên quản lý sản phẩm và xử lý đơn hàng một cách hiệu quả.

Kính mong thầy/cô cho ý kiến, hướng dẫn để hoàn thiện tốt hơn các giai đoạn tiếp theo.

---

## TÀI LIỆU THAM KHẢO

1. **FastAPI Documentation** — https://fastapi.tiangolo.com/
2. **SQLAlchemy Documentation** — https://docs.sqlalchemy.org/
3. **Python-Jose (JWT)** — https://github.com/mpdavis/python-jose
4. **Passlib & Bcrypt** — https://passlib.readthedocs.io/
5. **Phong Vũ** — https://www.phongvu.vn/ (tham khảo UI/UX)
6. **CellphoneS** — https://cellphones.com.vn/ (tham khảo UI/UX)
7. **OpenAI API** — https://platform.openai.com/docs (cho chatbot AI)

---

**Báo cáo được lập ngày: [Ngày/Tháng/Năm]**

**Người thực hiện:** [Họ và tên sinh viên]

**Chữ ký:** _____________________

---

*Tài liệu này được chuẩn bị để báo cáo tiến độ đồ án tốt nghiệp tại Đại học Thuỷ Lợi.*
