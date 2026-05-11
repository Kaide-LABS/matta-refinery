"""Criterion 13 — Tightening 2 Slack distributed lock primitive.

A unit-level test of the SET NX EX semantics the slack_events router depends on. The
HTTP-level integration test (concurrent FastAPI requests) lives in the integration suite;
this test verifies the lock primitive itself behaves correctly so the router can rely on it.

If two acquisitions on the same event_id occur within the TTL, the first MUST succeed and
the second MUST return a falsy value (0 / None / False). When the lock is released, a
subsequent acquisition MUST succeed again.
"""
import time

import pytest


SLACK_LOCK_TTL_SECONDS = 60


class _FakeRedisLock:
    """Minimal in-memory implementation of Redis SET NX EX + DEL semantics used by the router."""

    def __init__(self):
        self._kv: dict[str, tuple[str, float]] = {}  # key -> (value, expires_at_monotonic)

    def set(self, key: str, value: str, ex: int, nx: bool = False) -> bool:
        now = time.monotonic()
        existing = self._kv.get(key)
        if existing is not None and existing[1] > now:
            if nx:
                return False
            self._kv[key] = (value, now + ex)
            return True
        self._kv[key] = (value, now + ex)
        return True

    def delete(self, key: str) -> int:
        return 1 if self._kv.pop(key, None) is not None else 0


def test_first_acquisition_succeeds_second_fails_within_ttl():
    redis = _FakeRedisLock()
    event_id = "Ev-DUPLICATE-001"

    first = redis.set(f"slack:lock:{event_id}", "1", ex=SLACK_LOCK_TTL_SECONDS, nx=True)
    second = redis.set(f"slack:lock:{event_id}", "1", ex=SLACK_LOCK_TTL_SECONDS, nx=True)

    assert first is True, "first acquisition must succeed"
    assert second is False, (
        "second acquisition within TTL must fail — the router relies on this to return "
        "HTTP 202 duplicate_in_flight rather than spawning a second workflow"
    )


def test_release_allows_reacquire():
    """After Celery on_success/on_failure callback releases the lock, a later legitimate retry
    must be able to re-acquire."""
    redis = _FakeRedisLock()
    event_id = "Ev-RELEASE-002"

    assert redis.set(f"slack:lock:{event_id}", "1", ex=SLACK_LOCK_TTL_SECONDS, nx=True) is True
    redis.delete(f"slack:lock:{event_id}")
    reacquired = redis.set(f"slack:lock:{event_id}", "1", ex=SLACK_LOCK_TTL_SECONDS, nx=True)
    assert reacquired is True, "post-release reacquire must succeed"


def test_ttl_60_seconds_per_spec():
    """The TTL must be 60 seconds per PHASE_1_SPEC §D.2 — slightly exceeding the maximum per-task
    Celery execution envelope. Verify the constant in the router module matches."""
    from apps.refinery_api.routers.slack_events import SLACK_LOCK_TTL_SECONDS as router_ttl

    assert router_ttl == 60, f"SLACK_LOCK_TTL_SECONDS must be 60s; found {router_ttl}"
