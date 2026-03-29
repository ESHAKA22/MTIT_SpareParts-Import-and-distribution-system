from pydantic import BaseModel
from typing import Optional


class ComplaintCreate(BaseModel):
    customer_id: str
    order_id: str
    subject: str
    description: str


class ComplaintUpdate(BaseModel):
    status: Optional[str]
    response_message: Optional[str]