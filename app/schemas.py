from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    sku: str
    price: float
    stock: int
    color: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    color: Optional[str] = None

class Product(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True