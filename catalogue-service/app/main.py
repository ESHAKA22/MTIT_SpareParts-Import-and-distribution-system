from fastapi import FastAPI
from app.routes.product_routes import router as product_router

app = FastAPI(title="Catalogue Service")

app.include_router(product_router)

@app.get("/")
def root():
    return {"message": "Catalogue Service Running"}