import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "assessment_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "employees")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]
employees_collection = db[COLLECTION_NAME]
