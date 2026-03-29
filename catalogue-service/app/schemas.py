from pydantic import BaseModel
from typing import Optional


class Product(BaseModel):
    name: str
    category: str
    price: float
    stock: int
    description: str


class ProductResponse(BaseModel):
    id: str
    name: str
    category: str
    price: float
    stock: int
    description: str
    image: Optional[str]