"""Companies House Public Data API adapter — UK-jurisdiction only.

Fetches structured company facts for UK prospects. Returns
not_applicable status for non-UK prospects (no jurisdiction matching).

API docs: https://developer.company-information.service.gov.uk/
Auth: HTTP Basic with API key as username, empty password.
Rate limit: 600 requests per 5 minutes per API key.
"""
import logging
from typing import Optional

import requests
from requests.auth import HTTPBasicAuth

from apps.refinery_api.config import settings
from packages.schemas.enrichment import CompaniesHousePayload

logger = logging.getLogger(__name__)

COMPANIES_HOUSE_BASE_URL = "https://api.company-information.service.gov.uk"
REQUEST_TIMEOUT_SEC = 8.0

# UK-jurisdiction heuristic — avoid wasted API calls on non-UK prospects.
UK_JURISDICTION_HINTS = {".co.uk", ".uk", " ltd", " limited", " plc"}


class CompaniesHouseAdapter:
    """Synchronous adapter — called from Celery task context."""

    def __init__(self):
        self.api_key = settings.companies_house_api_key

    def is_uk_prospect(self, company_name: str, contact_email: str, raw_notes: str) -> bool:
        """Heuristic UK-jurisdiction detection — no API call needed."""
        signals = " " + " ".join([
            (company_name or "").lower(),
            (contact_email or "").lower(),
            (raw_notes or "").lower(),
        ])
        return any(hint in signals for hint in UK_JURISDICTION_HINTS)

    def fetch(
        self,
        prospect_id: str,
        company_name: str,
        contact_email: str = "",
        raw_notes: str = "",
    ) -> tuple[str, Optional[CompaniesHousePayload], Optional[str]]:
        """Returns (status, payload, fallback_reason).

        status in {'fetched', 'not_applicable', 'fallback_empty', 'failed'}.
        payload is a CompaniesHousePayload only when status == 'fetched'.
        """
        if not self.api_key:
            return ("failed", None, "no_api_key_configured")

        if not self.is_uk_prospect(company_name, contact_email, raw_notes):
            return ("not_applicable", None, "non_uk_jurisdiction_heuristic")

        # Step 1: search by name
        try:
            search_response = requests.get(
                f"{COMPANIES_HOUSE_BASE_URL}/search/companies",
                params={"q": company_name, "items_per_page": 5},
                auth=HTTPBasicAuth(self.api_key, ""),
                timeout=REQUEST_TIMEOUT_SEC,
            )
        except requests.RequestException as e:
            logger.exception(
                "Companies House search exception",
                extra={"prospect_id": prospect_id},
            )
            return ("failed", None, f"search_exception_{type(e).__name__}")

        if search_response.status_code == 429:
            return ("failed", None, "rate_limited")
        if search_response.status_code != 200:
            return ("failed", None, f"search_http_{search_response.status_code}")

        items = search_response.json().get("items", [])
        if not items:
            return ("fallback_empty", None, "no_search_results")

        top_match = items[0]
        company_number = top_match.get("company_number")
        if not company_number:
            return ("fallback_empty", None, "no_company_number_in_result")

        # Step 2: fetch full profile
        try:
            profile_response = requests.get(
                f"{COMPANIES_HOUSE_BASE_URL}/company/{company_number}",
                auth=HTTPBasicAuth(self.api_key, ""),
                timeout=REQUEST_TIMEOUT_SEC,
            )
        except requests.RequestException as e:
            logger.exception(
                "Companies House profile exception",
                extra={"prospect_id": prospect_id, "company_number": company_number},
            )
            return ("failed", None, f"profile_exception_{type(e).__name__}")

        if profile_response.status_code != 200:
            return ("failed", None, f"profile_http_{profile_response.status_code}")

        profile = profile_response.json()
        accounts = profile.get("accounts") or {}
        last_accounts = accounts.get("last_accounts") or {}

        payload = CompaniesHousePayload(
            company_number=profile.get("company_number", company_number),
            company_name=profile.get("company_name", company_name),
            company_status=profile.get("company_status", "unknown"),
            date_of_creation=profile.get("date_of_creation"),
            sic_codes=profile.get("sic_codes", []),
            registered_office_address=profile.get("registered_office_address"),
            jurisdiction=profile.get("jurisdiction"),
            accounts_last_filed=last_accounts.get("made_up_to"),
        )
        return ("fetched", payload, None)
