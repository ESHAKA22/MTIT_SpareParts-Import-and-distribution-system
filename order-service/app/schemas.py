from pydantic import BaseModel, Field
from typing import List, Optional


class OrderItem(BaseModel):
    product_id: str = Field(..., example="PRD001")
    product_name: str = Field(..., example="Tractor Brake Pad")
    unit_price: float = Field(..., gt=0, example=2500.00)
    quantity: int = Field(..., gt=0, example=2)
    subtotal: float = Field(..., gt=0, example=5000.00)


class OrderCreate(BaseModel):
    items: List[OrderItem]
    total_amount: float = Field(..., gt=0, example=5000.00)
    shipping_address: str = Field(..., example="Negombo, Sri Lanka")
    payment_status: str = Field(default="PENDING", example="PENDING")
    order_status: str = Field(default="PLACED", example="PLACED")


class OrderStatusUpdate(BaseModel):
    order_status: str = Field(..., example="CONFIRMED")


class PaymentStatusUpdate(BaseModel):
    payment_status: str = Field(..., example="SUCCESS")


class OrderResponse(BaseModel):
    id: Optional[str] = None
    customer_id: str
    items: List[OrderItem]
    total_amount: float
    shipping_address: str
    payment_status: str
    order_status: str
    created_at: str