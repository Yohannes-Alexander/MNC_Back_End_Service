import uuid
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.database.database import create_connection
from app.models.topUpRequest import TopUpRequest


conn = create_connection()

def top_up_user(user_id: str, topup_request: TopUpRequest):
    cursor = conn.cursor()
    try:
        # Fetch the current balance of the user
        cursor.execute("SELECT balance FROM users WHERE user_id = %s;", (user_id,))
        user = cursor.fetchone()

        if not user:
            return JSONResponse(
                status_code=404,
                content={"message": "User not found or Unauthenticated"}
            )

        current_balance = user[0]  # Assuming the balance is the first column
        new_balance = current_balance + topup_request.amount

        # Update user's balance
        cursor.execute(
            "UPDATE users SET balance = %s WHERE user_id = %s RETURNING balance;",
            (new_balance, user_id)
        )
        updated_balance = cursor.fetchone()[0]  # Fetch the updated balance

        # Insert into top_up table
        cursor.execute(
            "INSERT INTO top_up (top_up_id, amount_top_up, balance_before, balance_after, user_id, status, transaction_type) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING top_up_id, amount_top_up, balance_before, balance_after, created_at;",
            (str(uuid.uuid4()), topup_request.amount, current_balance, new_balance, user_id, "SUCCESS", "CREDIT")
        )
        top_up_data = cursor.fetchone()  # Fetch the inserted top-up data

        conn.commit()

        # Return a success response with the updated balance and top-up details
        return JSONResponse(
            status_code=200,
            content={
                "status": "SUCCESS",
                "result": {
                    "top_up_id": top_up_data[0],            # top_up_id
                    "amount_top_up": top_up_data[1],        # amount_top_up
                    "balance_before": top_up_data[2],       # balance_before
                    "balance_after": top_up_data[3],        # balance_after
                    "created_date": str(top_up_data[4]),           # created_at
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