from fastapi import APIRouter
from pydantic import BaseModel
from services.advise_services import recommend_career, generate_learning_path

router = APIRouter()

class ProfileRequest(BaseModel):
    user_profile: str

class PathRequest(BaseModel):
    career: str
    university: str

@router.post("/recommend_career")
def recommend_career_endpoint(request: ProfileRequest):
    result = recommend_career(user_profile=request.user_profile)
    return {"career_suggestions": result}

@router.post("/learning_path")
def learning_path_endpoint(request: PathRequest):
    result = generate_learning_path(career=request.career, university=request.university)
    return {"learning_path": result}