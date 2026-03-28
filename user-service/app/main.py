from fastapi import FastAPI
from app.routes.user_routes import router   # ✅ FIXED IMPORT

app = FastAPI(title="User Microservice")

# include user routes
app.include_router(router, prefix="/api/users")

@app.get("/")
def root():
    return {"message": "User Service Running"}