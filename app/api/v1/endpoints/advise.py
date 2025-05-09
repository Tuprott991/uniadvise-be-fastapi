from fastapi import APIRouter, HTTPException
from services.advise_services import load_recommender_agent, load_learning_path_agent
from pydantic import BaseModel

router = APIRouter()

recommender = load_recommender_agent()
path_planner = load_learning_path_agent()

class ProfileRequest(BaseModel):
    user_profile: str

class PathRequest(BaseModel):
    career: str
    university: str

@router.post("/recommend_career")
def recommend_career(request: ProfileRequest):
    result = recommender.run(user_profile=request.user_profile)
    return {"career_suggestions": result}

@router.post("/learning_path")
def learning_path(request: PathRequest):
    result = path_planner.run(
        career=request.career,
        university=request.university
    )
    return {"learning_path": result}