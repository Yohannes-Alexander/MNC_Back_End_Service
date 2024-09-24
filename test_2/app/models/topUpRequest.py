from pydantic import BaseModel

class TopUpRequest(BaseModel):
    amount: int