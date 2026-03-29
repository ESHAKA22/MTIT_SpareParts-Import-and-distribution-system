from fastapi import FastAPI
from app.routes.complaint_routes import router

app = FastAPI(title="Complaint Service")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Complaint Service Running"}