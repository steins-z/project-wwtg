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


def test_chat_message_includes_session_in_body() -> None:
    """SSE events include session_id in data."""
    response = client.post(
        "/api/v1/chat/message",
        json={"message": "苏州", "session_id": "test-sid-body"},
    )
    assert response.status_code == 200
    assert "test-sid-body" in response.text


def test_chat_sse_status_updates() -> None:
    """SSE should include parsing_intent status."""
    response = client.post(
        "/api/v1/chat/message",
        json={"message": "苏州，和老公"},
    )
    body = response.text
    assert "parsing_intent" in body


def test_chat_generates_plans_with_city() -> None:
    """When city is provided, plans should be generated."""
    response = client.post(
        "/api/v1/chat/message",
        json={"message": "苏州"},
    )
    body = response.text
    assert "event: plan_card" in body
    assert "event: actions" in body


def test_chat_asks_for_city_without_one() -> None:
    """Without city, should ask follow-up."""
    response = client.post(
        "/api/v1/chat/message",
        json={"message": "你好"},
    )
    body = response.text
    assert "event: message" in body
    # Should not have plan cards
    assert "event: plan_card" not in body


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
