from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel, Field

from app.text.service import TextService


class ChatRequest(BaseModel):
    session_id: str = Field(default="default", min_length=1, max_length=128)
    message: str = Field(min_length=1, max_length=20000)


class ChatResponse(BaseModel):
    session_id: str
    response: str


@dataclass(slots=True)
class TextAPI:
    service: TextService

    def router(self):
        try:
            from fastapi import APIRouter
        except ImportError as exc:
            raise RuntimeError("FastAPI is required for the HTTP text interface.") from exc

        router = APIRouter(prefix="/api/text", tags=["text"])

        @router.post("/chat", response_model=ChatResponse)
        async def chat(request: ChatRequest) -> ChatResponse:
            response = await self.service.chat(request.session_id, request.message)
            return ChatResponse(session_id=request.session_id, response=response)

        @router.delete("/sessions/{session_id}")
        async def clear_session(session_id: str) -> dict[str, str]:
            self.service.sessions.clear(session_id)
            return {"status": "cleared", "session_id": session_id}

        return router
