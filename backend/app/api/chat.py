"""Chat endpoints: message and history."""

import uuid

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.models.schemas import ChatMessageRequest, ChatMessageResponse
from app.services.chat_service import ChatService

router = APIRouter()
chat_service = ChatService()


@router.post("/message")
async def send_message(req: ChatMessageRequest) -> JSONResponse:
    """Send a chat message, receive JSON response.

    MVP: synchronous JSON response (no streaming).
    TODO(M5): migrate to SSE with enableChunked on mini program side.
    """
    session_id = req.session_id or str(uuid.uuid4())

    response = await chat_service.process_message(session_id, req.message)

    result: dict = {
        "session_id": session_id,
        "reply": response.reply,
    }

    if response.plans:
        result["plans"] = [p.model_dump() for p in response.plans]
        result["actions"] = ["select_a", "select_b", "reject"]

    return JSONResponse(content=result)


@router.get("/history/{session_id}")
async def get_history(session_id: str) -> list[ChatMessageResponse]:
    """Get chat history for a session (stub)."""
    return []
