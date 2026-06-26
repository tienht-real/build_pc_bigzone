"""
Gán ảnh thay thế (cùng danh mục) cho các sản phẩm có ảnh Unsplash bị chết (404).
Dùng ảnh nội bộ đã tải sẵn trong static/images/products/.
Chạy SAU localize_images.py. Không xóa dữ liệu khác.

Usage: python fill_missing_images.py
"""
import os
import sys
import shutil

from database import SessionLocal
import models

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST_DIR = os.path.join(BASE_DIR, "static", "images", "products")

# {sản phẩm thiếu ảnh: sản phẩm nguồn cùng danh mục đã có ảnh}
MAPPING = {
    2: 1,    # PC Gaming i7   -> PC Gaming i5
    6: 5,    # Mini PC        -> PC văn phòng
    8: 9,    # Màn LG         -> Màn Samsung
    11: 7,   # Màn AOC        -> Màn ASUS
    13: 12,  # CPU Intel      -> Card RTX (linh kiện)
    16: 17,  # Mainboard      -> PSU Corsair
    23: 27,  # Bàn phím DareU -> Mousepad SteelSeries
    25: 24,  # Chuột G102     -> Chuột G Pro
    29: 26,  # Tai nghe Sony  -> Tai nghe Razer
    34: 32,  # Bàn gaming     -> Ghế Secretlab
    35: 33,  # Bàn nâng hạ    -> Ghế DXRacer
    36: 37,  # Camera IP      -> Webcam Logitech
    38: 37,  # Camera PTZ     -> Webcam Logitech
    39: 37,  # Đầu ghi NVR    -> Webcam Logitech
}

db = SessionLocal()
done = 0
for target_id, source_id in MAPPING.items():
    src = os.path.join(DEST_DIR, f"p{source_id}.jpg")
    dst = os.path.join(DEST_DIR, f"p{target_id}.jpg")
    if not os.path.exists(src):
        print(f"  [BỎ QUA] #{target_id}: thiếu ảnh nguồn p{source_id}.jpg")
        continue
    shutil.copyfile(src, dst)
    product = db.query(models.Product).filter(models.Product.id == target_id).first()
    if product:
        product.image_url = f"/static/images/products/p{target_id}.jpg"
        done += 1
        print(f"  [OK] #{target_id} <- ảnh của #{source_id}")

db.commit()
db.close()
print(f"\nXong: đã gán ảnh thay thế cho {done} sản phẩm.")
