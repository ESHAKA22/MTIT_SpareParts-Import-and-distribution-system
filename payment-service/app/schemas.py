from pydantic import BaseModel, Field
from typing import Optional


class PaymentCreate(BaseModel):
    order_id: str = Field(..., example="ORD1001")
    amount: float = Field(..., gt=0, example=5000.00)
    payment_method: str = Field(..., example="CARD")
    card_number: Optional[str] = Field(default=None, example="4111111111111112")


class PaymentResponse(BaseModel):
    id: Optional[str] = None
    order_id: str
    customer_id: str
    amount: float
    payment_method: str
    payment_status: str
    message: str