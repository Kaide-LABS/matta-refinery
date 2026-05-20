"""Pydantic boundary schemas for enrichment_artifacts.

Boundary contract between adapters (Companies House / web scrape / Tavily)
and the persistence layer + downstream dossier composition. All schemas
use extra="forbid" per repo convention (29 → 33 boundaries with these 4).
"""
from datetime import datetime
from typing import Annotated, Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


EnrichmentSource = Literal["companies_house", "web_scrape", "tavily_news"]
EnrichmentStatus = Literal["fetched", "fallback_empty", "not_applicable", "failed"]


class EnrichmentArtifactRow(BaseModel):
    """Mirror of the enrichment_artifacts row, for API surfaces."""
    model_config = ConfigDict(extra="forbid")

    id: str
    prospect_id: Annotated[str, Field(min_length=1, max_length=64)]
    source: EnrichmentSource
    status: EnrichmentStatus
    payload: Optional[dict[str, Any]] = None
    fallback_reason: Optional[str] = None
    fetched_at: datetime


class CompaniesHousePayload(BaseModel):
    """UK Companies House profile data."""
    model_config = ConfigDict(extra="forbid")

    company_number: Annotated[str, Field(min_length=1, max_length=16)]
    company_name: Annotated[str, Field(min_length=1, max_length=256)]
    company_status: Annotated[str, Field(max_length=64)]
    date_of_creation: Optional[str] = None  # YYYY-MM-DD
    sic_codes: list[str] = []  # 5-digit SIC codes
    registered_office_address: Optional[dict[str, str]] = None
    jurisdiction: Optional[str] = None
    accounts_last_filed: Optional[str] = None  # YYYY-MM-DD


class WebScrapePayload(BaseModel):
    """Extracted facts from prospect website scrape."""
    model_config = ConfigDict(extra="forbid")

    url: Annotated[str, Field(max_length=2048)]
    title: Optional[Annotated[str, Field(max_length=512)]] = None
    meta_description: Optional[Annotated[str, Field(max_length=1024)]] = None
    extracted_capabilities: list[str] = []
    extracted_customers: list[str] = []
    extracted_certifications: list[str] = []  # ISO 9001, AS9100, IATF 16949, ...
    raw_text_sample: Annotated[str, Field(max_length=4096)] = ""
    scraped_at_iso: str


class TavilyNewsPayload(BaseModel):
    """News mentions retrieved from Tavily."""
    model_config = ConfigDict(extra="forbid")

    query: Annotated[str, Field(max_length=512)]
    # Tavily's per-result shape varies; keep loose dicts here.
    results: list[dict[str, Any]] = []
    results_count: int = 0
    summary: Optional[Annotated[str, Field(max_length=2048)]] = None  # Tavily auto-answer
    retrieved_at_iso: str
