import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="pass",
        database="ecommerce_shipping"
    )

def normalize_id(trx_id):
    try:
        return str(int(float(trx_id)))
    except Exception:
        return str(trx_id)

def get_order(transaction_id: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    trx_id = normalize_id(transaction_id)

    query = "SELECT * FROM orders WHERE Transaction_ID = %s"
    cursor.execute(query, (trx_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return result

def update_email(transaction_id: str, new_email: str):
    conn = get_connection()
    cursor = conn.cursor()

    trx_id = normalize_id(transaction_id)

    query = "UPDATE orders SET Email = %s WHERE Transaction_ID = %s"
    cursor.execute(query, (new_email, trx_id))
    conn.commit()

    cursor.close()
    conn.close()

def update_name(transaction_id: str, new_name: str):
    conn = get_connection()
    cursor = conn.cursor()

    trx_id = normalize_id(transaction_id)

    query = "UPDATE orders SET Name = %s WHERE Transaction_ID = %s"
    cursor.execute(query, (new_name, trx_id))
    conn.commit()

    cursor.close()
    conn.close()

def update_phone(transaction_id: str, new_phone: str):
    conn = get_connection()
    cursor = conn.cursor()

    trx_id = normalize_id(transaction_id)

    query = "UPDATE orders SET Phone = %s WHERE Transaction_ID = %s"
    cursor.execute(query, (new_phone, trx_id))
    conn.commit()

    cursor.close()
    conn.close()
