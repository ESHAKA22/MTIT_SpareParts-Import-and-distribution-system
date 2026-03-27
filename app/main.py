import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.order_routes import router as order_router

load_dotenv()

SERVICE_NAME = os.getenv("SERVICE_NAME", "Order Service")

app = FastAPI(
    title=SERVICE_NAME,
    description="Microservice for managing customer orders.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(order_router)


@app.get("/")
def root():
    return {
        "message": f"{SERVICE_NAME} is running"
    }