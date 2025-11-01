from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class ChatCompletionMessage(BaseModel):
    role: str = Field(..., description="Role of the message author")
    content: str = Field(..., description="Message content")


class ChatCompletionRequest(BaseModel):
    model: str = Field(default="gpt-4-turbo")
    temperature: float = Field(default=0.7, ge=0, le=2)
    messages: List[ChatCompletionMessage] = Field(default_factory=list)


class ChatCompletionResponse(BaseModel):
    id: str
    created: int
    model: str
    choices: List[ChatCompletionMessage]
