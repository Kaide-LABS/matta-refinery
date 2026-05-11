"""Shared pytest fixtures. Provides required env vars for the Pydantic Settings load that
fires when any router / task / worker module is imported during test collection."""
import os


def pytest_configure(config):
    """Seed test-only env vars before any test module imports `apps.refinery_api.config`.
    These are inert placeholder values — Phase 1 demo settings, no real credentials."""
    os.environ.setdefault("POSTGRES_URL", "postgresql+asyncpg://test:test@localhost:5432/test")
    os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
    os.environ.setdefault("CELERY_BROKER", "redis://localhost:6379/1")
    os.environ.setdefault("GCP_PROJECT", "kaide-labs-phase1-test")
    os.environ.setdefault("VERTEX_LOCATION", "europe-west4")
    os.environ.setdefault("SLACK_SIGNING_SECRET", "mock-signing-secret-phase1")
    os.environ.setdefault("CRM_WEBHOOK_SECRET_HUBSPOT", "mock-hubspot-secret")
    os.environ.setdefault("CRM_WEBHOOK_SECRET_SALESFORCE", "mock-salesforce-secret")
    os.environ.setdefault("MOCK_SURFACES", "true")
    os.environ.setdefault("KAIDE_LABS_PROJECT_ID", "kaide-labs-phase1-test")
