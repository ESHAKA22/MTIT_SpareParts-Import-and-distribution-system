from pydantic import BaseModel
from typing import Optional

# Full Product model
class Product(BaseModel):
    id: int
    name: str
    price: float

# Create Product
class ProductCreate(BaseModel):
    name: str
    price: float

# Update Product
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None