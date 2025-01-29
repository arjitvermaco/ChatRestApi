from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    system_instruction: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    created_at: datetime
    token_usage: Dict[str, int]

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    status_code: int 