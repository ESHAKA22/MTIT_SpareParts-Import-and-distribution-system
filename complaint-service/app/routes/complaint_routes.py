from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from bson import ObjectId
from app.database import complaint_collection
from app.schemas import ComplaintCreate, ComplaintUpdate
from app.utils import serialize
from app.auth import get_current_user

router = APIRouter(prefix="/complaints", tags=["Complaints"])


# CREATE COMPLAINT
@router.post("/")
def create_complaint(data: ComplaintCreate, current_user: dict = Depends(get_current_user)):
    # Use email from JWT token as customer_id
    customer_id = current_user["email"]
    complaint = {
        "customer_id": customer_id,
        "order_id": data.order_id,
        "subject": data.subject,
        "description": data.description,
        "status": "OPEN",
        "response_message": None,
        "created_at": datetime.utcnow().isoformat()
    }

    result = complaint_collection.insert_one(complaint)
    created = complaint_collection.find_one({"_id": result.inserted_id})

    return serialize(created)


# GET ALL COMPLAINTS
@router.get("/")
def get_all(current_user: dict = Depends(get_current_user)):
    customer_id = current_user["email"]
    complaints = list(complaint_collection.find({"customer_id": customer_id}))
    return [serialize(c) for c in complaints]


# GET BY CUSTOMER
@router.get("/customer/{customer_id}")
def get_by_customer(customer_id: str, current_user: dict = Depends(get_current_user)):
    # Only allow users to view their own complaints
    if customer_id != current_user["email"]:
        raise HTTPException(status_code=403, detail="Access denied: Cannot view other customer's complaints")
    complaints = list(complaint_collection.find({"customer_id": customer_id}))
    return [serialize(c) for c in complaints]


# GET BY ORDER
@router.get("/order/{order_id}")
def get_by_order(order_id: str):
    complaints = list(complaint_collection.find({"order_id": order_id}))
    return [serialize(c) for c in complaints]


# UPDATE COMPLAINT
@router.put("/{complaint_id}")
def update_complaint(complaint_id: str, data: ComplaintUpdate):
    existing = complaint_collection.find_one({"_id": ObjectId(complaint_id)})

    if not existing:
        raise HTTPException(status_code=404, detail="Complaint not found")

    update_data = {k: v for k, v in data.dict().items() if v is not None}

    complaint_collection.update_one(
        {"_id": ObjectId(complaint_id)},
        {"$set": update_data}
    )

    updated = complaint_collection.find_one({"_id": ObjectId(complaint_id)})
    return serialize(updated)


# DELETE
@router.delete("/{complaint_id}")
def delete_complaint(complaint_id: str):
    complaint_collection.delete_one({"_id": ObjectId(complaint_id)})
    return {"message": "Complaint deleted"}