from dotenv import load_dotenv
from datetime import datetime
from typing import List, Dict
from database import get_db_connection
from uuid import UUID


def get_all_universities() :
    """
    Lấy thông tin tất cả các trường đại học từ database.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM universities")
            universities = cur.fetchall()
        return universities


def get_university_sections_id( university_id: int):
    """
    Lấy thông tin các section của trường đại học từ database
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM university_sections WHERE university_id = %s", (university_id,))
            sections = cur.fetchall()
    return sections

        
   