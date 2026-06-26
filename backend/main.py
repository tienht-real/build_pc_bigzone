import logging
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, StreamingResponse
from sqlalchemy import or_
from sqlalchemy.orm import Session
import models
import schemas
import auth
import chatbot
from database import engine, get_db
from routers import auth_router, admin_router

logger = logging.getLogger("bigzone")
logging.basicConfig(level=logging.INFO)

# Tạo bảng DB khi startup nếu chưa có
models.Base.metadata.create_all(bind=engine)

import os

app = FastAPI(title="Bigzone API")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Mount Static Files (CSS, JS, Images)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Include Routers
app.include_router(auth_router)
app.include_router(admin_router)

# Cấu hình Jinja2 Templates
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


# ── Filters ──────────────────────────────────────────────────────────────────
def format_currency(value):
    if not value:
        return "Liên hệ"
    return "{:,.0f} VNĐ".format(value).replace(",", ".")

templates.env.filters["currency"] = format_currency


# ── Helper: context dùng chung cho mọi route ─────────────────────────────────
def base_ctx(request: Request, db: Session) -> dict:
    nav_categories = db.query(models.Category).all()
    user = auth.get_current_user_optional(request, db)
    return {"request": request, "nav_categories": nav_categories, "current_user": user}


# ── Trang chính ───────────────────────────────────────────────────────────────
@app.get("/")
async def home_page(request: Request, db: Session = Depends(get_db)):
    ctx = base_ctx(request, db)
    ctx["hot_sale"] = (
        db.query(models.Product)
        .filter(models.Product.section == "HOT_SALE")
        .limit(10).all()
    )
    ctx["pc_gaming"] = (
        db.query(models.Product)
        .filter(models.Product.section == "PC_GAMING")
        .limit(10).all()
    )
    return templates.TemplateResponse("pages/home.html", ctx)


# ── Trang danh mục ────────────────────────────────────────────────────────────
PRODUCTS_PER_PAGE = 12


