from pydantic import BaseModel, field_validator
from typing import Optional, List

class ProductBase(BaseModel):
    title: str
    price_current: int
    price_old: Optional[int] = None
    discount_percent: Optional[int] = None
    image_url: str = ""
    section: str = ""

class Product(ProductBase):
    id: int
    category_id: int
    
    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    icon: str

class Category(CategoryBase):
    id: int
    products: List[Product] = []

    class Config:
        from_attributes = True


# ── Order schemas ────────────────────────────────────────────────────────────
class OrderItemCreate(BaseModel):
    id: int
    title: str
    price: int
    quantity: int

    @field_validator("quantity")
    @classmethod
    def qty_positive(cls, v):
        if v < 1:
            raise ValueError("Số lượng phải >= 1")
        return v


class CustomerInfo(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    address: str
    note: Optional[str] = None
    payment: str = "cod"

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Tên không được để trống")
        return v.strip()

    @field_validator("phone")
    @classmethod
    def phone_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Số điện thoại không được để trống")
        return v.strip()

    @field_validator("address")
    @classmethod
    def address_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Địa chỉ không được để trống")
        return v.strip()


class OrderCreate(BaseModel):
    customer: CustomerInfo
    items: List[OrderItemCreate]
    total: int


# ── Chatbot schemas ────────────────────────────────────────────────────────────
class ChatMessage(BaseModel):
    role: str
    content: str

    @field_validator("role")
    @classmethod
    def role_valid(cls, v):
        if v not in ("user", "assistant"):
            raise ValueError("role phải là 'user' hoặc 'assistant'")
        return v

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Nội dung không được để trống")
        return v.strip()


class ChatRequest(BaseModel):
    messages: List[ChatMessage]

    @field_validator("messages")
    @classmethod
    def messages_not_empty(cls, v):
        if not v:
            raise ValueError("Cần ít nhất một tin nhắn")
        if v[-1].role != "user":
            raise ValueError("Tin nhắn cuối phải từ người dùng")
        return v
