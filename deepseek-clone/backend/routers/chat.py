from fastapi import APIRouter

from ..models.chat import ChatCompletionRequest, ChatCompletionResponse
from ..services.chat_service import ChatService

router = APIRouter(prefix="/api/chat", tags=["chat"])
service = ChatService()


@router.post('/completions', response_model=ChatCompletionResponse)
async def create_completion(payload: ChatCompletionRequest) -> ChatCompletionResponse:
    """Create a mock streaming-aware chat completion."""
    return await service.generate_completion(payload)
