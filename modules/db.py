from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017")
db = client["resumeiq"]
collection = db["analysis_results"]

def save_result(data):
    data_to_store = data.copy()
    data_to_store["timestamp"] = datetime.utcnow()
    collection.insert_one(data_to_store)

