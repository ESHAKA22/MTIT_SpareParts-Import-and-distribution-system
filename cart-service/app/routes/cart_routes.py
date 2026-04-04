from fastapi import APIRouter, HTTPException, Depends
from app.database import cart_collection
from app.schemas import CartItemCreate, CartItemUpdate
from app.utils import serialize_doc
from app.auth import get_current_user



router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("/health")
def health_check():
    return {"status": "ok", "service": "cart-service"}


@router.post("/add")
def add_to_cart(payload: CartItemCreate, current_user: dict = Depends(get_current_user)):
    # Use email from JWT token as customer_id
    customer_id = current_user["email"]
    existing_item = cart_collection.find_one(
        {
            "customer_id": customer_id,
            "product_id": payload.product_id
        }
    )

    if existing_item:
        new_quantity = existing_item["quantity"] + payload.quantity
        new_subtotal = round(new_quantity * existing_item["unit_price"], 2)

        cart_collection.update_one(
            {"_id": existing_item["_id"]},
            {
                "$set": {
                    "quantity": new_quantity,
                    "subtotal": new_subtotal
                }
            }
        )

        updated_item = cart_collection.find_one({"_id": existing_item["_id"]})
        item = serialize_doc(updated_item)
        item["id"] = item.pop("_id")
        return {
            "message": "Item already existed. Quantity updated successfully.",
            "item": item
        }

    new_item = {
        "customer_id": customer_id,
        "product_id": payload.product_id,
        "product_name": payload.product_name,
        "unit_price": payload.unit_price,
        "quantity": payload.quantity,
        "subtotal": round(payload.unit_price * payload.quantity, 2)
    }

    result = cart_collection.insert_one(new_item)
    created_item = cart_collection.find_one({"_id": result.inserted_id})
    item = serialize_doc(created_item)
    item["id"] = item.pop("_id")

    return {
        "message": "Item added to cart successfully.",
        "item": item
    }


@router.get("/")
def get_cart(current_user: dict = Depends(get_current_user)):
    customer_id = current_user["email"]
    items = list(cart_collection.find({"customer_id": customer_id}))

    if not items:
        return {
            "customer_id": customer_id,
            "items": [],
            "total_amount": 0
        }

    serialized_items = []
    total_amount = 0

    for item in items:
        s_item = serialize_doc(item)
        s_item["id"] = s_item.pop("_id")
        serialized_items.append(s_item)
        total_amount += s_item["subtotal"]

    return {
        "customer_id": customer_id,
        "items": serialized_items,
        "total_amount": round(total_amount, 2)
    }


@router.put("/item/{item_id}")
def update_cart_item(item_id: str, payload: CartItemUpdate):
    from bson import ObjectId

    existing_item = cart_collection.find_one({"_id": ObjectId(item_id)})
    if not existing_item:
        raise HTTPException(status_code=404, detail="Cart item not found.")

    new_subtotal = round(existing_item["unit_price"] * payload.quantity, 2)

    cart_collection.update_one(
        {"_id": ObjectId(item_id)},
        {
            "$set": {
                "quantity": payload.quantity,
                "subtotal": new_subtotal
            }
        }
    )

    updated_item = cart_collection.find_one({"_id": ObjectId(item_id)})
    item = serialize_doc(updated_item)
    item["id"] = item.pop("_id")

    return {
        "message": "Cart item updated successfully.",
        "item": item
    }


@router.delete("/item/{item_id}")
def remove_cart_item(item_id: str):
    from bson import ObjectId

    existing_item = cart_collection.find_one({"_id": ObjectId(item_id)})
    if not existing_item:
        raise HTTPException(status_code=404, detail="Cart item not found.")

    cart_collection.delete_one({"_id": ObjectId(item_id)})
    return {"message": "Cart item removed successfully."}


@router.delete("/clear")
def clear_cart(current_user: dict = Depends(get_current_user)):
    customer_id = current_user["email"]
    result = cart_collection.delete_many({"customer_id": customer_id})
    return {
        "message": "Cart cleared successfully.",
        "deleted_count": result.deleted_count
    }

