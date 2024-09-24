from pydantic import BaseModel

class TransferRequest(BaseModel):
    target_user: str
    amount: int
    remarks: str