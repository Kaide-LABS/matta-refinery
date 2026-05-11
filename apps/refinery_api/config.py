from typing import Literal
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

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
