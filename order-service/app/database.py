import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "order_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "orders")

client = MongoClient(MONGO_URL)
db = client[DB_NAME]
order_collection = db[COLLECTION_NAME]