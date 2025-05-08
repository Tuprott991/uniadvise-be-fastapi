# Xử lý chatbot với LangChain + FastAPI
 
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from services.chatbot_services import get_answer, get_answer_stream, format_chat_history
from database.chatbot_history import get_recent_chat_history, create_thread_id_for_user, get_thread_id_for_user
import logging
import json
from typing import AsyncGenerator, Dict

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    user_id: int
    question: str
    thread_id: str

class ChatResponse(BaseModel):
    answer: str

class ThreadRequest(BaseModel):
    user_id: str


@router.post("/chatt")
async def chat(request: ChatRequest):
    try:
        logger.info(f"Received question: {request.question} for thread: {request.thread_id}")
        result = get_answer(request.question, request.thread_id)
        logger.info(f"Got result: {result}")
        
        if not isinstance(result, dict) or "output" not in result:
            raise ValueError("Invalid response format from get_answer")
            
        return ChatResponse(answer=result["output"])
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )

async def event_generator(question: str, thread_id: str, user_id: int) -> AsyncGenerator[str, None]:
    try:
        async for chunk in get_answer_stream(question, thread_id, user_id):
            if chunk:  # Only yield if there's content
                yield f"data: {json.dumps({'content': chunk})}\n\n"
    except Exception as e:
        logger.error(f"Error in stream: {str(e)}", exc_info=True)
        yield f"data: {json.dumps({'error': str(e)})}\n\n"


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    return StreamingResponse(
        event_generator(user_id = request.user_id , question = request.question, thread_id=  request.thread_id),
        media_type="text/event-stream"
    ) 

@router.get("/chat/all_history/{user_id}")
def get_all_chat_threads_id(user_id: int):
    """
    Lấy danh sách các thread chat của người dùng
    """
    try:
        threads = get_thread_id_for_user(user_id) # Lấy danh sách các thread chat của người dùng từ database
        if not threads:
            raise HTTPException(status_code=404, detail="No chat threads found")
        return {"threads": threads}
    except Exception as e:
        logger.error(f"Error fetching chat threads: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/history/{thread_id}")
def get_chat_history(user_id: int, thread_id: str):
    """
    Lấy lịch sử chat gần đây của một cuộc trò chuyện
    """
    try:
        history = get_recent_chat_history(thread_id)
        if not history:
            raise HTTPException(status_code=404, detail="No chat history found")
        formatted_history = format_chat_history(history)  # Định dạng lịch sử chat thành chuỗi văn bản
        return {"history": formatted_history}
    except Exception as e:
        logger.error(f"Error fetching chat history: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/chat/create")
def create_chat_thread(request: ThreadRequest):
    """
    Tạo một thread chat mới cho người dùng
    """
    try:
        print(request.user_id)
        thread_id = create_thread_id_for_user(request.user_id)  # Tạo thread chat mới cho người dùng
        if not thread_id:
            raise HTTPException(status_code=500, detail="Failed to create chat thread")
        return {"thread_id": thread_id}
    except Exception as e:
        logger.error(f"Error creating chat thread: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    
