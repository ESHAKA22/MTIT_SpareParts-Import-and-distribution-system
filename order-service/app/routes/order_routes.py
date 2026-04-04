from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from app.database import order_collection
from app.schemas import OrderCreate, OrderStatusUpdate, PaymentStatusUpdate
from app.utils import serialize_doc
from app.auth import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/health")
def health_check():
    return {"status": "ok", "service": "order-service"}


@router.post("/create")
def create_order(payload: OrderCreate, current_user: dict = Depends(get_current_user)):
    # Use email from JWT token as customer_id
    customer_id = current_user["email"]
    order_doc = {
        "customer_id": customer_id,
        "items": [item.dict() for item in payload.items],
        "total_amount": payload.total_amount,
        "shipping_address": payload.shipping_address,
        "payment_status": payload.payment_status.upper(),
        "order_status": payload.order_status.upper(),
        "created_at": datetime.utcnow().isoformat()
    }

    result = order_collection.insert_one(order_doc)
    created_order = order_collection.find_one({"_id": result.inserted_id})

    order = serialize_doc(created_order)
    order["id"] = order.pop("_id")

    return {
        "message": "Order created successfully.",
        "order": order
    }


@router.get("/")
def get_all_orders(current_user: dict = Depends(get_current_user)):
    customer_id = current_user["email"]
    orders = list(order_collection.find({"customer_id": customer_id}).sort("created_at", -1))

    serialized_orders = []
    for order in orders:
        data = serialize_doc(order)
        data["id"] = data.pop("_id")
        serialized_orders.append(data)

    return {
        "count": len(serialized_orders),
        "orders": serialized_orders
    }


@router.get("/{order_id}")
def get_order_by_id(order_id: str):
    if not ObjectId.is_valid(order_id):
        raise HTTPException(status_code=400, detail="Invalid order ID format.")

    order = order_collection.find_one({"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")

    data = serialize_doc(order)
    data["id"] = data.pop("_id")
    return data


@router.get("/customer/{customer_id}")
def get_orders_by_customer(customer_id: str, current_user: dict = Depends(get_current_user)):
    # Only allow users to view their own orders
    if customer_id != current_user["email"]:
        raise HTTPException(status_code=403, detail="Access denied: Cannot view other customer's orders")
    orders = list(order_collection.find({"customer_id": customer_id}).sort("created_at", -1))

    serialized_orders = []
    for order in orders:
        data = serialize_doc(order)
        data["id"] = data.pop("_id")
        serialized_orders.append(data)

    return {
        "customer_id": customer_id,
        "count": len(serialized_orders),
        "orders": serialized_orders
    }


@router.put("/{order_id}/status")
def update_order_status(order_id: str, payload: OrderStatusUpdate):
    if not ObjectId.is_valid(order_id):
        raise HTTPException(status_code=400, detail="Invalid order ID format.")

    existing_order = order_collection.find_one({"_id": ObjectId(order_id)})
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found.")

    order_collection.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"order_status": payload.order_status.upper()}}
    )

    updated_order = order_collection.find_one({"_id": ObjectId(order_id)})
    data = serialize_doc(updated_order)
    data["id"] = data.pop("_id")

    return {
        "message": "Order status updated successfully.",
        "order": data
    }


@router.put("/{order_id}/payment-status")
def update_payment_status(order_id: str, payload: PaymentStatusUpdate):
    if not ObjectId.is_valid(order_id):
        raise HTTPException(status_code=400, detail="Invalid order ID format.")

    existing_order = order_collection.find_one({"_id": ObjectId(order_id)})
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found.")

    order_collection.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"payment_status": payload.payment_status.upper()}}
    )

    updated_order = order_collection.find_one({"_id": ObjectId(order_id)})
    data = serialize_doc(updated_order)
    data["id"] = data.pop("_id")

    return {
        "message": "Payment status updated successfully.",
        "order": data
    }