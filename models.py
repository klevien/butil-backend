from pydantic import BaseModel
from typing import Optional

class PredictionInput(BaseModel):
    rainfall: float
    fertilizer: float
    ph: float
    user_id: str  # from Firebase UID

class PredictionResponse(BaseModel):
    yield_mt_ha: str
    consistency: str
    message: str