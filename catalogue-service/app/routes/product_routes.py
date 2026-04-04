import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from app.database import product_collection
from app.utils import serialize
from app.auth import get_current_user
from bson import ObjectId
import shutil

router = APIRouter(prefix="/products", tags=["Products"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# CREATE PRODUCT WITH IMAGE
@router.post("/")
async def create_product(
    name: str = Form(...),
    category: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    file_path = f"{UPLOAD_DIR}/{image.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    product = {
        "name": name,
        "category": category,
        "price": price,
        "stock": stock,
        "description": description,
        "image": file_path
    }

    result = product_collection.insert_one(product)
    created = product_collection.find_one({"_id": result.inserted_id})

    return serialize(created)


# GET ALL PRODUCTS
@router.get("/")
def get_products():
    products = list(product_collection.find())
    return [serialize(p) for p in products]


# GET SINGLE PRODUCT
@router.get("/{product_id}")
def get_product(product_id: str):
    product = product_collection.find_one({"_id": ObjectId(product_id)})

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return serialize(product)


# UPDATE PRODUCT
@router.put("/{product_id}")
def update_product(product_id: str, data: dict, current_user: dict = Depends(get_current_user)):
    product_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": data}
    )

    updated = product_collection.find_one({"_id": ObjectId(product_id)})
    return serialize(updated)


# DELETE PRODUCT
@router.delete("/{product_id}")
def delete_product(product_id: str, current_user: dict = Depends(get_current_user)):
    product_collection.delete_one({"_id": ObjectId(product_id)})
    return {"message": "Product deleted"}