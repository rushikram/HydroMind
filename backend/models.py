from pydantic import BaseModel, Field

class WaterEntry(BaseModel):
    amount_ml: int = Field(..., gt=0, description="Amount of water in milliliters (must be > 0)")

class UserQuery(BaseModel):
    question: str = Field(..., min_length=3, description="Question for the AI hydration coach")

