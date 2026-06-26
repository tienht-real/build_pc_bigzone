"""
Dữ liệu linh kiện cho trang Build PC + hàm gắn loại linh kiện (component_type)
vào DB. Dùng chung cho seed.py (tạo mới) và add_build_components.py (migrate DB cũ).

8 khe: cpu, mainboard, ram, vga, ssd, psu, case, cooling
"""

IMG = "/static/images/products/"

# Ảnh đại diện cho từng loại (tái dùng ảnh sẵn có; case/cooling dùng SVG)
TYPE_IMAGE = {
    "cpu": IMG + "p13.jpg",
    "mainboard": IMG + "p16.jpg",
    "ram": IMG + "p14.jpg",
    "vga": IMG + "p12.jpg",
    "ssd": IMG + "p15.jpg",
    "psu": IMG + "p17.jpg",
    "case": IMG + "case.svg",
    "cooling": IMG + "cooling.svg",
}

# Tự nhận loại cho các sản phẩm linh kiện đã có sẵn (danh mục 3) theo tiền tố tên
PREFIX_TO_TYPE = [
    ("CPU", "cpu"),
    ("Mainboard", "mainboard"),
    ("RAM", "ram"),
    ("Card màn hình", "vga"),
    ("VGA", "vga"),
    ("SSD", "ssd"),
    ("PSU", "psu"),
    ("Nguồn", "psu"),
    ("Case", "case"),
    ("Vỏ", "case"),
    ("Tản", "cooling"),
]

CATEGORY_LINHKIEN = 3  # "Linh Kiện PC"

