import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

# Try to connect to MongoDB, fallback to memory if fails
try:
    client = MongoClient(MONGO_URL)
    db = client[os.getenv("DB_NAME", "catalogue_db")]
    product_collection = db[os.getenv("COLLECTION_NAME", "products")]
    # Test connection
    client.admin.command('ping')
    print("Connected to MongoDB")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    print("Using in-memory database")
    from app.database_memory import product_collection