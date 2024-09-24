import uuid, pytz
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.models.user import User
from app.models.updateRequest import UpdateRequest
from app.database.database import create_connection
from app.utils.jwt_utils import create_access_token, create_refresh_token
from datetime import timedelta
from datetime import datetime

conn = create_connection()

def register_user(user: User):
    cursor = conn.cursor()
    try:
        # Ensure the phone number is passed as a tuple
        cursor.execute("SELECT * FROM users WHERE phone_number = %s;", (user.phone_number,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            return JSONResponse(
                status_code=400,
                content={"message": "Phone Number already registered"},  # Custom structure
            )
        
        user.hash_password()  
        
        user_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO users (user_id, first_name, last_name, phone_number, address, pin) VALUES (%s, %s, %s, %s, %s, %s) RETURNING user_id, first_name, last_name, phone_number, address, created_at;",
            (user_id, user.first_name, user.last_name, user.phone_number, user.address, user.pin)
        )
        user_data = cursor.fetchone()  # Fetch the returned row
        conn.commit()
        
        # Adjust indices based on your table schema
        return JSONResponse(
            status_code=200,
            content={
                "status":"SUCCESS",
                "result":{
                        "user_id": user_data[0],            # user_id
                        "first_name": user_data[1],         # first_name
                        "last_name": user_data[2],          # last_name
                        "phone_number": user_data[3],       # phone_number
                        "address": user_data[4],            # address
                        "created_date": str(user_data[5])        # created_at or whatever the correct column is
                    }
            }
        )        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        
def login_user(phone_number: str, pin: str):
    cursor = conn.cursor()
    try:
        # Fetch user by phone_number
        cursor.execute("SELECT * FROM users WHERE phone_number = %s;", (phone_number,))
        user = cursor.fetchone()
        
        if not user:
            return JSONResponse(
                status_code=404,
                content={"message": "Phone Number and PIN doesn't match."}
            )
        
        # Check the hashed pin (password)
        hashed_pin = user[5]  # Assuming 'pin' is at index 5
        # if not bcrypt.checkpw(pin.encode(), hashed_pin.encode()):
        if not User.verify_password(pin, hashed_pin):
            return JSONResponse(
                status_code=401,
                content={"message": "Phone Number and PIN doesn't match."}
            )

        # Generate access and refresh tokens
        access_token = create_access_token(data={"user_id": user[0]}, expires_delta=timedelta(minutes=15))
        refresh_token = create_refresh_token(data={"user_id": user[0]}, expires_delta=timedelta(days=7))

        # Return tokens in the response
        return JSONResponse(
                status_code=201,
                content={
                    "status": "SUCCESS",
                    "result":{
                        "access_token":access_token,
                        "refresh_token":refresh_token
                    }
                }
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()

def update_user(user_id: str, update_request: UpdateRequest):
    cursor = conn.cursor()
    try:
        # Fetch the current user data
        cursor.execute("SELECT * FROM users WHERE user_id = %s;", (user_id,))
        current_user = cursor.fetchone()

        if not current_user:
            return JSONResponse(
                status_code=404,
                content={"message": "User not found"}
            )

        # Prepare the update fields
        update_fields = {}
        if update_request.first_name is not None:
            update_fields['first_name'] = update_request.first_name
        if update_request.last_name is not None:
            update_fields['last_name'] = update_request.last_name
        if update_request.address is not None:
            update_fields['address'] = update_request.address

        jakarta_tz = pytz.timezone('Asia/Jakarta')
        update_fields['updated_at'] = datetime.now(jakarta_tz)

        # Update user data
        if update_fields:
            set_clause = ", ".join([f"{key} = %s" for key in update_fields.keys()])
            values = list(update_fields.values())
            values.append(user_id)

            cursor.execute(f"UPDATE users SET {set_clause} WHERE user_id = %s RETURNING user_id, first_name, last_name, address, updated_at;", values)
            updated_user = cursor.fetchone()
            conn.commit()

        return JSONResponse(
            status_code=200,
                content={
                    "status": "SUCCESS",
                    "result":{
                        "user_id":updated_user[0],
                        "first_name":updated_user[1],
                        "last_name":updated_user[2],
                        "address":updated_user[3],
                        "updated_date":str(updated_user[4])
                    }
                }
        )

    except Exception as e:
        conn.rollback()
        return JSONResponse(
            status_code=500,
            content={"message": str(e)}
        )
    finally:
        cursor.close()
