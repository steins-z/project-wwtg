"""Tests for chat, plan, and auth endpoints."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# --- Chat ---

def test_chat_message_returns_sse_stream() -> None:
    """POST /api/v1/chat/message returns SSE with plan cards."""
    response = client.post(
        "/api/v1/chat/message",
        json={"message": "苏州，和老公，周末去哪玩"},
    )
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
    body = response.text
    assert "event: thinking" in body
    assert "event: done" in body


def test_chat_message_with_session_id() -> None:
    """Session ID passed through in header."""
    response = client.post(
        "/api/v1/chat/message",
        json={"message": "hello", "session_id": "test-sid-001"},
    )
    assert response.status_code == 200
    assert response.headers.get("x-session-id") == "test-sid-001"


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


def test_plan_detail() -> None:
    response = client.get("/api/v1/plan/detail/mock-plan-a-001")
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "stops" in data
    assert "tips" in data
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
