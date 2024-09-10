import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import APIRouter, status
from fastapi import Response, Depends, HTTPException

from chatbot_service import ChatbotService, ChatRequest

#initilize the OpenAI chatbot api 
chatbot = ChatbotService()

# router object
router = APIRouter(
    prefix="/api/v1/chat",
    tags=['Chat'],
    responses={ 404: {"description" : "Not Found"}}
)


@router.post("/", )
async def chat(request: ChatRequest):
    try:
        response = await chatbot.get_response(request.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {e}")