from fastapi import FastAPI
from .models.user import User
from .models.userLogin import UserLogin
from .controllers.user_controller import register_user
from .controllers.user_controller import login_user
from .controllers.topup_controller import top_up_user
from .controllers.payment_controller import payment_user
from .controllers.transfer_controller import transfer_user
from .controllers.user_controller import update_user
from .controllers.transaction_controller import transaction_get
from app.utils.jwt_utils import get_current_user_id
from fastapi import Depends
from app.models.topUpRequest import TopUpRequest
from app.models.paymentRequest import PaymentRequest
from app.models.transferRequest import TransferRequest
from app.models.updateRequest import UpdateRequest
# from app.routers.item_router import router as item_router

app = FastAPI()

# app.include_router(item_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

@app.post("/register")
async def register(user:User):
    return register_user(user)

@app.post("/login")
async def login(user: UserLogin):
    return login_user(user.phone_number, user.pin)

@app.post("/topup")
async def topup(topup_request: TopUpRequest, user_id: str = Depends(get_current_user_id)):
    return top_up_user(user_id, topup_request)

@app.post("/pay")
async def topup(payment_request: PaymentRequest, user_id: str = Depends(get_current_user_id)):
    return payment_user(user_id, payment_request)

@app.post("/transfer")
async def topup(transfer_request: TransferRequest, user_id: str = Depends(get_current_user_id)):
    return transfer_user(user_id, transfer_request)

@app.put("/profile")
async def topup(update_request: UpdateRequest, user_id: str = Depends(get_current_user_id)):
    return update_user(user_id, update_request)

@app.get("/transactions")
async def topup(user_id: str = Depends(get_current_user_id)):
    return transaction_get(user_id)
