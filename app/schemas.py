from pydantic import BaseModel

# ده اللي بنستخدمه لما نيجي نبعت بيانات منتج جديد
class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int
    color: str | None = None

# ده اللي الـ API بيرجعهولنا بعد ما المنتج يتسيف
class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    color: str | None = None
    class Config:
        from_attributes = True