from pydantic import BaseModel
from typing import Optional

class RegisterRequest(BaseModel):
    email: str
    password: str
    fullname: Optional[str] = None
    gender: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class User(BaseModel):
    email: str
    fullname: str
    nickname: str
    list_message: Optional[list] = None
    #    threads TEXT[],
    threads: Optional[list] = None 

