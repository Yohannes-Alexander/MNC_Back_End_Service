from pydantic import BaseModel
from typing import Optional


class UpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
