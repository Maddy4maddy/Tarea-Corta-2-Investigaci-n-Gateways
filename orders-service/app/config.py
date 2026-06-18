from pymongo import MongoClient

class Config:
    MONGO_URI = "mongodb://localhost:27017"
    DATABASE_NAME = "ordenes_db"

client = MongoClient(Config.MONGO_URI)

db = client[Config.DATABASE_NAME]

ordenes_collection = db["ordenes"]