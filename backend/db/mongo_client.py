from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client["docuchat"]
documents_col = db["documents"]
chunks_col = db["chunks"]
queries_col = db["queries"]