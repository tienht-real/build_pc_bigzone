"""
Seed script - chạy file này để tạo lại toàn bộ dữ liệu mẫu.
Usage: python seed.py
"""
from database import engine, SessionLocal
import models

# Xóa và tạo lại toàn bộ bảng
models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# ── USERS ───────────────────────────────────────────────────────────────────
import auth
admin_user = models.User(
    username="admin",
    password_hash=auth.get_password_hash("admin123"),
    role="admin"
)
db.add(admin_user)
db.commit()

# ── CATEGORIES ──────────────────────────────────────────────────────────────
categories = [
    models.Category(name="Máy Tính Chơi Game", icon="ph-desktop"),          # id=1
    models.Category(name="Màn Hình Máy Tính",  icon="ph-monitor"),          # id=2
    models.Category(name="Linh Kiện PC",        icon="ph-cpu"),              # id=3
    models.Category(name="Laptop & Phụ Kiện",  icon="ph-laptop"),           # id=4
    models.Category(name="Gaming Gear",         icon="ph-mouse"),            # id=5
    models.Category(name="Thiết Bị Âm Thanh",  icon="ph-headphones"),       # id=6
    models.Category(name="Bàn Ghế Gaming",      icon="ph-chair"),            # id=7
    models.Category(name="Camera & An Ninh",   icon="ph-camera"),           # id=8
]
db.add_all(categories)
db.commit()

