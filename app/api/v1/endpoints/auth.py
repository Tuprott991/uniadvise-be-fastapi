from fastapi import APIRouter, HTTPException
from services.auth import register_user, login_user, get_current_user
from models.auth_model import RegisterRequest, LoginRequest, Token

router = APIRouter()

@router.post("/register")
def register(user: RegisterRequest):
    user_id = register_user(user)
    if not user_id:
        raise HTTPException(status_code=400, detail="Registration failed")
    return user_id

@router.post("/login")
def login(user: LoginRequest):
    user_id = login_user(user)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user_id

@router.get("/current_user")
def get_user(token: str):
    user = get_current_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user