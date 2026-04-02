from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os

import models
from database import get_db
import auth

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

def format_currency(value):
    if not value:
        return "Liên hệ"
    return "{:,.0f} VNĐ".format(value).replace(",", ".")

templates.env.filters["currency"] = format_currency

auth_router = APIRouter()
admin_router = APIRouter(prefix="/admin", dependencies=[Depends(auth.get_current_admin)])

def base_ctx(request: Request, db: Session) -> dict:
    nav_categories = db.query(models.Category).all()
    user = auth.get_current_user_optional(request, db)
    return {"request": request, "nav_categories": nav_categories, "current_user": user}

@auth_router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, db: Session = Depends(get_db)):
    ctx = base_ctx(request, db)
    return templates.TemplateResponse("pages/login.html", ctx)

@auth_router.post("/login")
async def login_post(
    request: Request, 
    username: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not auth.verify_password(password, user.password_hash):
        ctx = base_ctx(request, db)
        
        ctx["error"] = "Sai tên đăng nhập hoặc mật khẩu"
        return templates.TemplateResponse("pages/login.html", ctx)
    
    token = auth.create_access_token(data={"sub": user.username})
    redirect_url = "/admin" if user.role == "admin" else "/"
    response = RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True, max_age=auth.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    return response

@auth_router.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("access_token")
    return response

# --- Admin Routes ---
@admin_router.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    total_products = db.query(models.Product).count()
    total_orders = db.query(models.Order).count()
    ctx = {"request": request, "total_products": total_products, "total_orders": total_orders}
    ctx["current_user"] = auth.get_current_user_optional(request, db)
    return templates.TemplateResponse("admin/dashboard.html", ctx)

@admin_router.get("/products", response_class=HTMLResponse)
async def admin_products(request: Request, db: Session = Depends(get_db)):
    products = db.query(models.Product).order_by(models.Product.id.desc()).all()
    ctx = {"request": request, "products": products, "current_user": auth.get_current_user_optional(request, db)}
    return templates.TemplateResponse("admin/products_list.html", ctx)

@admin_router.get("/products/new", response_class=HTMLResponse)
async def admin_product_new_page(request: Request, db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    ctx = {"request": request, "categories": categories, "product": None, "current_user": auth.get_current_user_optional(request, db)}
    return templates.TemplateResponse("admin/product_form.html", ctx)

@admin_router.post("/products/new")
async def admin_product_create(
    request: Request,
    title: str = Form(...),
    brand: str = Form(""),
    price_current: int = Form(...),
    price_old: int = Form(0),
    discount_percent: int = Form(0),
    image_url: str = Form(""),
    description: str = Form(""),
    stock: int = Form(0),
    category_id: int = Form(...),
    section: str = Form(""),
    db: Session = Depends(get_db)
):
    product = models.Product(
        title=title, brand=brand, price_current=price_current,
        price_old=price_old if price_old else None,
        discount_percent=discount_percent if discount_percent else None,
        image_url=image_url, description=description, stock=stock, 
        category_id=category_id, section=section if section else None
    )
    db.add(product)
    db.commit()
    return RedirectResponse(url="/admin/products", status_code=status.HTTP_302_FOUND)

@admin_router.get("/products/{product_id}/edit", response_class=HTMLResponse)
async def admin_product_edit_page(product_id: int, request: Request, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    categories = db.query(models.Category).all()
    ctx = {"request": request, "product": product, "categories": categories, "current_user": auth.get_current_user_optional(request, db)}
    return templates.TemplateResponse("admin/product_form.html", ctx)

@admin_router.post("/products/{product_id}/edit")
async def admin_product_edit(
    product_id: int,
    request: Request,
    title: str = Form(...),
    brand: str = Form(""),
    price_current: int = Form(...),
    price_old: int = Form(0),
    discount_percent: int = Form(0),
    image_url: str = Form(""),
    description: str = Form(""),
    stock: int = Form(0),
    category_id: int = Form(...),
    section: str = Form(""),
    db: Session = Depends(get_db)
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        product.title = title
        product.brand = brand
        product.price_current = price_current
        product.price_old = price_old if price_old else None
        product.discount_percent = discount_percent if discount_percent else None
        product.image_url = image_url
        product.description = description
        product.stock = stock
        product.category_id = category_id
        product.section = section if section else None
        db.commit()
    return RedirectResponse(url="/admin/products", status_code=status.HTTP_302_FOUND)

@admin_router.post("/products/{product_id}/delete")
async def admin_product_delete(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return RedirectResponse(url="/admin/products", status_code=status.HTTP_302_FOUND)
