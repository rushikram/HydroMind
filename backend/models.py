from pydantic import BaseModel

class WaterEntry(BaseModel):
    user_id: str
    amount_ml: int

class ResetRequest(BaseModel):
    user_id: str
