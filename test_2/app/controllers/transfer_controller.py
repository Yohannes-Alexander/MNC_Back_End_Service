import uuid
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.database.database import create_connection
from app.models.transferRequest import  TransferRequest

import uuid
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.database.database import create_connection
from app.models.transferRequest import  TransferRequest

conn = create_connection()

def transfer_user(user_id: str, transfer_request : TransferRequest):
    cursor = conn.cursor()
    try:
        
        cursor.execute("SELECT balance FROM users WHERE user_id = %s;", (transfer_request.target_user,))
        sender = cursor.fetchone()

        if not sender:
            return JSONResponse(
                status_code=404,
                content={"message": "Unauthenticated"}
            )
        
        # Fetch the current balance of the user
        cursor.execute("SELECT balance FROM users WHERE user_id = %s;", (user_id,))
        user = cursor.fetchone()

        if not user:
            return JSONResponse(
                status_code=404,
                content={"message": "Unauthenticated"}
            )

        current_balance = user[0]  # Assuming the balance is the first column

        if ((current_balance-transfer_request.amount)<0):

            return JSONResponse(
                status_code=400,
                content={"message": "Balance is not enough"}
            )
        
        new_balance = current_balance - transfer_request.amount

        # Update user's balance
        cursor.execute(
            "UPDATE users SET balance = %s WHERE user_id = %s RETURNING balance;",
            (new_balance, user_id)
        )
        updated_balance = cursor.fetchone()[0]  # Fetch the updated balance

        # Update sender's balance
        cursor.execute(
            "UPDATE users SET balance = %s WHERE user_id = %s RETURNING balance;",
            (sender[0]+transfer_request.amount, transfer_request.target_user)
        )
        updated_balance = cursor.fetchone()[0]  # Fetch the updated balance        

        # Insert into top_up table
        cursor.execute(
            "INSERT INTO transfers (transfer_id, amount, remarks, balance_before, balance_after, user_id, target_user_id, status, transaction_type) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING transfer_id, amount, remarks, balance_before, balance_after, created_at;",
            (str(uuid.uuid4()), transfer_request.amount, transfer_request.remarks, current_balance, new_balance, user_id, transfer_request.target_user,"SUCCESS", "DEBIT")
        )
        transfer_data = cursor.fetchone()  # Fetch the inserted top-up data

        conn.commit()

        # Return a success response with the updated balance and top-up details
        return JSONResponse(
            status_code=200,
            content={
                "status": "SUCCESS",
                "result": {
                    "transfer_id": transfer_data[0],            # top_up_id
                    "amount": transfer_data[1],
                    "remarks" : transfer_data[2],
                    "balance_before": transfer_data[2],       # balance_before
                    "balance_after": transfer_data[3],        # balance_after
                    "created_date": str(transfer_data[4]),           # created_at
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