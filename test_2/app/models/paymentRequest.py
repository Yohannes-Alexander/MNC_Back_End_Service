from pydantic import BaseModel

class PaymentRequest(BaseModel):
    amount: int
    remarks: str