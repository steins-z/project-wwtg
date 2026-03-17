"""Pydantic models for API request/response and domain objects."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# --- Conversation State ---

class ConversationState(str, Enum):
    INIT = "init"
    COLLECTING = "collecting"
    GENERATING = "generating"
    PRESENTING = "presenting"
    DETAIL = "detail"
    REJECTING = "rejecting"
    IDLE = "idle"


# --- User Context ---

class UserContext(BaseModel):
    """Collected user preferences for plan generation."""
    city: Optional[str] = None
    people_count: int = 2
    companion_type: Optional[str] = None  # 独自/情侣/亲子/朋友
    energy_level: str = "medium"  # high/medium/low
    constraints: list[str] = Field(default_factory=list)
    preferences: list[str] = Field(default_factory=list)
    rejection_reasons: list[str] = Field(default_factory=list)


# --- Chat ---

class ChatMessageRequest(BaseModel):
    session_id: Optional[str] = None
    message: str
    wx_user_id: Optional[str] = None


class ChatMessageResponse(BaseModel):
    role: str  # user / assistant
    content: str
    metadata: Optional[dict] = None


# --- Plan Card (summary shown in chat) ---

class PlanCard(BaseModel):
    plan_id: str
    title: str
    emoji: str
    description: str
    duration: str
    cost_range: str
    transport: str
    tags: list[str]
    stops_count: int
    source_count: int


# --- Plan Detail ---

class PlanStop(BaseModel):
    name: str
    arrive_at: str
    stay_duration: str
    recommendation: str
    nav_link: str = ""
    walk_to_next: str = ""


class PlanSource(BaseModel):
    title: str
    likes: int = 0
    url: str = ""


class PlanDetail(BaseModel):
    plan_id: str
    title: str
    stops: list[PlanStop]
    tips: list[str]
    sources: list[PlanSource]


# --- Chat Service Response (internal) ---

class ChatResponse(BaseModel):
    reply: str = ""
    plans: list[PlanCard] = Field(default_factory=list)
    state: ConversationState = ConversationState.INIT


class PlanSelectRequest(BaseModel):
    plan_id: str
    session_id: Optional[str] = None
