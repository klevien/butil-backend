from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")  # get from Atlas later
client = AsyncIOMotorClient(MONGODB_URL)
db = client.butil_db

# Collections
users = db.users
predictions = db.predictions
recommendations = db.recommendations