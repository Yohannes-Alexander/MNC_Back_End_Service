from pydantic import BaseModel
from typing import Optional
import bcrypt

class User(BaseModel):
    user_id : Optional[str] = None
    first_name: str
    last_name: str
    phone_number: str
    address: str
    pin: str
    refresh_token: Optional[str] = None  # Nullable field
    created_at: Optional[str] = None  # Nullable field
    updated_at: Optional[str] = None  # Nullable field

    def hash_password(self):
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        self.pin = bcrypt.hashpw(self.pin.encode(), salt).decode()

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        # Verify the password against the stored hash
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
