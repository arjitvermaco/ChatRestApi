from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from datetime import datetime
import uvicorn

from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.core.config import Settings
from app.core.dependencies import get_api_key

# Initialize FastAPI app
app = FastAPI(
    title="LangChain ChatBot API",
    description="A REST API for interacting with LangChain-powered chatbot",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    api_key: str = Depends(get_api_key),
    chat_service: ChatService = Depends()
):
    """
    Process a chat message and return AI-generated response
    """
    try:
        response = await chat_service.process_message(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    api_key: str = Depends(get_api_key),
    chat_service: ChatService = Depends()
):
    """
    Retrieve conversation history
    """
    try:
        history = await chat_service.get_conversation_history(conversation_id)
        return history
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 