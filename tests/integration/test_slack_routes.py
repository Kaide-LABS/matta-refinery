"""Integration test: unsigned POSTs to slack routes must be rejected with 401.

The original Phase 1.7 bug: signature.verify() returned False on failure
instead of raising. The router wrapped the call in try/except, discarding
the return value, so unsigned requests passed through. This test pins the
fix.
"""
from fastapi.testclient import TestClient


def _client():
    # Imported lazily so conftest env vars are set before app import.
    from apps.refinery_api.main import app
    return TestClient(app)


def test_unsigned_slack_interactions_returns_401():
    client = _client()
    resp = client.post(
        "/slack/interactions",
        data={"payload": '{"action_id":"test"}'},
    )
    assert resp.status_code == 401, resp.text
    assert "signature" in resp.text.lower()


def test_unsigned_slack_events_returns_401():
    client = _client()
    resp = client.post(
        "/slack/events",
        json={"type": "url_verification", "challenge": "x"},
    )
    assert resp.status_code == 401, resp.text
    assert "signature" in resp.text.lower()
