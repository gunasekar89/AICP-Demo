from __future__ import annotations

from datetime import datetime
from typing import List

from ..models.chat import ChatCompletionMessage, ChatCompletionRequest, ChatCompletionResponse


class ChatService:
    """In-memory chat completion service with deterministic responses."""

    async def generate_completion(self, payload: ChatCompletionRequest) -> ChatCompletionResponse:
        last_message = payload.messages[-1] if payload.messages else None
        content = self._build_response(last_message.content if last_message else "")
        return ChatCompletionResponse(
            id=f"mock-{datetime.utcnow().timestamp()}",
            created=int(datetime.utcnow().timestamp()),
            model=payload.model,
            choices=[ChatCompletionMessage(role="assistant", content=content)],
        )

    def _build_response(self, prompt: str) -> str:
        segments = [
            "### DeepSeek Response",
            "- Insightful reasoning anchored in verifiable knowledge.",
            "- Actionable next steps with clear prioritisation.",
            "- References to uploaded artefacts for additional context.",
        ]
        if prompt:
            segments.append(f"\n> Echoing your prompt: {prompt[:200]}")
        return "\n".join(segments)