# Linh kiện thêm mới (mỗi khe có nhiều lựa chọn hơn). price tính theo VNĐ.
NEW_COMPONENTS = [
    # ── CPU ──────────────────────────────────────────────────────────────
    dict(title="CPU Intel Core i7-13700K", brand="Intel", price_current=9_990_000,
         price_old=11_200_000, discount_percent=11, component_type="cpu",
         description="16 nhân 24 luồng, xung tối đa 5.4GHz — chiến game và làm việc nặng."),
    dict(title="CPU AMD Ryzen 7 7800X3D", brand="AMD", price_current=11_490_000,
         component_type="cpu",
         description="CPU gaming mạnh nhất phân khúc nhờ công nghệ 3D V-Cache."),

    # ── Mainboard ────────────────────────────────────────────────────────
    dict(title="Mainboard MSI MAG B650 Tomahawk WiFi", brand="MSI", price_current=4_990_000,
         component_type="mainboard",
         description="Socket AM5 cho Ryzen 7000, hỗ trợ DDR5, WiFi 6E."),
    dict(title="Mainboard Gigabyte B760M DS3H DDR4", brand="Gigabyte", price_current=2_690_000,
         component_type="mainboard",
         description="Socket LGA1700, dùng RAM DDR4 tiết kiệm chi phí."),

    # ── RAM ──────────────────────────────────────────────────────────────
    dict(title="RAM Corsair Vengeance 16GB (2x8) DDR5 5600", brand="Corsair",
         price_current=1_490_000, component_type="ram",
         description="Kit 16GB DDR5 bus 5600MHz, đủ cho gaming phổ thông."),
    dict(title="RAM G.Skill Trident Z5 RGB 32GB (2x16) DDR5 6400", brand="G.Skill",
         price_current=3_290_000, component_type="ram",
         description="32GB DDR5 6400MHz LED RGB, cho cấu hình cao cấp."),

    # ── VGA ──────────────────────────────────────────────────────────────
    dict(title="VGA Gigabyte RTX 4070 SUPER WindForce 12GB", brand="Gigabyte",
         price_current=16_990_000, price_old=18_500_000, discount_percent=8,
         component_type="vga",
         description="RTX 4070 SUPER 12GB, chiến mượt 2K mọi tựa game."),
    dict(title="VGA ASUS Dual RX 7600 8GB", brand="ASUS", price_current=6_990_000,
         component_type="vga",
         description="Card AMD tầm trung, chơi tốt Full HD."),

    # ── SSD ──────────────────────────────────────────────────────────────
    dict(title="SSD WD Black SN770 500GB NVMe PCIe 4.0", brand="WD",
         price_current=1_290_000, component_type="ssd",
         description="Tốc độ đọc tới 5000MB/s, khởi động hệ thống nhanh."),
    dict(title="SSD Crucial P3 Plus 2TB NVMe PCIe 4.0", brand="Crucial",
         price_current=3_190_000, component_type="ssd",
         description="Dung lượng lớn 2TB cho game và dữ liệu."),

    # ── PSU ──────────────────────────────────────────────────────────────
    dict(title="Nguồn Cooler Master MWE 650 V2 80+ Bronze", brand="Cooler Master",
         price_current=1_290_000, component_type="psu",
         description="650W chuẩn 80 Plus Bronze, ổn định cho dàn tầm trung."),
    dict(title="Nguồn Seasonic Focus GX-750 80+ Gold Full Modular", brand="Seasonic",
         price_current=2_690_000, component_type="psu",
         description="750W 80 Plus Gold, full modular, bảo hành 10 năm."),

    # ── Case ─────────────────────────────────────────────────────────────
    dict(title="Case NZXT H5 Flow Mid Tower", brand="NZXT", price_current=1_990_000,
         component_type="case",
         description="Thiết kế tối ưu luồng gió, mặt lưới thoáng."),
    dict(title="Case Corsair 4000D Airflow", brand="Corsair", price_current=2_290_000,
         component_type="case",
         description="Vỏ ATX nổi tiếng về tản nhiệt và lắp ráp dễ dàng."),
    dict(title="Case Lian Li Lancool 216 RGB", brand="Lian Li", price_current=2_490_000,
         component_type="case",
         description="2 fan 160mm ARGB phía trước, không gian rộng rãi."),

    # ── Tản nhiệt ────────────────────────────────────────────────────────
    dict(title="Tản nhiệt khí DeepCool AK400", brand="DeepCool", price_current=690_000,
         component_type="cooling",
         description="Tản khí 4 ống đồng, mát và êm cho CPU tầm trung."),
    dict(title="Tản nhiệt nước Cooler Master ML240L V2 ARGB", brand="Cooler Master",
         price_current=1_790_000, component_type="cooling",
         description="AIO 240mm ARGB, làm mát tốt cho CPU cao cấp."),
    dict(title="Tản nhiệt nước NZXT Kraken 240 RGB", brand="NZXT", price_current=3_490_000,
         component_type="cooling",
         description="AIO 240mm màn hình LCD, hiệu năng và thẩm mỹ cao."),
]


def _detect_type(title: str):
    for prefix, ctype in PREFIX_TO_TYPE:
        if title.startswith(prefix):
            return ctype
    return None


def apply_build_components(db, models):
    """Gắn component_type cho SP linh kiện sẵn có và thêm linh kiện mới (idempotent)."""
    # 1. Gắn loại cho các sản phẩm linh kiện đã có (danh mục 3)
    existing = db.query(models.Product).filter(
        models.Product.category_id == CATEGORY_LINHKIEN
    ).all()
    tagged = 0
    for p in existing:
        if p.component_type:
            continue
        ctype = _detect_type(p.title)
        if ctype:
            p.component_type = ctype
            tagged += 1

    # 2. Thêm linh kiện mới nếu chưa tồn tại (so theo title)
    have_titles = {row[0] for row in db.query(models.Product.title).all()}
    added = 0
    for c in NEW_COMPONENTS:
        if c["title"] in have_titles:
            continue
        ctype = c["component_type"]
        db.add(models.Product(
            title=c["title"],
            brand=c.get("brand"),
            price_current=c["price_current"],
            price_old=c.get("price_old"),
            discount_percent=c.get("discount_percent"),
            image_url=TYPE_IMAGE[ctype],
            description=c.get("description", ""),
            stock=c.get("stock", 20),
            category_id=CATEGORY_LINHKIEN,
            component_type=ctype,
        ))
        added += 1

    db.commit()
    return tagged, added
