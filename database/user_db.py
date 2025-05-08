from dotenv import load_dotenv
from datetime import datetime
from typing import List, Dict
from database import get_db_connection
from uuid import UUID
from decimal import Decimal

def init_user_info():
    """Initialize user_info table if it doesn't exist"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS user_info (
                    id SERIAL PRIMARY KEY,
                    email TEXT,
                    password TEXT,
                    username TEXT,
                    fullname VARCHAR(255),
                    gender VARCHAR(50),
                    threads TEXT[], 
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        conn.commit()


def append_thread(user_id: int, thread_id: str) -> Dict:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE user_info
                SET threads = array_append(threads, %s)
                WHERE id = %s
                RETURNING *;
                """,
                (thread_id, user_id)
            )
            result = cur.fetchone()
        conn.commit()
        return result

def save_user_info(email: str, password:str, fullname: str, gender: str) -> Dict:
    """Insert user information into database"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO user_info (email, password, fullname, gender, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING *
                """,
                (email, password, fullname, gender,
                 datetime.now(), datetime.now())
            )
            result = cur.fetchone()
        conn.commit()
        return result

def get_user_info_by_email(email: str) -> Dict:
    """Get user information by email"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM user_info WHERE email = %s
                """,
                (email,)
            )
            result = cur.fetchone()
        return result


init_user_info()
