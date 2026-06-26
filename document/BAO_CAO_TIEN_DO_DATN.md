# BÁO CÁO TIẾN ĐỘ ĐỒ ÁN TỐT NGHIỆP

**Trường:** Đại học Thuỷ Lợi — Khoa Công nghệ Thông tin

**Tên đề tài:** Xây dựng website thương mại điện tử bán PC/Laptop tích hợp chatbot AI hỗ trợ tư vấn

| Thông tin | Nội dung |
|-----------|----------|
| Sinh viên thực hiện | [Họ và tên sinh viên] |
| Lớp | [Tên lớp] |
| Mã sinh viên | [MSSV] |
| Giáo viên hướng dẫn | [Học hàm/học vị – Họ và tên GVHD] |
| Kỳ báo cáo | [Tuần thứ ... / ngày ... tháng ... năm 2026] |

---

## 1. Giới thiệu đề tài

Trong bối cảnh thương mại điện tử phát triển mạnh và nhu cầu mua sắm thiết bị công
nghệ (PC, laptop, linh kiện) ngày càng tăng, đề tài hướng tới xây dựng một hệ thống
bán hàng trực tuyến chuyên biệt cho mặt hàng PC/Laptop. Hệ thống cho phép người dùng
duyệt sản phẩm theo danh mục, tìm kiếm – lọc – sắp xếp, thêm vào giỏ hàng, đặt hàng
và thanh toán; đồng thời cung cấp trang quản trị (admin) để quản lý sản phẩm và đơn
hàng. Giai đoạn tiếp theo của đề tài sẽ tích hợp module chatbot AI dựa trên mô hình
ngôn ngữ lớn (LLM) để tư vấn sản phẩm theo nhu cầu và ngân sách của khách hàng.

---

## 2. Mục tiêu và phạm vi

**Mục tiêu:**

1. Phân tích quy trình xây dựng website TMĐT và lựa chọn công nghệ phù hợp.
2. Thiết kế kiến trúc hệ thống, cơ sở dữ liệu và giao diện người dùng.
3. Xây dựng đầy đủ các chức năng TMĐT cốt lõi (sản phẩm, giỏ hàng, đặt hàng, quản trị).
4. Tích hợp chatbot AI tư vấn sản phẩm (giai đoạn kế tiếp).
5. Kiểm thử, tối ưu và hoàn thiện báo cáo, chuẩn bị bảo vệ.

**Phạm vi hiện tại:** Hoàn thành phần website TMĐT (frontend + backend + trang quản
trị). Phần chatbot AI đang ở giai đoạn chuẩn bị triển khai.

---

## 3. Công nghệ sử dụng

> **Lưu ý:** Trong quá trình thực hiện, nhóm/sinh viên đã điều chỉnh stack công nghệ
> so với đề cương ban đầu (đề cương dự kiến React/Node.js/MongoDB) sang stack
> **Python + FastAPI** nhằm rút ngắn thời gian phát triển, tận dụng khả năng render
> server-side (Jinja2) và dễ tích hợp thư viện AI ở giai đoạn sau. Đây là thay đổi
> đã được cân nhắc về mặt kỹ thuật, cần xin ý kiến GVHD để thống nhất.

| Thành phần | Công nghệ |
|------------|-----------|
| Ngôn ngữ | Python 3 |
| Web framework | FastAPI |
| ORM / CSDL | SQLAlchemy + SQLite (`pcmarket.db`) |
| Template engine | Jinja2 (render server-side) |
| Xác thực | JWT (python-jose) + băm mật khẩu bcrypt |
| Frontend | HTML5, CSS3 (module hoá theo trang), JavaScript thuần |
| Web server | Uvicorn (ASGI) |

---

## 4. Kiến trúc và thiết kế hệ thống

### 4.1. Cấu trúc thư mục

```
build_pc_bigzone/
├── backend/
│   ├── main.py          # Khởi tạo app, route public + API
│   ├── routers.py       # Route đăng nhập/đăng xuất + quản trị (admin)
│   ├── models.py        # Mô hình dữ liệu (SQLAlchemy ORM)
│   ├── schemas.py       # Pydantic schema cho API
│   ├── auth.py          # Xác thực JWT, băm mật khẩu, phân quyền
│   ├── database.py      # Cấu hình kết nối CSDL
│   ├── seed.py          # Script tạo dữ liệu mẫu
│   └── requirements.txt
├── templates/           # Giao diện Jinja2 (trang người dùng + admin)
├── static/              # CSS, JS, hình ảnh
└── ...
```

### 4.2. Mô hình cơ sở dữ liệu

Hệ thống gồm 5 bảng chính:

- **User** — tài khoản, mật khẩu băm, phân quyền (`user` / `admin`).
- **Category** — danh mục sản phẩm (tên, icon).
- **Product** — sản phẩm (tên, thương hiệu, giá hiện tại/giá cũ, % giảm, ảnh, mô tả, tồn kho, nhóm hiển thị, khoá ngoại danh mục).
- **Order** — đơn hàng (thông tin khách, địa chỉ, phương thức thanh toán, tổng tiền, trạng thái, thời gian tạo).
- **OrderItem** — chi tiết từng dòng sản phẩm trong đơn hàng.

Quan hệ: `Category 1–N Product`, `Order 1–N OrderItem`.

---

## 5. Kết quả đã đạt được

