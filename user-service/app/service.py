from app.database import user_collection
from app.auth import create_token
from passlib.hash import bcrypt
from bson import ObjectId


class UserService:

    # ✅ REGISTER (CREATE USER)
    def register(self, user_data):
        # check existing user
        if user_collection.find_one({"email": user_data.email}):
            return {"error": "User already exists"}

        user = user_data.dict()

        # 🔥 FIX: limit password to 72 characters
        password = user["password"][:72]

        # hash password
        user["password"] = bcrypt.hash(password)

        result = user_collection.insert_one(user)

        return {
            "message": "User created successfully",
            "id": str(result.inserted_id)
        }

    # ✅ LOGIN
    def login(self, login_data):
        user = user_collection.find_one({"email": login_data.email})

        # 🔥 FIX: limit password to 72 characters
        password = login_data.password[:72]

        # verify password
        if not user or not bcrypt.verify(password, user["password"]):
            return None

        token = create_token({"sub": user["email"]})

        return {"access_token": token}

    # ✅ GET ALL USERS
    def get_all_users(self):
        users = []
        for user in user_collection.find():
            user["_id"] = str(user["_id"])
            user.pop("password", None)  # remove password
            users.append(user)
        return users

    # ✅ GET SINGLE USER
    def get_user(self, user_id):
        user = user_collection.find_one({"_id": ObjectId(user_id)})

        if not user:
            return None

        user["_id"] = str(user["_id"])
        user.pop("password", None)

        return user

    # ✅ UPDATE USER
    def update_user(self, user_id, update_data):
        update_dict = {
            k: v for k, v in update_data.dict().items() if v is not None
        }

        # 🔥 FIX: handle password update safely
        if "password" in update_dict:
            password = update_dict["password"][:72]
            update_dict["password"] = bcrypt.hash(password)

        result = user_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_dict}
        )

        return result.modified_count > 0

    # ✅ DELETE USER
    def delete_user(self, user_id):
        result = user_collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0