from fastapi import APIRouter, HTTPException
from app.models import UserCreate, UserLogin, UserUpdate   # ✅ fixed import
from app.service import UserService                        # ✅ fixed import

router = APIRouter()
user_service = UserService()


# ✅ REGISTER
@router.post("/register")
def register(user: UserCreate):
    result = user_service.register(user)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


# ✅ LOGIN
@router.post("/login")
def login(user: UserLogin):
    result = user_service.login(user)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return result


# ✅ GET ALL USERS
@router.get("/")
def get_users():
    return user_service.get_all_users()


# ✅ GET SINGLE USER
@router.get("/{user_id}")
def get_user(user_id: str):
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ✅ UPDATE USER
@router.put("/{user_id}")
def update_user(user_id: str, user: UserUpdate):
    success = user_service.update_user(user_id, user)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated successfully"}


# ✅ DELETE USER
@router.delete("/{user_id}")
def delete_user(user_id: str):
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}