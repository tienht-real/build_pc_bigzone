"""
Migrate DB hiện có để hỗ trợ trang Build PC, KHÔNG xoá dữ liệu (giữ đơn hàng):
  1. Thêm cột component_type vào bảng products nếu chưa có.
  2. Gắn loại cho linh kiện sẵn có + thêm linh kiện mới.

Usage: python add_build_components.py
"""
import sys
from sqlalchemy import text, inspect

from database import engine, SessionLocal
import models
from build_components import apply_build_components

sys.stdout.reconfigure(encoding="utf-8")

# 1. Thêm cột nếu thiếu (SQLite: ALTER TABLE ADD COLUMN)
cols = [c["name"] for c in inspect(engine).get_columns("products")]
if "component_type" not in cols:
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE products ADD COLUMN component_type VARCHAR"))
    print("Đã thêm cột 'component_type' vào bảng products.")
else:
    print("Cột 'component_type' đã tồn tại — bỏ qua bước thêm cột.")

# 2. Gắn loại + thêm linh kiện mới
db = SessionLocal()
tagged, added = apply_build_components(db, models)
db.close()
print(f"Đã gắn loại cho {tagged} linh kiện sẵn có, thêm mới {added} linh kiện.")
print("Xong. Trang Build PC đã có đủ dữ liệu.")
