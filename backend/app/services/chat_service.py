"""Chat service: conversation state machine and intent parsing."""

from app.models.schemas import (
    ChatResponse,
    ConversationState,
    UserContext,
)
from app.services.plan_service import PlanService


class ChatService:
    """Manages conversation flow and state transitions."""

    def __init__(self) -> None:
        self.plan_service = PlanService()
        # In-memory session store (W1 mock — will use Redis in W2)
        self._sessions: dict[str, dict] = {}

    def _get_session(self, session_id: str) -> dict:
        if session_id not in self._sessions:
            self._sessions[session_id] = {
                "state": ConversationState.INIT,
                "context": UserContext(),
                "history": [],
            }
        return self._sessions[session_id]

    async def process_message(self, session_id: str, message: str) -> ChatResponse:
        """Process a user message and return response with optional plans."""
        session = self._get_session(session_id)
        state = session["state"]
        ctx = session["context"]

        # Simple intent parsing (W1 mock — will use LLM in W2)
        parsed = self._parse_intent(message)

        if parsed.get("city"):
            ctx.city = parsed["city"]
        if parsed.get("companion_type"):
            ctx.companion_type = parsed["companion_type"]
        if parsed.get("constraints"):
            ctx.constraints.extend(parsed["constraints"])
        if parsed.get("preferences"):
            ctx.preferences.extend(parsed["preferences"])

        # State machine logic
        if state in (ConversationState.INIT, ConversationState.COLLECTING):
            if ctx.city:
                # Enough info to generate — produce mock plans
                session["state"] = ConversationState.PRESENTING
                plans = self.plan_service.generate_mock_plans(ctx)
                return ChatResponse(
                    reply="为您找到以下方案：",
                    plans=plans,
                    state=ConversationState.PRESENTING,
                )
            else:
                session["state"] = ConversationState.COLLECTING
                return ChatResponse(
                    reply="你好！我是周末搭子 🎉 告诉我你想在哪个城市玩？和谁一起？有什么特殊需求吗？",
                    state=ConversationState.COLLECTING,
                )

        elif state == ConversationState.PRESENTING:
            # User said something after seeing plans — treat as rejection or new request
            session["state"] = ConversationState.COLLECTING
            return ChatResponse(
                reply="好的，让我重新为您推荐。有什么新的要求吗？",
                state=ConversationState.COLLECTING,
            )

        # Default fallback
        return ChatResponse(
            reply="我是周末搭子，帮你规划周末出行！告诉我城市和你的需求吧 😊",
            state=ConversationState.IDLE,
        )

    def _parse_intent(self, message: str) -> dict:
        """Mock intent parsing — keyword extraction (W1 stub, LLM in W2)."""
        result: dict = {}

        # City detection (simple keyword match)
        cities = ["苏州", "上海", "杭州", "南京", "北京", "广州", "深圳", "成都"]
        for city in cities:
            if city in message:
                result["city"] = city
                break

        # Companion detection
        if "老公" in message or "老婆" in message or "情侣" in message:
            result["companion_type"] = "情侣"
        elif "孩子" in message or "亲子" in message or "娃" in message:
            result["companion_type"] = "亲子"
        elif "朋友" in message:
            result["companion_type"] = "朋友"

        # Constraints
        constraints = []
        if "孕妇" in message:
            constraints.append("孕妇")
        if "轮椅" in message:
            constraints.append("轮椅")
        if constraints:
            result["constraints"] = constraints

        # Preferences
        preferences = []
        if "人少" in message:
            preferences.append("人少")
        if "免费" in message:
            preferences.append("免费")
        if preferences:
            result["preferences"] = preferences

        return result
