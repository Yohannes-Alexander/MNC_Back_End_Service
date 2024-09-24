import uuid
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.database.database import create_connection
from app.models.paymentRequest import  PaymentRequest

conn = create_connection()

def payment_user(user_id: str, payment_request : PaymentRequest):
    cursor = conn.cursor()
    try:
        # Fetch the current balance of the user
        cursor.execute("SELECT balance FROM users WHERE user_id = %s;", (user_id,))
        user = cursor.fetchone()

        if not user:
            return JSONResponse(
                status_code=404,
                content={"message": "Unauthenticated"}
            )

        current_balance = user[0]  # Assuming the balance is the first column

        if ((current_balance-payment_request.amount)<0):

            return JSONResponse(
                status_code=400,
                content={"message": "Balance is not enough"}
            )
        
        new_balance = current_balance - payment_request.amount

        # Update user's balance
        cursor.execute(
            "UPDATE users SET balance = %s WHERE user_id = %s RETURNING balance;",
            (new_balance, user_id)
        )
        updated_balance = cursor.fetchone()[0]  # Fetch the updated balance

        # Insert into top_up table
        cursor.execute(
            "INSERT INTO payments (payment_id, amount, remarks, balance_before, balance_after, user_id, status, transaction_type) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING payment_id, amount, remarks, balance_before, balance_after, created_at;",
            (str(uuid.uuid4()), payment_request.amount, payment_request.remarks, current_balance, new_balance, user_id, "SUCCESS", "DEBIT")
        )
        payment_data = cursor.fetchone()  # Fetch the inserted top-up data

        conn.commit()

        # Return a success response with the updated balance and top-up details
        return JSONResponse(
            status_code=200,
            content={
                "status": "SUCCESS",
                "result": {
                    "payment_id": payment_data[0],            # top_up_id
                    "amount": payment_data[1],
                    "remarks" : payment_data[2],
                    "balance_before": payment_data[2],       # balance_before
                    "balance_after": payment_data[3],        # balance_after
                    "created_date": str(payment_data[4]),           # created_at
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