### 5.1. Chức năng phía người dùng (đã hoàn thành)

- **Trang chủ:** hiển thị nhóm sản phẩm "Hot Sale" và "PC Gaming".
- **Trang danh mục:** lọc theo danh mục, **sắp xếp** (giá tăng/giảm, theo mức giảm giá), **phân trang** (12 sản phẩm/trang).
- **Trang chi tiết sản phẩm:** thông tin đầy đủ + gợi ý sản phẩm liên quan.
- **Tìm kiếm:** theo tên, thương hiệu, mô tả; có sắp xếp và phân trang.
- **Giỏ hàng:** lưu phía client (localStorage), thêm/sửa số lượng/xoá, tự tính tổng tiền.
- **Thanh toán & đặt hàng:** gửi đơn qua API, có trang xác nhận đơn thành công.
- **API JSON:** `/api/categories`, `/api/products` (lọc theo danh mục/nhóm/từ khoá), `/api/orders`.

### 5.2. Trang quản trị (đã hoàn thành)

- Đăng nhập bằng JWT lưu trong cookie HttpOnly, phân quyền admin.
- Dashboard thống kê tổng số sản phẩm và đơn hàng.
- **Quản lý sản phẩm (CRUD):** thêm / sửa / xoá, gán danh mục và nhóm hiển thị.

### 5.3. Xử lý nghiệp vụ và bảo mật đáng chú ý

- **Kiểm tra tồn kho** khi đặt hàng; tự động **trừ tồn kho** sau khi đơn được tạo.
- **Xác thực giá phía server:** tổng tiền đơn hàng được tính lại từ giá trong CSDL,
  không tin giá do client gửi lên (chống can thiệp giá).
- **Mật khẩu băm bằng bcrypt**, không lưu mật khẩu gốc.
- Phân tách rõ route công khai / route quản trị qua dependency phân quyền.

### 5.4. Dữ liệu mẫu

CSDL đã được seed với **8 danh mục** (Máy tính chơi game, Màn hình, Linh kiện PC,
Laptop & phụ kiện, Gaming gear, Thiết bị âm thanh, Bàn ghế gaming, Camera & an ninh)
và **39 sản phẩm** kèm hình ảnh, giá, mô tả thực tế. Tài khoản admin mặc định phục vụ
demo (`admin` / `admin123`).

---

## 6. Phần chưa hoàn thành / công việc tiếp theo

| Hạng mục | Trạng thái | Kế hoạch |
|----------|-----------|----------|
| **Chatbot AI tư vấn (LLM)** | Chưa triển khai | Thiết kế luồng hội thoại, tích hợp LLM API, kết nối dữ liệu sản phẩm thực để gợi ý theo nhu cầu/ngân sách |
| Đăng ký người dùng cuối | Có giao diện, cần hoàn thiện luồng | Hoàn thiện đăng ký + xác thực |
| Cổng thanh toán trực tuyến | Hiện hỗ trợ COD | Tích hợp cổng thanh toán (VNPay/Stripe) |
| Quản lý đơn hàng phía admin | Chưa có giao diện duyệt đơn | Bổ sung trang quản lý & cập nhật trạng thái đơn |
| Kiểm thử & tối ưu | Đang thực hiện | Kiểm thử tích hợp, tối ưu hiệu năng, triển khai cloud |

---

## 7. Đánh giá tiến độ so với kế hoạch

So với tiến độ trong đề cương:

- ✅ **Giai đoạn 1 – Khảo sát, thu thập yêu cầu:** hoàn thành.
- ✅ **Giai đoạn 2 – Thiết kế hệ thống (CSDL, kiến trúc, giao diện):** hoàn thành.
- ✅ **Giai đoạn 3 – Xây dựng website (module chính TMĐT):** hoàn thành phần cốt lõi
  (riêng cổng thanh toán trực tuyến đang dùng COD, sẽ tích hợp sau).
- 🔄 **Giai đoạn 4 – Chatbot AI:** chuẩn bị triển khai (đúng theo mốc tuần 8–12).
- ⏳ **Giai đoạn 5 – Kiểm thử, tối ưu, hoàn thiện báo cáo:** sẽ thực hiện sau khi xong chatbot.

**Đánh giá chung:** Tiến độ bám sát kế hoạch. Phần nền tảng TMĐT đã chạy ổn định, tạo
cơ sở thuận lợi để tích hợp chatbot AI trong giai đoạn tới.

---

## 8. Hướng phát triển và kiến nghị

1. Triển khai module chatbot AI là trọng tâm của giai đoạn tiếp theo.
2. Bổ sung cổng thanh toán trực tuyến và hoàn thiện quản lý đơn hàng cho admin.
3. Kính mong thầy/cô cho ý kiến về việc **điều chỉnh stack công nghệ** (FastAPI thay
   cho React/Node) để thống nhất trước khi hoàn thiện báo cáo cuối.

---

## 9. Tài liệu tham khảo

1. FastAPI Documentation — https://fastapi.tiangolo.com/
2. SQLAlchemy Documentation — https://docs.sqlalchemy.org/
3. OpenAI API Documentation — https://platform.openai.com/docs
4. Phong Vũ — https://www.phongvu.vn/
5. CellphoneS — https://cellphones.com.vn/

---

*Báo cáo được lập ngày [.../.../2026]. Sinh viên thực hiện: [Họ và tên].*
