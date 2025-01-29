from typing import Dict, Optional
from datetime import datetime
import uuid
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from app.models.chat import ChatRequest, ChatResponse
from app.core.config import settings

class ChatService:
    def __init__(self):
        self.chat_model = ChatOpenAI(
            temperature=0.7,
            model_name=settings.MODEL_NAME,
            max_tokens=settings.MAX_TOKENS,
            api_key=settings.OPENAI_API_KEY
        )
        # In a real application, you'd want to use a proper database
        self.conversations = {}

    async def process_message(self, request: ChatRequest) -> ChatResponse:
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        messages = []
        if request.system_instruction:
            messages.append(SystemMessage(content=request.system_instruction))
        messages.append(HumanMessage(content=request.message))

        response = await self.chat_model.ainvoke(messages)
        
        # Store conversation in memory (replace with database in production)
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        
        self.conversations[conversation_id].append({
            "message": request.message,
            "response": response.content,
            "timestamp": datetime.utcnow()
        })

        return ChatResponse(
            response=response.content,
            conversation_id=conversation_id,
            created_at=datetime.utcnow(),
            token_usage={"total_tokens": response.additional_kwargs.get("token_usage", {}).get("total_tokens", 0)}
        )

    async def get_conversation_history(self, conversation_id: str) -> Dict:
        if conversation_id not in self.conversations:
            raise ValueError(f"Conversation {conversation_id} not found")
        return self.conversations[conversation_id] 