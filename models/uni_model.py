from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from decimal import Decimal


# CREATE TABLE universities (
#     id SERIAL PRIMARY KEY,
#     name TEXT NOT NULL,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );

# -- Bảng lưu từng section nội dung (Giới thiệu, Tuyển sinh, Tin tức...)
# CREATE TABLE university_sections (
#     id SERIAL PRIMARY KEY,
#     university_id INT REFERENCES universities(id),
#     section_title TEXT NOT NULL,
#     content TEXT,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );

class university(BaseModel):
    """
    Mô hình dữ liệu cho bảng universities
    """
    id: int = Field(..., title="ID của trường đại học")
    name: str = Field(..., title="Tên trường đại học")
    created_at: datetime = Field(..., title="Thời gian tạo")

class university_section(BaseModel):
    """
    Mô hình dữ liệu cho bảng university_sections
    """
    id: int = Field(..., title="ID của section")
    university_id: int = Field(..., title="ID của trường đại học")
    section_title: str = Field(..., title="Tiêu đề của section")
    content: str = Field(..., title="Nội dung của section")
    created_at: datetime = Field(..., title="Thời gian tạo")

