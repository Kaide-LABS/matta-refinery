"""Playwright-based web scraper — handles JS-rendered prospect websites.

Fetches the prospect's primary website + extracts capabilities, customer
mentions, certifications, and a raw text sample for downstream LLM
consumption. Headless Chromium handles both static HTML and SPAs
(React, Vue, Angular) — BeautifulSoup-only would return empty for SPAs.
"""
import logging
import re
from datetime import datetime, timezone
from typing import Optional

from apps.refinery_api.config import settings
from packages.schemas.enrichment import WebScrapePayload

logger = logging.getLogger(__name__)


# ISO / industry certifications — extracted if mentioned anywhere on the page
ISO_CERTIFICATION_PATTERNS = [
    r"\bISO\s*9001\b",
    r"\bISO\s*14001\b",
    r"\bISO\s*45001\b",
    r"\bAS\s*9100\b",
    r"\bIATF\s*16949\b",
    r"\bNADCAP\b",
    r"\bAS\s*9120\b",
    r"\bISO\s*27001\b",
]

# Manufacturing capability vocabulary — substring-matched (case-insensitive)
CAPABILITY_KEYWORDS = [
    "investment casting", "sand casting", "die casting", "centrifugal casting",
    "open-die forging", "closed-die forging", "drop forging", "upset forging",
    "5-axis machining", "CNC machining", "EDM", "wire EDM",
    "laser cutting", "waterjet cutting", "plasma cutting",
    "sheet metal forming", "deep drawing", "stamping",
    "additive manufacturing", "laser powder bed fusion", "DED",
    "polymer extrusion", "injection moulding", "injection molding",
    "heat treatment", "HIP", "hot isostatic pressing",
    "surface treatment", "anodizing", "plating",
    "welding", "TIG welding", "MIG welding", "robotic welding",
    "non-destructive testing", "NDT", "X-ray inspection",
    "metrology", "CMM inspection",
]

# Customer / OEM vocabulary
CUSTOMER_INDUSTRY_PATTERNS = [
    r"\b(Rolls-Royce|Rolls Royce)\b",
    r"\b(Airbus)\b",
    r"\b(Boeing)\b",
    r"\b(BAE Systems?)\b",
    r"\b(Babcock)\b",
    r"\b(Lockheed Martin)\b",
    r"\b(Cummins)\b",
    r"\b(Caterpillar)\b",
    r"\b(Tata|Tata Steel)\b",
    r"\b(Jaguar Land Rover|JLR)\b",
    r"\b(Mercedes|Mercedes-Benz|Daimler)\b",
    r"\b(BMW)\b",
    r"\b(Volkswagen|VW)\b",
    r"\b(Ford)\b",
    r"\b(General Motors|GM)\b",
    r"\b(Bowers\s*&?\s*Wilkins)\b",
]


def derive_url_from_email(email: str) -> Optional[str]:
    """Best-effort URL derivation from email TLD."""
    if not email or "@" not in email:
        return None
    try:
        domain = email.split("@", 1)[1].strip().lower()
    except (ValueError, IndexError):
        return None
    if domain in ("example.com", "demo.invalid", "synthetic.test", ""):
        return None
    return f"https://{domain}"


def derive_url_from_company_name(company_name: str) -> Optional[str]:
    """Last-resort URL guess by snake-casing the company name."""
    if not company_name:
        return None
    slug = re.sub(r"[^a-z0-9]+", "-", company_name.lower()).strip("-")
    if not slug or "test" in slug or "mock" in slug or "synthetic" in slug:
        return None
    return f"https://{slug}.co.uk"  # Optimistic UK-default for the demo


class WebScraperAdapter:
    """Synchronous Playwright adapter — called from Celery task context."""

    def __init__(self):
        self.timeout_ms = settings.playwright_timeout_ms

    def extract_facts(self, text: str) -> tuple[list[str], list[str], list[str]]:
        """Returns (capabilities, customers, certifications) — deduped, order-preserved."""
        text_lower = text.lower()

        capabilities = [cap for cap in CAPABILITY_KEYWORDS if cap.lower() in text_lower]

        def _dedupe(items: list[str]) -> list[str]:
            seen: set[str] = set()
            out: list[str] = []
            for item in items:
                key = item.lower()
                if key not in seen:
                    seen.add(key)
                    out.append(item)
            return out

        customers: list[str] = []
        for pattern in CUSTOMER_INDUSTRY_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                customers.append(match.group(0))
        customers = _dedupe(customers)

        certifications: list[str] = []
        for pattern in ISO_CERTIFICATION_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                certifications.append(match.group(0).strip())
        certifications = _dedupe(certifications)

        return capabilities, customers, certifications

    def fetch(
        self,
        prospect_id: str,
        company_name: str,
        contact_email: str = "",
        explicit_url: Optional[str] = None,
    ) -> tuple[str, Optional[WebScrapePayload], Optional[str]]:
        """Returns (status, payload, fallback_reason)."""

        url = (
            explicit_url
            or derive_url_from_email(contact_email)
            or derive_url_from_company_name(company_name)
        )
        if not url:
            return ("fallback_empty", None, "no_derivable_url")

        # Lazy import so module-level imports work even when playwright is
        # not yet installed (e.g. dev IDE introspection of the codebase).
        try:
            from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
        except ImportError:
            return ("failed", None, "playwright_not_installed")

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    user_agent=(
                        "Mozilla/5.0 (compatible; Kaide-Labs-Refinery/1.0; "
                        "+https://kaide-labs.com)"
                    ),
                    viewport={"width": 1280, "height": 800},
                )
                page = context.new_page()

                try:
                    page.goto(url, timeout=self.timeout_ms, wait_until="domcontentloaded")
                except PlaywrightTimeout:
                    browser.close()
                    return ("fallback_empty", None, "page_load_timeout")
                except Exception as e:
                    browser.close()
                    return ("failed", None, f"navigation_failed_{type(e).__name__}")

                # SPAs often never reach networkidle; extract what we have on timeout.
                try:
                    page.wait_for_load_state("networkidle", timeout=3000)
                except PlaywrightTimeout:
                    pass

                title = page.title() or ""

                meta_desc = ""
                try:
                    meta_desc_elem = page.query_selector('meta[name="description"]')
                    if meta_desc_elem:
                        meta_desc = meta_desc_elem.get_attribute("content") or ""
                except Exception:
                    pass

                try:
                    body_text = page.inner_text("body") or ""
                except Exception:
                    body_text = ""

                browser.close()

                if len(body_text) < 200:
                    return ("fallback_empty", None, "body_text_too_short")

                capabilities, customers, certifications = self.extract_facts(body_text)

                payload = WebScrapePayload(
                    url=url,
                    title=title[:512] if title else None,
                    meta_description=meta_desc[:1024] if meta_desc else None,
                    extracted_capabilities=capabilities[:20],
                    extracted_customers=customers[:15],
                    extracted_certifications=certifications[:10],
                    raw_text_sample=body_text[:4096],
                    scraped_at_iso=datetime.now(timezone.utc).isoformat(),
                )
                return ("fetched", payload, None)

        except Exception as e:
            logger.exception(
                "Playwright scrape failed",
                extra={"prospect_id": prospect_id, "url": url},
            )
            return ("failed", None, f"playwright_exception_{type(e).__name__}")