@app.get("/category/{category_id}")
async def category_page(
    category_id: int,
    request: Request,
    sort: str = "default",
    page: int = 1,
    db: Session = Depends(get_db),
):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Danh mục không tồn tại")

    query = db.query(models.Product).filter(models.Product.category_id == category_id)

    if sort == "price_asc":
        query = query.order_by(models.Product.price_current.asc())
    elif sort == "price_desc":
        query = query.order_by(models.Product.price_current.desc())
    elif sort == "discount":
        query = query.filter(models.Product.discount_percent != None).order_by(
            models.Product.discount_percent.desc()
        )

    total_products = query.count()
    total_pages = max(1, (total_products + PRODUCTS_PER_PAGE - 1) // PRODUCTS_PER_PAGE)
    page = max(1, min(page, total_pages))
    products = query.offset((page - 1) * PRODUCTS_PER_PAGE).limit(PRODUCTS_PER_PAGE).all()

    ctx = base_ctx(request, db)
    ctx["category"] = category
    ctx["products"] = products
    ctx["sort"] = sort
    ctx["page"] = page
    ctx["total_pages"] = total_pages
    ctx["total_products"] = total_products
    return templates.TemplateResponse("pages/category.html", ctx)


# ── Trang chi tiết sản phẩm ───────────────────────────────────────────────────
@app.get("/product/{product_id}")
async def product_page(product_id: int, request: Request, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Sản phẩm không tồn tại")

    related = (
        db.query(models.Product)
        .filter(
            models.Product.category_id == product.category_id,
            models.Product.id != product.id,
        )
        .limit(5).all()
    )

    ctx = base_ctx(request, db)
    ctx["product"] = product
    ctx["related_products"] = related
    return templates.TemplateResponse("pages/product.html", ctx)


# ── Trang tìm kiếm ────────────────────────────────────────────────────────────
@app.get("/search")
async def search_page(
    q: str = "",
    sort: str = "default",
    page: int = 1,
    request: Request = None,
    db: Session = Depends(get_db),
):
    products = []
    total_products = 0
    total_pages = 1

    if q.strip():
        keyword = f"%{q.strip()}%"
        query = (
            db.query(models.Product)
            .filter(or_(
                models.Product.title.ilike(keyword),
                models.Product.brand.ilike(keyword),
                models.Product.description.ilike(keyword),
            ))
        )

        if sort == "price_asc":
            query = query.order_by(models.Product.price_current.asc())
        elif sort == "price_desc":
            query = query.order_by(models.Product.price_current.desc())
        elif sort == "discount":
            query = query.filter(models.Product.discount_percent != None).order_by(
                models.Product.discount_percent.desc()
            )

        total_products = query.count()
        total_pages = max(1, (total_products + PRODUCTS_PER_PAGE - 1) // PRODUCTS_PER_PAGE)
        page = max(1, min(page, total_pages))
        products = query.offset((page - 1) * PRODUCTS_PER_PAGE).limit(PRODUCTS_PER_PAGE).all()

    ctx = base_ctx(request, db)
    ctx["products"] = products
    ctx["query"] = q
    ctx["sort"] = sort
    ctx["page"] = page
    ctx["total_pages"] = total_pages
    ctx["total_products"] = total_products
    return templates.TemplateResponse("pages/search.html", ctx)


# ── Giỏ hàng ─────────────────────────────────────────────────────────────────
@app.get("/cart")
async def cart_page(request: Request, db: Session = Depends(get_db)):
    ctx = base_ctx(request, db)
    return templates.TemplateResponse("pages/cart.html", ctx)


# ── Thanh toán ────────────────────────────────────────────────────────────────
@app.get("/checkout")
async def checkout_page(request: Request, db: Session = Depends(get_db)):
    ctx = base_ctx(request, db)
    return templates.TemplateResponse("pages/checkout.html", ctx)


# ── API JSON ──────────────────────────────────────────────────────────────────
@app.get("/api/categories")
async def api_categories(db: Session = Depends(get_db)):
    cats = db.query(models.Category).all()
    return [{"id": c.id, "name": c.name, "icon": c.icon} for c in cats]


@app.get("/api/products")
async def api_products(
    category_id: int = None,
    section: str = None,
    q: str = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Product)
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    if section:
        query = query.filter(models.Product.section == section)
    if q:
        keyword = f"%{q.strip()}%"
        query = query.filter(or_(
            models.Product.title.ilike(keyword),
            models.Product.brand.ilike(keyword),
            models.Product.description.ilike(keyword),
        ))
    return [
        {
            "id": p.id,
            "title": p.title,
            "brand": p.brand,
            "price_current": p.price_current,
            "price_old": p.price_old,
            "discount_percent": p.discount_percent,
            "image_url": p.image_url,
            "stock": p.stock,
            "category_id": p.category_id,
        }
        for p in query.all()
    ]


@app.post("/api/orders")
async def create_order(order_data: schemas.OrderCreate, db: Session = Depends(get_db)):
    # Validate từng item: kiểm tra sản phẩm tồn tại, giá đúng, còn hàng
    verified_total = 0
    order_items = []

    for item in order_data.items:
        product = db.query(models.Product).filter(models.Product.id == item.id).first()
        if not product:
            raise HTTPException(status_code=400, detail=f"Sản phẩm ID {item.id} không tồn tại")
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"'{product.title}' chỉ còn {product.stock} sản phẩm",
            )
        # Dùng giá từ DB, không tin giá client gửi lên
        verified_total += product.price_current * item.quantity
        order_items.append(
            models.OrderItem(
                product_id=product.id,
                product_title=product.title,
                price=product.price_current,
                quantity=item.quantity,
            )
        )

    # Tạo đơn hàng
    cust = order_data.customer
    order = models.Order(
        customer_name=cust.name,
        customer_phone=cust.phone,
        customer_email=cust.email,
        address=cust.address,
        note=cust.note,
        payment_method=cust.payment,
        total=verified_total,
        items=order_items,
    )
    db.add(order)

    # Trừ tồn kho
    for item in order_data.items:
        db.query(models.Product).filter(models.Product.id == item.id).update(
            {"stock": models.Product.stock - item.quantity}
        )

    db.commit()
    db.refresh(order)
    logger.info("Order #%s created – total %s VNĐ", order.id, verified_total)
    return {"status": "success", "order_id": order.id}


# ── Chatbot AI tư vấn ────────────────────────────────────────────────────
@app.post("/api/chat")
async def chat(req: schemas.ChatRequest, db: Session = Depends(get_db)):
    messages = [{"role": m.role, "content": m.content} for m in req.messages]
    return StreamingResponse(
        chatbot.stream_chat(messages, db),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ── Trang xác nhận đơn hàng ──────────────────────────────────────────────
@app.get("/order-success/{order_id}")
async def order_success_page(order_id: int, request: Request, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Đơn hàng không tồn tại")
    ctx = base_ctx(request, db)
    ctx["order"] = order
    return templates.TemplateResponse("pages/order_success.html", ctx)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
