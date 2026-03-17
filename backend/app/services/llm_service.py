"""LLM client abstraction (W1 mock)."""

from typing import Any


class LLMService:
    """LLM client for intent parsing and plan generation.
    
    W1: Returns hardcoded responses.
    W2: Will integrate DeepSeek V3 / Qwen-Max API with streaming.
    """

    async def parse_intent(self, message: str) -> dict[str, Any]:
        """Parse user intent from a message. Returns structured fields."""
        # W1 mock — actual parsing is in chat_service._parse_intent
        return {"raw": message}

    async def generate_plan(self, prompt: str) -> str:
        """Generate a plan from a prompt. Returns JSON string."""
        # W1 mock
        return '{"title": "mock plan", "stops": []}'

    async def generate_plan_stream(self, prompt: str):
        """Stream plan generation tokens. Yields chunks."""
        # W1 mock
        yield '{"title": "mock plan"}'
