from fastapi import APIRouter, HTTPException
from models.auth_model import RegisterRequest, LoginRequest, Token
from services.uni_info_services import all_universities_json, format_university_sections

router = APIRouter()

@router.get("/universities", response_model=list[dict]) 
def get_universities():
    """
    Lấy tên và id trường đại học từ database.
    """
    try:
        universities = all_universities_json()
        return universities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/universities/{university_id}",response_model=list[dict]) 
def get_university_info(university_id: int):
    print("ID trường đại học:", university_id)
    """
    Lấy thông tin chi tiết của trường đại học theo id.
    """
    try:
        university_info = format_university_sections(university_id)
        if not university_info:
            raise HTTPException(status_code=404, detail="University not found")
        return university_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    