import jwt, os, pytz
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

JAKARTA_TZ = pytz.timezone('Asia/Jakarta')
# Function to create an access token with Jakarta timezone
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    
    # Use Jakarta timezone for expiration time
    if expires_delta:
        expire = datetime.now(JAKARTA_TZ) + expires_delta
    else:
        expire = datetime.now(JAKARTA_TZ) + timedelta(minutes=15)  # Default 15 minutes expiration
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to create a refresh token with Jakarta timezone
def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    
    # Use Jakarta timezone for expiration time
    if expires_delta:
        expire = datetime.now(JAKARTA_TZ) + expires_delta
    else:
        expire = datetime.now(JAKARTA_TZ) + timedelta(days=7)  # Default 7 days expiration
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

    
def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            return JSONResponse(
                status_code=401,
                content={
                    "message":"Unauthenticated"
                }
            )  
        return user_id
    except jwt.ExpiredSignatureError:
        return JSONResponse(
            status_code=401,
            content={
                "message":"Unauthenticated"
            }
        )          
    except jwt.JWTError:
        return JSONResponse(
            status_code=401,
            content={
                "message":"Unauthenticated"
            }
        )  
    

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def get_current_user_id(token: str = Depends(oauth2_scheme)):
    user_id = decode_jwt_token(token)
    if not user_id:
        return JSONResponse(
            status_code=401,
            content={
                "message":"Unauthenticated"
            }
        )  
    return user_id

    
    
