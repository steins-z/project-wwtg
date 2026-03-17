"""Tests for chat, plan, and auth endpoints."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# --- Chat ---

def test_chat_message_returns_json() -> None:
    """POST /api/v1/chat/message returns JSON with session_id."""
    response = client.post(
        "/api/v1/chat/message",
        json={"message": "苏州，和老公，周末去哪玩"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert "reply" in data


def test_chat_message_with_session_id() -> None:
    """Session ID passed through in response."""
    response = client.post(
        "/api/v1/chat/message",
        json={"message": "hello", "session_id": "test-sid-001"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == "test-sid-001"


def test_chat_generates_plans_with_city() -> None:
    """When city is provided, plans should be generated."""
    response = client.post(
        "/api/v1/chat/message",
        json={"message": "苏州"},
    )
    data = response.json()
    assert "plans" in data
    assert len(data["plans"]) > 0
    assert "actions" in data


def test_chat_asks_for_city_without_one() -> None:
    """Without city, should ask follow-up."""
    response = client.post(
        "/api/v1/chat/message",
        json={"message": "你好"},
    )
    data = response.json()
    assert "reply" in data
    # Should not have plans
    assert "plans" not in data or len(data.get("plans", [])) == 0


# --- Plan ---

def test_plan_select() -> None:
    response = client.post(
        "/api/v1/plan/select",
        json={"plan_id": "mock-plan-a-001"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["plan_id"] == "mock-plan-a-001"


def test_plan_reject() -> None:
    response = client.post(
        "/api/v1/plan/reject",
        json={"plan_id": "mock-plan-a-001"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_plan_detail_fallback() -> None:
    """Unknown plan_id should return fallback detail."""
    response = client.get("/api/v1/plan/detail/unknown-plan")
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "stops" in data
    assert len(data["stops"]) > 0


# --- Auth ---

def test_wx_login_stub() -> None:
    response = client.post(
        "/api/v1/auth/wx-login",
        json={"code": "mock_code"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert "openid" in data
