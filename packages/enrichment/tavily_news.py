"""Tavily news mentions adapter — replaces the LinkedIn signal stub.

Tavily is an AI-agent-optimized web search API. Queries for recent
news mentions of the prospect company surface capacity expansions,
contract wins, regulatory actions, M&A — the operational-state signal
that justifies sales engagement.

LinkedIn Sales Navigator integration deferred to Phase 2 (paid OAuth).

Docs: https://docs.tavily.com/sdk/python/reference
"""
import logging
from datetime import datetime, timezone
from typing import Optional

from apps.refinery_api.config import settings
from packages.schemas.enrichment import TavilyNewsPayload

logger = logging.getLogger(__name__)


class TavilyNewsAdapter:
    """Synchronous Tavily adapter — called from Celery task context."""

    def __init__(self):
        self.api_key = settings.tavily_api_key
        self._client = None
        if self.api_key:
            try:
                from tavily import TavilyClient
                self._client = TavilyClient(api_key=self.api_key)
            except ImportError:
                # tavily-python not installed; fetch() will return 'failed'.
                self._client = None

    def build_query(self, company_name: str) -> str:
        """Construct a high-signal news query for a manufacturing prospect.

        Targets operational-state signals: expansions, contracts,
        certifications, M&A, capacity changes.
        """
        return (
            f'"{company_name}" '
            f'(capacity expansion OR new contract OR acquisition OR investment OR '
            f'certification OR factory OR plant OR manufacturing)'
        )

    def fetch(
        self,
        prospect_id: str,
        company_name: str,
    ) -> tuple[str, Optional[TavilyNewsPayload], Optional[str]]:
        """Returns (status, payload, fallback_reason)."""
        if not self.api_key:
            return ("failed", None, "no_api_key_configured")
        if self._client is None:
            return ("failed", None, "tavily_sdk_not_installed")

        if not company_name or len(company_name) < 3:
            return ("fallback_empty", None, "company_name_too_short")

        query = self.build_query(company_name)

        try:
            response = self._client.search(
                query=query,
                search_depth="advanced",
                include_answer=True,
                max_results=8,
            )
        except Exception as e:
            logger.exception(
                "Tavily search exception",
                extra={"prospect_id": prospect_id, "query": query},
            )
            return ("failed", None, f"tavily_exception_{type(e).__name__}")

        # Tavily returns: { results: [...], answer: "...", query: "..." }
        results = response.get("results", []) if isinstance(response, dict) else []
        answer = response.get("answer", "") if isinstance(response, dict) else ""

        if not results:
            return ("fallback_empty", None, "no_search_results")

        trimmed_results = [
            {
                "title": (r.get("title") or "")[:256],
                "url": (r.get("url") or "")[:512],
                "snippet": (r.get("content") or "")[:512],
                "published_date": r.get("published_date"),
                "score": r.get("score"),
            }
            for r in results[:8]
        ]

        payload = TavilyNewsPayload(
            query=query[:512],
            results=trimmed_results,
            results_count=len(results),
            summary=answer[:2048] if answer else None,
            retrieved_at_iso=datetime.now(timezone.utc).isoformat(),
        )
        return ("fetched", payload, None)
