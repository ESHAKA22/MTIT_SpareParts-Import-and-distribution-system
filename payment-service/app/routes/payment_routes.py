from datetime import datetime
from typing import Optional, Tuple
from fastapi import APIRouter, HTTPException
from app.database import payment_collection
from app.schemas import PaymentCreate
from app.utils import serialize_doc

router = APIRouter(prefix="/payments", tags=["Payments"])


def mock_payment_status(card_number: Optional[str]) -> Tuple[str, str]:
    """
    Demo rule:
    - If no card number is given, success.
    - If last digit is even -> SUCCESS
    - If last digit is odd -> FAILED
    """
    if not card_number:
        return "SUCCESS", "Mock payment completed successfully."

    last_char = card_number[-1]
    if not last_char.isdigit():
        return "FAILED", "Invalid mock card number."

    if int(last_char) % 2 == 0:
        return "SUCCESS", "Mock payment completed successfully."
    return "FAILED", "Mock payment failed during simulation."


@router.get("/health")
def health_check():
    return {"status": "ok", "service": "payment-service"}


@router.post("/process")
def process_payment(payload: PaymentCreate):
    payment_status, message = mock_payment_status(payload.card_number)

    payment_doc = {
        "order_id": payload.order_id,
        "customer_id": payload.customer_id,
        "amount": payload.amount,
        "payment_method": payload.payment_method.upper(),
        "card_number": payload.card_number,
        "payment_status": payment_status,
        "message": message,
        "created_at": datetime.utcnow().isoformat()
    }

    result = payment_collection.insert_one(payment_doc)
    created_payment = payment_collection.find_one({"_id": result.inserted_id})

    payment = serialize_doc(created_payment)
    payment["id"] = payment.pop("_id")

    return {
        "message": "Payment request processed.",
        "payment": payment
    }


@router.get("/{payment_id}")
def get_payment(payment_id: str):
    from bson import ObjectId

    payment = payment_collection.find_one({"_id": ObjectId(payment_id)})
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found.")

    data = serialize_doc(payment)
    data["id"] = data.pop("_id")
    return data


@router.get("/customer/{customer_id}")
def get_customer_payments(customer_id: str):
    payments = list(payment_collection.find({"customer_id": customer_id}))

    serialized = []
    for payment in payments:
        p = serialize_doc(payment)
        p["id"] = p.pop("_id")
        serialized.append(p)

    return {
        "customer_id": customer_id,
        "payments": serialized,
        "count": len(serialized)
    }