# ── PRODUCTS ─────────────────────────────────────────────────────────────────
products = [

    # ── Danh mục 1: Máy Tính Chơi Game ──────────────────────────────────────
    models.Product(
        title="PC Gaming Intel Core i5-13400F / RTX 4060 8GB",
        brand="Bigzone Custom", price_current=18_990_000, price_old=21_500_000,
        discount_percent=12, section="HOT_SALE", category_id=1, stock=15,
        image_url="https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=400&h=400&fit=crop",
        description="Cấu hình mạnh mẽ cho gaming 1080p/1440p. CPU Intel Core i5-13400F 10 nhân, VGA RTX 4060 8GB GDDR6, RAM 16GB DDR4, SSD 500GB NVMe, Case NZXT H510."
    ),
    models.Product(
        title="PC Gaming Core i7-13700K / RTX 4070 Ti 12GB",
        brand="Bigzone Custom", price_current=45_000_000, price_old=48_000_000,
        discount_percent=6, section="PC_GAMING", category_id=1, stock=8,
        image_url="https://images.unsplash.com/photo-1600861194942-f884de542387?w=400&h=400&fit=crop",
        description="Hệ thống gaming cao cấp với Intel Core i7-13700K, RTX 4070 Ti 12GB, RAM 32GB DDR5, SSD 1TB NVMe Gen4, tản nhiệt nước 240mm."
    ),
    models.Product(
        title="PC AMD Ryzen 7 7800X3D / RX 7800 XT 16GB",
        brand="Bigzone Custom", price_current=38_990_000, price_old=42_500_000,
        discount_percent=8, section="PC_GAMING", category_id=1, stock=10,
        image_url="https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=400&h=400&fit=crop",
        description="Hệ thống gaming AMD tối ưu cho game. Ryzen 7 7800X3D với 3D V-Cache, RX 7800 XT 16GB, RAM 32GB DDR5, SSD 1TB Gen4."
    ),
    models.Product(
        title="PC Streaming Core i9-13900K / RTX 4090 24GB",
        brand="Bigzone Custom", price_current=75_000_000, price_old=None,
        discount_percent=None, section="PC_GAMING", category_id=1, stock=3,
        image_url="https://images.unsplash.com/photo-1518770660439-4636190af475?w=400&h=400&fit=crop",
        description="Đỉnh cao gaming và streaming. Core i9-13900K 24 nhân, RTX 4090 24GB, RAM 64GB DDR5, SSD 2TB NVMe."
    ),
    models.Product(
        title="PC Văn Phòng Core i3-13100 / 8GB / 256GB SSD",
        brand="Bigzone Custom", price_current=6_500_000, price_old=6_800_000,
        discount_percent=4, section="HOT_SALE", category_id=1, stock=30,
        image_url="https://images.unsplash.com/photo-1541560052-5e137f229371?w=400&h=400&fit=crop",
        description="PC văn phòng ổn định, tiết kiệm điện. Core i3-13100, RAM 8GB, SSD 256GB, Windows 11 bản quyền."
    ),
    models.Product(
        title="Mini PC AsRock DeskMini X300 Ryzen 5 5600G",
        brand="ASRock", price_current=7_990_000, price_old=None,
        discount_percent=None, section=None, category_id=1, stock=12,
        image_url="https://images.unsplash.com/photo-1640523091910-c08da6da2ca1?w=400&h=400&fit=crop",
        description="Mini PC siêu nhỏ gọn với AMD Ryzen 5 5600G tích hợp đồ họa Vega 7, RAM 16GB, SSD 512GB."
    ),

    # ── Danh mục 2: Màn Hình Máy Tính ────────────────────────────────────────
    models.Product(
        title='Màn hình Gaming ASUS TUF VG27AQ 27" 165Hz IPS',
        brand="ASUS", price_current=7_490_000, price_old=8_500_000,
        discount_percent=12, section="HOT_SALE", category_id=2, stock=20,
        image_url="https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&h=400&fit=crop",
        description='Màn hình gaming 27" IPS 2K 165Hz, G-Sync compatible, HDR 400, 1ms GTG. Lý tưởng cho gaming 1440p.'
    ),
    models.Product(
        title='Màn hình LG 27GP950-B 4K 144Hz Nano IPS',
        brand="LG", price_current=15_900_000, price_old=17_500_000,
        discount_percent=9, section=None, category_id=2, stock=7,
        image_url="https://images.unsplash.com/photo-1616763355548-1b606f439f0a?w=400&h=400&fit=crop",
        description='Nano IPS 4K 144Hz, HDMI 2.1, DisplayPort 1.4, HDR600, DCI-P3 98%. Đỉnh cao trải nghiệm hình ảnh.'
    ),
    models.Product(
        title='Màn hình Samsung Odyssey G7 32" QHD 240Hz',
        brand="Samsung", price_current=12_500_000, price_old=14_000_000,
        discount_percent=11, section="PC_GAMING", category_id=2, stock=5,
        image_url="https://images.unsplash.com/photo-1551645120-d70bfe84c826?w=400&h=400&fit=crop",
        description='Cong 1000R, QLED 240Hz, 1ms MPRT, G-Sync, FreeSync Premium Pro. Trải nghiệm gaming đỉnh cao.'
    ),
    models.Product(
        title='Màn hình Dell U2722D 27" IPS 4K USB-C',
        brand="Dell", price_current=9_900_000, price_old=None,
        discount_percent=None, section=None, category_id=2, stock=10,
        image_url="https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=400&h=400&fit=crop",
        description='4K IPS, USB-C 90W, hub USB, Color Calibration, sRGB 99.9%. Màn hình chuyên đồ họa lý tưởng.'
    ),
    models.Product(
        title='Màn hình AOC 24G2SE 24" IPS 165Hz',
        brand="AOC", price_current=2_990_000, price_old=3_500_000,
        discount_percent=14, section="HOT_SALE", category_id=2, stock=25,
        image_url="https://images.unsplash.com/photo-1588702545922-7628a4ea54f6?w=400&h=400&fit=crop",
        description='24" IPS 165Hz Full HD, 1ms GTG, FreeSync Premium, giá tốt nhất phân khúc tầm trung.'
    ),

    # ── Danh mục 3: Linh Kiện PC ──────────────────────────────────────────────
    models.Product(
        title="Card màn hình ASUS TUF RTX 4060 Ti OC 8GB",
        brand="ASUS", price_current=9_490_000, price_old=10_500_000,
        discount_percent=10, section="HOT_SALE", category_id=3, stock=18,
        image_url="https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&h=400&fit=crop",
        description="RTX 4060 Ti 8GB GDDR6, boost 2610MHz, DLSS 3, AV1 encode, tiêu thụ chỉ 165W."
    ),
    models.Product(
        title="CPU Intel Core i5-13400F Tray (Không GPU tích hợp)",
        brand="Intel", price_current=3_890_000, price_old=4_200_000,
        discount_percent=7, section=None, category_id=3, stock=40,
        image_url="https://images.unsplash.com/photo-1624705527878-8fbabcc81bdf?w=400&h=400&fit=crop",
        description="10 nhân 16 luồng, base 2.5GHz boost 4.6GHz, TDP 65W, socket LGA1700. Tối ưu chi phí nhất trong dòng i5."
    ),
    models.Product(
        title="RAM Kingston Fury Beast 32GB (2x16) DDR5 6000MHz",
        brand="Kingston", price_current=2_490_000, price_old=2_800_000,
        discount_percent=11, section="HOT_SALE", category_id=3, stock=22,
        image_url="https://images.unsplash.com/photo-1555680202-c86f0e12f086?w=400&h=400&fit=crop",
        description="DDR5 6000MHz CL30, Intel XMP 3.0 Ready, tản nhiệt nhôm thấp profile. Hiệu năng cao cho nền tảng Intel 13th gen."
    ),
    models.Product(
        title="SSD Samsung 990 Pro 1TB NVMe PCIe 4.0",
        brand="Samsung", price_current=2_890_000, price_old=3_200_000,
        discount_percent=10, section=None, category_id=3, stock=35,
        image_url="https://images.unsplash.com/photo-1563770660941-20978e870e26?w=400&h=400&fit=crop",
        description="PCIe 4.0 x4, đọc 7450MB/s, ghi 6900MB/s. Nhanh nhất dòng consumer của Samsung."
    ),
    models.Product(
        title="Mainboard ASUS ROG STRIX B760-F Gaming WiFi",
        brand="ASUS", price_current=5_490_000, price_old=None,
        discount_percent=None, section=None, category_id=3, stock=12,
        image_url="https://images.unsplash.com/photo-1686616428789-9a1b18d2235c?w=400&h=400&fit=crop",
        description="LGA1700, DDR5, PCIe 5.0 x16, WiFi 6E, 2.5G LAN, 4x M.2, USB 3.2 Gen2x2. Bo mạch chủ cao cấp cho Intel Gen 12/13."
    ),
    models.Product(
        title="PSU Corsair RM850x 850W 80+ Gold Full Modular",
        brand="Corsair", price_current=2_890_000, price_old=3_100_000,
        discount_percent=7, section=None, category_id=3, stock=15,
        image_url="https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=400&h=400&fit=crop",
        description="850W, 80+ Gold, full modular, zero RPM mode, bảo hành 10 năm. Nguồn điện ổn định và im lặng."
    ),

    # ── Danh mục 4: Laptop & Phụ Kiện ────────────────────────────────────────
    models.Product(
        title="Laptop Gaming Acer Nitro 5 AN515 i5-12500H RTX 3060",
        brand="Acer", price_current=19_990_000, price_old=22_200_000,
        discount_percent=10, section="HOT_SALE", category_id=4, stock=9,
        image_url="https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=400&h=400&fit=crop",
        description='15.6" IPS 144Hz, i5-12500H, RTX 3060 6GB, 16GB DDR5, SSD 512GB NVMe. Gaming laptop tầm trung tốt nhất.'
    ),
    models.Product(
        title="Laptop ASUS ROG Strix G16 Ryzen 9 7945HX RTX 4070",
        brand="ASUS", price_current=35_990_000, price_old=39_000_000,
        discount_percent=8, section="PC_GAMING", category_id=4, stock=5,
        image_url="https://images.unsplash.com/photo-1593640408182-31c70c8268f5?w=400&h=400&fit=crop",
        description='16" QHD+ 240Hz, Ryzen 9 7945HX, RTX 4070 8GB, 32GB DDR5, SSD 1TB Gen4. Hiệu năng gaming đỉnh cao.'
    ),
    models.Product(
        title="Laptop Gaming MSI Katana B13VGK i7-13620H RTX 4070",
        brand="MSI", price_current=24_990_000, price_old=27_500_000,
        discount_percent=9, section=None, category_id=4, stock=7,
        image_url="https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop",
        description='15.6" FHD 144Hz, i7-13620H, RTX 4070 8GB, 16GB DDR5, SSD 512GB. Cân bằng hiệu năng và giá thành.'
    ),
    models.Product(
        title="Laptop Dell XPS 15 9530 i7-13700H OLED",
        brand="Dell", price_current=42_500_000, price_old=None,
        discount_percent=None, section=None, category_id=4, stock=4,
        image_url="https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=400&h=400&fit=crop",
        description='15.6" OLED 3.5K 60Hz, i7-13700H, RTX 4060 8GB, 32GB LPDDR5, SSD 1TB. Laptop sáng tạo cao cấp nhất.'
    ),
    models.Product(
        title="Laptop Lenovo Legion 5 Gen 8 Ryzen 7 7745HX RTX 4060",
        brand="Lenovo", price_current=28_990_000, price_old=31_000_000,
        discount_percent=7, section=None, category_id=4, stock=6,
        image_url="https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=400&h=400&fit=crop",
        description='15.6" IPS 165Hz, Ryzen 7 7745HX, RTX 4060 8GB, 16GB DDR5, SSD 512GB. Gaming laptop AMD tốt nhất tầm 29 triệu.'
    ),

    # ── Danh mục 5: Gaming Gear ───────────────────────────────────────────────
    models.Product(
        title="Bàn phím cơ DareU EK87 Compact Red Switch",
        brand="DareU", price_current=550_000, price_old=580_000,
        discount_percent=5, section="HOT_SALE", category_id=5, stock=50,
        image_url="https://images.unsplash.com/photo-1612282130134-4b53f6312a02?w=400&h=400&fit=crop",
        description="87 phím TKL, switch Linear Red, đèn LED RGB, kết nối USB-C, tương thích Windows/Mac. Bàn phím cơ giá tốt nhất."
    ),
    models.Product(
        title="Chuột Logitech G Pro X Superlight 2 DEX",
        brand="Logitech", price_current=2_890_000, price_old=3_200_000,
        discount_percent=10, section=None, category_id=5, stock=15,
        image_url="https://images.unsplash.com/photo-1595225476474-87563907a212?w=400&h=400&fit=crop",
        description="Sensor HERO 2 25K DPI, 32K polling rate, nặng chỉ 60g, pin 95 giờ. Chuột gaming không dây chuyên pro."
    ),
    models.Product(
        title="Chuột Logitech G102 Lightsync RGB Black",
        brand="Logitech", price_current=399_000, price_old=499_000,
        discount_percent=20, section="HOT_SALE", category_id=5, stock=80,
        image_url="https://images.unsplash.com/photo-1527814050087-142db74032d9?w=400&h=400&fit=crop",
        description="Sensor 8000 DPI, 6 nút lập trình, đèn RGB 16.8M màu, nhẹ 85g. Chuột gaming giá rẻ bán chạy nhất."
    ),
    models.Product(
        title="Tai nghe Razer BlackShark V2 Pro Wireless",
        brand="Razer", price_current=3_690_000, price_old=4_000_000,
        discount_percent=8, section=None, category_id=5, stock=12,
        image_url="https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=400&h=400&fit=crop",
        description="Driver 50mm Triforce Titanium, mic HyperClear Supercardioid, pin 70 giờ, kết nối 2.4GHz. Âm thanh định vị xuất sắc."
    ),
    models.Product(
        title="Mousepad SteelSeries QcK Heavy XXL 900x400mm",
        brand="SteelSeries", price_current=690_000, price_old=750_000,
        discount_percent=8, section=None, category_id=5, stock=30,
        image_url="https://images.unsplash.com/photo-1608667508764-33cf0726b13a?w=400&h=400&fit=crop",
        description="Kích thước 900x400x6mm, bề mặt micro-texture tối ưu chuột quang, đế cao su chống trượt. Lựa chọn của 90% pro gamer."
    ),

    # ── Danh mục 6: Thiết Bị Âm Thanh ────────────────────────────────────────
    models.Product(
        title="Loa Bookshelf Edifier R1280DBs Bluetooth",
        brand="Edifier", price_current=1_690_000, price_old=1_900_000,
        discount_percent=11, section="HOT_SALE", category_id=6, stock=20,
        image_url="https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400&h=400&fit=crop",
        description="2.0 stereo, Bluetooth 5.0, optical/coaxial/RCA, bass 4\" + tweeter 13mm. Loa để bàn chất lượng âm thanh tốt nhất phân khúc."
    ),
    models.Product(
        title="Tai nghe Chống Ồn Sony WH-1000XM5",
        brand="Sony", price_current=7_990_000, price_old=8_500_000,
        discount_percent=6, section=None, category_id=6, stock=8,
        image_url="https://images.unsplash.com/photo-1550005973-786315af6411?w=400&h=400&fit=crop",
        description="ANC tốt nhất thế giới, LDAC, pin 30 giờ, sạc 3 phút = 3 giờ, multipoint connection. Tai nghe cao cấp đỉnh nhất."
    ),
    models.Product(
        title="Microphone Blue Yeti X USB Condenser",
        brand="Blue", price_current=3_290_000, price_old=None,
        discount_percent=None, section=None, category_id=6, stock=10,
        image_url="https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=400&fit=crop",
        description="Condenser 3 capsule, 4 chế độ pickup, LED metering, kết nối USB, phù hợp streaming/podcast/voiceover."
    ),
    models.Product(
        title="DAC/AMP FiiO K7 Desktop Balanced",
        brand="FiiO", price_current=3_490_000, price_old=3_800_000,
        discount_percent=8, section=None, category_id=6, stock=6,
        image_url="https://images.unsplash.com/photo-1518770660439-4636190af475?w=400&h=400&fit=crop",
        description="PCM 768kHz/32bit, DSD512, cổng Balanced 4.4mm + SE 6.35mm, tổng trở 200Ω. Khuếch đại tai nghe cao cấp."
    ),

    # ── Danh mục 7: Bàn Ghế Gaming ───────────────────────────────────────────
    models.Product(
        title="Ghế Gaming Secretlab Titan Evo 2022 SoftWeave",
        brand="Secretlab", price_current=9_990_000, price_old=11_000_000,
        discount_percent=9, section="HOT_SALE", category_id=7, stock=5,
        image_url="https://images.unsplash.com/photo-1505843490538-5133c6c7d0e1?w=400&h=400&fit=crop",
        description="Vải SoftWeave Plus, tựa lưng điều chỉnh 4 chiều, đệm lưng memory foam tích hợp, cần tay 4D, khung thép. Ghế gaming tốt nhất thế giới."
    ),
    models.Product(
        title="Ghế DXRacer Formula Series OH/FH08/N",
        brand="DXRacer", price_current=4_990_000, price_old=5_500_000,
        discount_percent=9, section=None, category_id=7, stock=10,
        image_url="https://images.unsplash.com/photo-1598257006626-48b0c252070d?w=400&h=400&fit=crop",
        description="Da PU cao cấp, lưng ngả 135°, cần tay 3D, bánh xe polyurethane, khung thép 2mm. Thương hiệu esport hàng đầu."
    ),
    models.Product(
        title="Bàn Gaming L-Shape 160x120cm RGB",
        brand="GameDesk", price_current=2_490_000, price_old=2_800_000,
        discount_percent=11, section=None, category_id=7, stock=8,
        image_url="https://images.unsplash.com/photo-1554104707-a76b270e4fb0?w=400&h=400&fit=crop",
        description="Hình chữ L 160x120cm, mặt bàn carbon fiber texture, đèn LED RGB 5V, tay kẹp tai nghe, móc chuột tích hợp."
    ),
    models.Product(
        title="Bàn Gaming Nâng Hạ Điện DeskPro Pro 140x70cm",
        brand="DeskPro", price_current=5_990_000, price_old=None,
        discount_percent=None, section=None, category_id=7, stock=4,
        image_url="https://images.unsplash.com/photo-1616422285116-2da9cc503f84?w=400&h=400&fit=crop",
        description="Điều chỉnh chiều cao 70-120cm bằng điện, 4 preset nhớ, tải trọng 80kg, chân khung thép. Tốt cho sức khỏe cột sống."
    ),

    # ── Danh mục 8: Camera & An Ninh ─────────────────────────────────────────
    models.Product(
        title="Camera IP Hikvision DS-2CD2143G2-I 4MP AcuSense",
        brand="Hikvision", price_current=890_000, price_old=990_000,
        discount_percent=10, section="HOT_SALE", category_id=8, stock=40,
        image_url="https://images.unsplash.com/photo-1557993077-802c632b7190?w=400&h=400&fit=crop",
        description="4MP, IR 40m, IP67 chống bụi nước, phát hiện người/xe, WDR 120dB, H.265+. Camera ngoài trời tốt nhất."
    ),
    models.Product(
        title="Webcam Logitech C920s Pro HD 1080p",
        brand="Logitech", price_current=1_890_000, price_old=2_200_000,
        discount_percent=14, section=None, category_id=8, stock=25,
        image_url="https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400&h=400&fit=crop",
        description="1080p 30fps, autofocus, mic kép khử ồn, cover lensguard, tương thích Zoom/Teams/Meet. Webcam streaming tốt nhất tầm giá."
    ),
    models.Product(
        title="Camera PTZ 4K 30x Zoom Dahua SD49425XB-HNR",
        brand="Dahua", price_current=8_500_000, price_old=None,
        discount_percent=None, section=None, category_id=8, stock=3,
        image_url="https://images.unsplash.com/photo-1615554160408-51fbdf3fe5da?w=400&h=400&fit=crop",
        description="4K 30x optical zoom, AI tracking tự động, IR 100m, IP66, PoE+. Camera PTZ chuyên nghiệp cho hội trường/sự kiện."
    ),
    models.Product(
        title="Đầu ghi NVR Hikvision DS-7608NXI-K2 8 kênh 4K",
        brand="Hikvision", price_current=2_890_000, price_old=None,
        discount_percent=None, section=None, category_id=8, stock=7,
        image_url="https://images.unsplash.com/photo-1593508512255-8f4b50ca4316?w=400&h=400&fit=crop",
        description="8 kênh 4K, H.265+, hỗ trợ HDD đến 10TB, HDMI 4K out, phát hiện AI. Đầu ghi hình chuyên dụng cho hệ thống camera IP."
    ),
]

db.add_all(products)
db.commit()
db.close()

print(f"OK! Seeded {len(categories)} categories va {len(products)} products thanh cong!")
