from typing import Literal, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    postgres_url: str
    redis_url: str
    celery_broker: str
    gcp_project: str
    vertex_location: Literal["europe-west4"] = "europe-west4"
    slack_signing_secret: str
    crm_webhook_secret_hubspot: str
    crm_webhook_secret_salesforce: str
    mock_surfaces: bool = True
    kaide_labs_project_id: str

    # External enrichment APIs (Phase 1.7)
    companies_house_api_key: Optional[str] = None
    tavily_api_key: Optional[str] = None

    # Web scraping
    playwright_timeout_ms: int = 8000

    # Cloud Logging (auto-detected on Cloud Run via K_SERVICE env var;
    # gcp_logging_enabled is a local-dev override for forcing JSON output)
    gcp_logging_enabled: bool = False
    gcp_project_log_name: str = "matta-refinery"

    # Enrichment behavior toggles
    enrichment_use_cache: bool = True
    enrichment_cache_ttl_hours: int = 168  # 7 days

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
