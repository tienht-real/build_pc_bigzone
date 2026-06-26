"""
Tải ảnh sản phẩm từ URL ngoài (Unsplash) về lưu nội bộ trong static/images/products/
rồi cập nhật image_url trong DB sang đường dẫn /static/... — KHÔNG xóa dữ liệu khác.

Usage: python localize_images.py
"""
import os
import sys
import urllib.request

from database import SessionLocal
import models

# Console Windows mặc định cp1252 — ép UTF-8 để in được tiếng Việt
sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST_DIR = os.path.join(BASE_DIR, "static", "images", "products")
os.makedirs(DEST_DIR, exist_ok=True)

db = SessionLocal()
products = db.query(models.Product).all()

ok, skip, fail = 0, 0, 0
failed = []
for p in products:
    url = (p.image_url or "").strip()
    # Bỏ qua ảnh đã là nội bộ hoặc rỗng
    if not url or url.startswith("/static"):
        skip += 1
        continue

    filename = f"p{p.id}.jpg"
    dest = os.path.join(DEST_DIR, filename)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        with open(dest, "wb") as f:
            f.write(data)
        p.image_url = f"/static/images/products/{filename}"
        ok += 1
        print(f"  [OK]   #{p.id} {p.title[:45]}")
    except Exception as e:
        fail += 1
        p.image_url = ""  # để trống -> web hiện ô placeholder thay vì ảnh vỡ
        failed.append((p.id, p.title))
        print(f"  [FAIL] #{p.id} {p.title[:45]} -> {e}")

db.commit()
db.close()
print(f"\nXong: {ok} tải thành công, {skip} bỏ qua, {fail} lỗi.")
if failed:
    print("Các sản phẩm tải ảnh lỗi (đã để trống image_url):")
    for pid, title in failed:
        print(f"  #{pid} - {title}")
print(f"Ảnh lưu tại: {DEST_DIR}")
