"""Plan endpoints: select, reject, detail."""

from fastapi import APIRouter

from app.models.schemas import PlanDetail, PlanSelectRequest
from app.services.chat_service import ChatService

router = APIRouter()

# Import the shared chat_service to access plan_service with stored plans
from app.api.chat import chat_service


@router.post("/select")
async def select_plan(req: PlanSelectRequest) -> dict[str, str]:
    """User selects a plan."""
    return {"status": "ok", "plan_id": req.plan_id, "message": "方案已选择"}


@router.post("/reject")
async def reject_plan(req: PlanSelectRequest) -> dict[str, str]:
    """User rejects current plans, requesting regeneration."""
    return {"status": "ok", "message": "已记录，将为您重新生成方案"}


@router.get("/detail/{plan_id}")
async def get_plan_detail(plan_id: str) -> PlanDetail:
    """Get full plan detail with stops, tips, sources."""
    return chat_service.plan_service.get_plan_detail(plan_id)
