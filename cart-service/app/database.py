import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

# Try to connect to MongoDB, fallback to memory if fails
try:
    client = MongoClient(MONGO_URL)
    db = client.get_database(os.getenv("DB_NAME", "cart_db"))
    cart_collection = db.get_collection(os.getenv("COLLECTION_NAME", "carts"))
    # Test connection
    client.admin.command('ping')
    print("Connected to MongoDB")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    print("Using in-memory database")
    from app.database_memory import cart_collection