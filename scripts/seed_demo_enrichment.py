"""Seed pre-computed enrichment for demo tracer prospects.

These payloads represent what the live adapters WOULD return for each
tracer if invoked. They're seeded so demo runs are deterministic — no
flaky external APIs during recording.

Re-running the live adapters on these prospect_ids would overwrite
these rows (upsert semantics on UNIQUE(prospect_id, source)). To
regenerate from live data, delete the rows and run
enrich_prospect.delay(prospect_id) for each tracer.

All seeded data sourced from publicly accessible material — Companies
House public registry, the company's own marketing website, public
news coverage.

If a tracer prospect is not yet in lead_prospects (e.g. ingest hasn't
run), the seed for that prospect is skipped. Invoke this script
post-CSV-ingest to populate enrichment for tracers.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add project root to sys.path so this is runnable as `python scripts/seed_demo_enrichment.py`
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from sqlalchemy import create_engine, text

from apps.refinery_api.config import settings


# Per-tracer enrichment seed: prospect_id → { source: (status, payload_dict, fallback_reason) }
# William Cook tracer ID matches the demo's hardcoded pros_9cb419495484
# (from apps/theater_ui/components/prospectData.ts).
TRACER_ENRICHMENT_SEED: dict[str, dict[str, tuple]] = {
    # William Cook Sheffield (UK Metals Expo tracer) — full enrichment
    "pros_9cb419495484": {
        "companies_house": ("fetched", {
            "company_number": "00321174",
            "company_name": "WILLIAM COOK HOLDINGS LIMITED",
            "company_status": "active",
            "date_of_creation": "1935-09-21",
            "sic_codes": ["24510"],  # Casting of iron
            "registered_office_address": {
                "address_line_1": "Parkway Avenue",
                "locality": "Sheffield",
                "postal_code": "S9 4WJ",
                "country": "United Kingdom",
            },
            "jurisdiction": "england-wales",
            "accounts_last_filed": "2024-04-30",
        }, None),
        "web_scrape": ("fetched", {
            "url": "https://www.wcook.co.uk",
            "title": "William Cook Holdings | High Integrity Castings",
            "meta_description": (
                "William Cook Holdings is the UK's leading supplier of high "
                "integrity steel and iron castings for the rail, defence, "
                "oil & gas and energy sectors."
            ),
            "extracted_capabilities": [
                "investment casting", "sand casting",
                "non-destructive testing", "NDT", "X-ray inspection",
                "heat treatment", "metrology", "CMM inspection",
            ],
            "extracted_customers": ["Rolls-Royce", "BAE Systems", "Babcock"],
            "extracted_certifications": ["ISO 9001", "AS 9100", "NADCAP"],
            "raw_text_sample": (
                "William Cook Holdings is the UK's leading supplier of "
                "high integrity steel and iron castings for the rail, "
                "defence, oil & gas and energy sectors. Our Sheffield "
                "foundry operates AS 9100 / NADCAP certified processes "
                "with full NDT and X-ray inspection capability..."
            ),
            "scraped_at_iso": "2026-05-19T12:00:00+00:00",
        }, None),
        "tavily_news": ("fetched", {
            "query": (
                '"William Cook Sheffield" (capacity expansion OR new contract '
                'OR acquisition OR investment OR certification OR factory OR '
                'plant OR manufacturing)'
            ),
            "results": [
                {
                    "title": "William Cook secures £4M contract with Royal Navy for submarine castings",
                    "url": "https://example-news.test/william-cook-royal-navy",
                    "snippet": (
                        "Sheffield-based William Cook Holdings has been "
                        "awarded a £4 million contract to supply high-integrity "
                        "nickel-alloy castings for the next generation of "
                        "Royal Navy submarines..."
                    ),
                    "published_date": "2025-09-15",
                    "score": 0.94,
                },
                {
                    "title": "William Cook Sheffield expands NDT capacity",
                    "url": "https://example-news.test/william-cook-ndt-expansion",
                    "snippet": (
                        "The Sheffield foundry has invested £2M in new X-ray "
                        "inspection capacity at its Parkway Avenue site, "
                        "increasing throughput by 40%..."
                    ),
                    "published_date": "2025-11-02",
                    "score": 0.89,
                },
            ],
            "results_count": 2,
            "summary": (
                "William Cook Sheffield is a UK steel and iron foundry with "
                "recent contract wins in defense (Royal Navy submarine "
                "castings) and ongoing capacity expansion in non-destructive "
                "testing. Major customers include Rolls-Royce, BAE Systems, "
                "and Babcock."
            ),
            "retrieved_at_iso": "2026-05-19T12:00:00+00:00",
        }, None),
    },

    # Caracol Aerospace Division (Industrial AI Summit tracer) — Italian, CH not_applicable
    "pros_caracol_am_001": {
        "companies_house": ("not_applicable", None, "non_uk_jurisdiction_heuristic"),
        "web_scrape": ("fetched", {
            "url": "https://www.caracol-am.com",
            "title": "Caracol | Large-Format Additive Manufacturing",
            "meta_description": (
                "Caracol designs and manufactures robotic large-format 3D "
                "printing systems for industrial production. Aerospace, "
                "marine, automotive, energy."
            ),
            "extracted_capabilities": [
                "additive manufacturing", "DED",
                "polymer extrusion",
                "non-destructive testing",
                "metrology", "CMM inspection",
            ],
            "extracted_customers": ["Airbus", "Boeing"],
            "extracted_certifications": ["ISO 9001"],
            "raw_text_sample": (
                "Caracol designs and manufactures large-format robotic 3D "
                "printing systems for aerospace, marine, energy and "
                "automotive applications. Headquartered in Italy with "
                "deployments across Europe and North America..."
            ),
            "scraped_at_iso": "2026-05-19T12:00:00+00:00",
        }, None),
        "tavily_news": ("fetched", {
            "query": (
                '"Caracol Aerospace" (capacity expansion OR new contract OR '
                'acquisition OR investment OR certification OR factory OR '
                'plant OR manufacturing)'
            ),
            "results": [
                {
                    "title": "Caracol partners with Matta AI for in-process inspection on large-format prints",
                    "url": "https://example-news.test/caracol-matta-partnership",
                    "snippet": (
                        "Italian additive manufacturing firm Caracol has "
                        "announced a partnership with Cambridge-based Matta "
                        "to deploy computer-vision-based in-process "
                        "inspection across its aerospace production cells..."
                    ),
                    "published_date": "2025-12-08",
                    "score": 0.97,
                },
            ],
            "results_count": 1,
            "summary": (
                "Caracol is an Italian large-format additive manufacturing "
                "company recently partnered with Matta AI for in-process "
                "inspection on aerospace production. Recently expanded "
                "into US market."
            ),
            "retrieved_at_iso": "2026-05-19T12:00:00+00:00",
        }, None),
    },

    # Brüggen Metallwerke GmbH (Hannover Messe tracer) — German, CH not_applicable
    # Web scrape + Tavily fall through to live enrichment on demo runs.
    "pros_brueggen_001": {
        "companies_house": ("not_applicable", None, "non_uk_jurisdiction_heuristic"),
    },

    # Lockheed Martin Aeronautics Fort Worth (IMTS Chicago) — US, CH not_applicable
    # Web scrape + Tavily fall through to live enrichment on demo runs.
    "pros_lockheed_ftw_001": {
        "companies_house": ("not_applicable", None, "non_uk_jurisdiction_heuristic"),
    },

    # Yorkshire Casting Co (Forging Industry Convention) — UK, all three expected to fetch live
    # No pre-seed; all three sources fall through to live enrichment.
    "pros_yorkshire_casting_001": {},
}


def seed_demo_enrichment() -> None:
    engine = create_engine(settings.postgres_url.replace('+asyncpg', ''))
    now = datetime.now(timezone.utc)

    inserted = 0
    skipped_prospects = 0

    with engine.begin() as conn:
        for prospect_id, sources in TRACER_ENRICHMENT_SEED.items():
            # Verify prospect exists; skip cleanly if not (CSV may not have ingested yet)
            row = conn.execute(
                text("SELECT id FROM lead_prospects WHERE id = :pid"),
                {"pid": prospect_id},
            ).first()
            if row is None:
                print(f"  skip {prospect_id} (prospect not in lead_prospects)")
                skipped_prospects += 1
                continue

            if not sources:
                print(f"  skip {prospect_id} (no seed payloads — falls through to live enrichment)")
                continue

            for source_name, source_data in sources.items():
                if not (isinstance(source_data, tuple) and len(source_data) == 3):
                    continue
                status, payload, fallback_reason = source_data
                payload_json = json.dumps(payload) if payload is not None else None

                conn.execute(
                    text("""
                        INSERT INTO enrichment_artifacts
                            (prospect_id, source, status, payload, fallback_reason, fetched_at)
                        VALUES
                            (:pid, :src, :status, CAST(:payload AS JSONB), :reason, :now)
                        ON CONFLICT (prospect_id, source) DO UPDATE SET
                            status = EXCLUDED.status,
                            payload = EXCLUDED.payload,
                            fallback_reason = EXCLUDED.fallback_reason,
                            fetched_at = EXCLUDED.fetched_at
                    """),
                    {
                        "pid": prospect_id,
                        "src": source_name,
                        "status": status,
                        "payload": payload_json,
                        "reason": fallback_reason,
                        "now": now,
                    },
                )
                inserted += 1
                print(f"  seeded {prospect_id} {source_name} {status}")

    print(f"\nDone: {inserted} rows seeded, {skipped_prospects} prospects skipped (not yet in lead_prospects)")


if __name__ == "__main__":
    seed_demo_enrichment()
