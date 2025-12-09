from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

app = FastAPI(title="BUTIL API")

# Allow your React Native app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to MongoDB
client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
db = client.butil_db
predictions = db.predictions

class PredictIn(BaseModel):
    rainfall: float
    fertilizer: float
    ph: float
    user_id: str = "guest"

class PredictOut(BaseModel):
    yield_mt_ha: str
    consistency: str
    message: str

def calculate_yield(rainfall: float, fertilizer: float, ph: float):
    base = 4.0
    rain = min(rainfall / 150, 1.5)
    fert = min(fertilizer / 80, 1.4)
    ph_score = 1.5 if 6.0 <= ph <= 7.2 else 0.8
    total = base + rain + fert + ph_score
    return {
        "yield_mt_ha": f"{total:.1f}",
        "consistency": f"{int(70 + (total - 5) * 10)}%",
        "message": "Excellent conditions!" if total > 6.8 else "Good – can improve"
    }

@app.get("/")
async def home():
    return {"message": "BUTIL API + MongoDB Running!"}

@app.post("/predict", response_model=PredictOut)
async def predict(data: PredictIn):
    result = calculate_yield(data.rainfall, data.fertilizer, data.ph)
    
    # Save to MongoDB
    await predictions.insert_one({
        "user_id": data.user_id,
        "input": data.dict(),
        "output": result,
        "timestamp": datetime.utcnow()
    })
    
    return PredictOut(**result)