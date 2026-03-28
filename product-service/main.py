from fastapi import FastAPI, HTTPException, status
from typing import List
from models import Product, ProductCreate, ProductUpdate
from service import ProductService

app = FastAPI(title="Product Microservice", version="1.0.0")

product_service = ProductService()


@app.get("/")
def root():
    return {"message": "Product Service is running"}


# 🔹 Get all products
@app.get("/api/products")
def get_all_products():
    return product_service.get_all()


# 🔹 Get product by ID (IMPORTANT: string ID for MongoDB)
@app.get("/api/products/{product_id}")
def get_product(product_id: str):
    product = product_service.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# 🔹 Create product
@app.post("/api/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    return product_service.create(product)


# 🔹 Update product
@app.put("/api/products/{product_id}")
def update_product(product_id: str, product: ProductUpdate):
    updated = product_service.update(product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated


# 🔹 Delete product
@app.delete("/api/products/{product_id}")
def delete_product(product_id: str):
    success = product_service.delete(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}