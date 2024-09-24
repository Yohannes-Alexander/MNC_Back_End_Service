import uuid
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.database.database import create_connection

conn = create_connection()

def transaction_get(user_id: str):
    cursor = conn.cursor()
    try:
        # Fetching top_up transactions
        cursor.execute("""
            SELECT top_up_id, status, user_id, transaction_type, amount_top_up AS amount, '' AS remarks, balance_before, balance_after, created_at 
            FROM top_up WHERE user_id = %s;
        """, (user_id,))
        top_up = cursor.fetchall()
        top_up_columns = [desc[0] for desc in cursor.description]

        # Fetching payment transactions
        cursor.execute("""
            SELECT payment_id, status, user_id, transaction_type, amount, remarks, balance_before, balance_after, created_at 
            FROM payments WHERE user_id = %s;
        """, (user_id,))
        payment = cursor.fetchall()
        payment_columns = [desc[0] for desc in cursor.description]

        # Fetching transfer transactions
        cursor.execute("""
            SELECT transfer_id, status, user_id, transaction_type, amount, remarks, balance_before, balance_after, created_at 
            FROM transfers WHERE user_id = %s;
        """, (user_id,))
        transfer = cursor.fetchall()
        transfer_columns = [desc[0] for desc in cursor.description]

        conn.commit()

        # Format results as a list of dictionaries
        top_up_array = [dict(zip(top_up_columns, row)) for row in top_up]
        
        payment_array = [dict(zip(payment_columns, row)) for row in payment]

        transfer_array = [dict(zip(transfer_columns, row)) for row in transfer]

        # Combine all arrays into a single array
        combined_array = top_up_array + payment_array + transfer_array

        for transaction in combined_array:
            if transaction['created_at']:
                transaction['created_at'] = transaction['created_at'].strftime("%Y-%m-%d %H:%M:%S")

        # Sort combined_array by created_at in descending order
        combined_array = sorted(combined_array, key=lambda x: x['created_at'], reverse=True)

        # Return a success response with combined transaction details
        return JSONResponse(
            status_code=200,
            content={
                "status": "SUCCESS",
                "result": combined_array  # Correctly return combined_array as a list
            }
        )

    except Exception as e:
        conn.rollback()
        return JSONResponse(
            status_code=500,
            content={"message": str(e)}
        )
    finally:
        cursor.close()  # Ensure cursor is closed
