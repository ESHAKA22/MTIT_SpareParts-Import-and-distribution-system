from pydantic import BaseModel, Field
from typing import Optional, List


class CartItemCreate(BaseModel):
    customer_id: str = Field(..., example="CUS001")
    product_id: str = Field(..., example="PRD001")
    product_name: str = Field(..., example="Tractor Brake Pad")
    unit_price: float = Field(..., gt=0, example=2500.00)
    quantity: int = Field(..., gt=0, example=2)


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0, example=3)


class CartItemResponse(BaseModel):
    id: Optional[str] = None
    customer_id: str
    product_id: str
    product_name: str
    unit_price: float
    quantity: int
    subtotal: float


class CartSummaryResponse(BaseModel):
    customer_id: str
    items: List[CartItemResponse]
    total_amount: float