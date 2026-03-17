"""Chat service: conversation state machine with LLM integration."""

import asyncio
import logging
from typing import Any

from app.config import settings
from app.models.schemas import (
    ChatResponse,
    ConversationState,
    PlanCard,
    UserContext,
)
from app.services.data_service import DataService
from app.services.llm_service import LLMService
from app.services.map_service import MapService
from app.services.plan_service import PlanService
from app.services.weather_service import WeatherService

logger = logging.getLogger(__name__)


class ChatService:
    """Manages conversation flow and state transitions."""

    def __init__(self) -> None:
        self.llm = LLMService(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
            model=settings.llm_model,
        )
        self.weather = WeatherService(api_key=settings.amap_api_key)
        self.map = MapService(api_key=settings.amap_api_key)
        self.plan_service = PlanService(llm=self.llm, map_service=self.map)
        self.data = DataService()

        # In-memory session store (MVP — Redis later)
        self._sessions: dict[str, dict[str, Any]] = {}

    def _get_session(self, session_id: str) -> dict[str, Any]:
        if session_id not in self._sessions:
            self._sessions[session_id] = {
                "state": ConversationState.INIT,
                "context": UserContext(),
                "history": [],  # list of {"role": str, "content": str}
                "rejected_plans": [],
                "current_plans": [],
            }
        return self._sessions[session_id]

    async def process_message(self, session_id: str, message: str) -> ChatResponse:
        """Process a user message through the full conversation flow."""
        session = self._get_session(session_id)
        state = session["state"]
        ctx: UserContext = session["context"]
        history: list[dict[str, str]] = session["history"]

        # Add user message to history
        history.append({"role": "user", "content": message})

        # --- Handle rejection / selection from PRESENTING state ---
        if state == ConversationState.PRESENTING:
            lower_msg = message.strip().lower()
            if "换" in message or "不喜欢" in message or "reject" in lower_msg:
                # Track rejected plan titles
                for plan in session.get("current_plans", []):
                    if isinstance(plan, PlanCard):
                        session["rejected_plans"].append(plan.title)
                    elif isinstance(plan, dict):
                        session["rejected_plans"].append(plan.get("title", ""))
                session["state"] = ConversationState.GENERATING
                # Re-generate
                return await self._generate_and_present(session, ctx)

            if "选" in message or "select" in lower_msg:
                # Plan selected — acknowledge
                reply = "好的，方案已选择！祝你周末愉快 🎉"
                session["state"] = ConversationState.IDLE
                history.append({"role": "assistant", "content": reply})
                return ChatResponse(reply=reply, state=ConversationState.IDLE)

            # Any other message → treat as new input, restart collecting
            session["state"] = ConversationState.COLLECTING

        # --- Parse intent via LLM ---
        parsed = await self.llm.parse_intent(message, history)

        # Merge parsed fields into context
        if parsed.get("city"):
            ctx.city = parsed["city"]
        if parsed.get("people_count"):
            ctx.people_count = parsed["people_count"]
        if parsed.get("companion_type"):
            ctx.companion_type = parsed["companion_type"]
        if parsed.get("energy_level"):
            ctx.energy_level = parsed["energy_level"]
        if parsed.get("constraints"):
            for c in parsed["constraints"]:
                if c not in ctx.constraints:
                    ctx.constraints.append(c)
        if parsed.get("preferences"):
            for p in parsed["preferences"]:
                if p not in ctx.preferences:
                    ctx.preferences.append(p)

        # --- Check if we have enough context ---
        if not ctx.city:
            session["state"] = ConversationState.COLLECTING
            reply = "你好！我是周末搭子 🎉 告诉我你想在哪个城市玩？和谁一起？有什么特殊需求吗？"
            history.append({"role": "assistant", "content": reply})
            return ChatResponse(reply=reply, state=ConversationState.COLLECTING)

        # --- Enough context → generate plans ---
        session["state"] = ConversationState.GENERATING
        return await self._generate_and_present(session, ctx)

    async def _generate_and_present(
        self, session: dict[str, Any], ctx: UserContext
    ) -> ChatResponse:
        """Parallel-fetch weather + POIs, then generate plans."""
        history: list[dict[str, str]] = session["history"]

        # Parallel fetch: weather + POIs (15-second timeline from tech design)
        weather_task = asyncio.create_task(self.weather.get_weather(ctx.city or "苏州"))
        pois_task = asyncio.create_task(
            self.data.get_pois(ctx.city or "苏州", ctx.preferences)
        )

        weather_data, pois_data = await asyncio.gather(weather_task, pois_task)

        # Build context dict for plan generation
        context_dict = ctx.model_dump()

        # Generate plans
        plans = await self.plan_service.generate_plans(
            context=context_dict,
            weather=weather_data,
            pois=pois_data,
            rejected_plans=session.get("rejected_plans"),
        )

        session["state"] = ConversationState.PRESENTING
        session["current_plans"] = plans

        reply = "为您找到以下方案："
        history.append({"role": "assistant", "content": reply})

        return ChatResponse(
            reply=reply,
            plans=plans,
            state=ConversationState.PRESENTING,
        )
