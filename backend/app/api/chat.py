"""Chat endpoints: message (SSE) and history."""

import json
import uuid
from typing import AsyncGenerator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.schemas import ChatMessageRequest, ChatMessageResponse
from app.services.chat_service import ChatService

router = APIRouter()
chat_service = ChatService()


async def _sse_stream(session_id: str, message: str) -> AsyncGenerator[str, None]:
    """Generate SSE events for a chat message."""
    # Status: parsing intent
    yield f"event: thinking\ndata: {json.dumps({'status': 'parsing_intent', 'session_id': session_id})}\n\n"

    # Process through chat service
    response = await chat_service.process_message(session_id, message)

    # If plans were generated, stream them
    if response.plans:
        yield f"event: thinking\ndata: {json.dumps({'status': 'querying_weather', 'session_id': session_id})}\n\n"
        yield f"event: thinking\ndata: {json.dumps({'status': 'generating_plans', 'session_id': session_id})}\n\n"

        # Reply text
        yield f"event: message\ndata: {json.dumps({'content': response.reply, 'session_id': session_id}, ensure_ascii=False)}\n\n"

        # Plan cards
        for plan in response.plans:
            yield f"event: plan_card\ndata: {json.dumps({**plan.model_dump(), 'session_id': session_id}, ensure_ascii=False)}\n\n"

        yield f"event: actions\ndata: {json.dumps({'options': ['select_a', 'select_b', 'reject'], 'session_id': session_id})}\n\n"
    else:
        # Text-only response
        yield f"event: message\ndata: {json.dumps({'content': response.reply, 'session_id': session_id}, ensure_ascii=False)}\n\n"

    yield f"event: done\ndata: {json.dumps({'session_id': session_id})}\n\n"


@router.post("/message")
async def send_message(req: ChatMessageRequest) -> StreamingResponse:
    """Send a chat message, receive SSE streaming response."""
    session_id = req.session_id or str(uuid.uuid4())
    return StreamingResponse(
        _sse_stream(session_id, req.message),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Session-Id": session_id},
    )


@router.get("/history/{session_id}")
async def get_history(session_id: str) -> list[ChatMessageResponse]:
    """Get chat history for a session (stub)."""
    return []
