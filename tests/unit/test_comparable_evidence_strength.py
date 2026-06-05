"""Stage E: §3 evidence_strength gating — named subject vs vertical precedent.

The selector returns is_named_subject_match=True only when the briefed
prospect IS the anchor's named subject (Caracol clicking Caracol).
Otherwise the worker downgrades evidence_strength from the anchor's
strong label (e.g. 'named_customer_oem_partnership') to
'vertical_precedent'. The contrast — Caracol = green/named, every
other AM prospect = slate/precedent — is the load-bearing
calibrated-honesty proof point.

Plus a substring-guard test that loads ALL seed CSV company names
and asserts none false-positive the substring match against
'Caracol', 'Bowers', or 'Wilkins' except the one intended Caracol
row. The substring rule is fragile-by-design (distinctive partner
names only); this guard fails loudly if a future seed introduces
a collision.
"""
import csv
import json
from pathlib import Path

import pytest

from packages.knowledge_graph.loader import load_graph
from packages.knowledge_graph.select import (
    _is_named_subject_match,
    select_comparable,
)


CARACOL_ANCHOR_ID = "matta_deployment_caracol_am"
BW_ANCHOR_ID = "matta_deployment_bowers_and_wilkins"

SEED_CSV_DIR = Path("apps/theater_ui/public/seed_csvs")


def _find_anchor(anchor_id: str):
    for a in load_graph().anchors:
        if a.anchor_id == anchor_id:
            return a
    raise ValueError(anchor_id)


def _all_seed_company_names() -> list[tuple[str, str]]:
    """Returns [(csv_filename, company_name), ...] across all seed CSVs."""
    rows: list[tuple[str, str]] = []
    for csv_path in sorted(SEED_CSV_DIR.glob("*.csv")):
        with csv_path.open(encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                rows.append((csv_path.name, row["company_name"]))
    return rows


# ─── selector match-rule unit tests ────────────────────────────────────────


def test_caracol_aerospace_division_matches_named_subject():
    """The intended named match: Caracol Aerospace Division (rank-1
    in Industrial_AI_Summit_2025) IS the caracol_am anchor's named
    subject. evidence_strength must stay at the anchor's strong label."""
    anchor = _find_anchor(CARACOL_ANCHOR_ID)
    assert anchor.named_subject_company == "Caracol"
    assert _is_named_subject_match(anchor, "Caracol Aerospace Division") is True

    anchor_id, _line, _dims, is_match = select_comparable(
        "additive_manufacturing", None, "Caracol Aerospace Division"
    )
    assert anchor_id == CARACOL_ANCHOR_ID
    assert is_match is True


def test_non_caracol_am_prospects_get_vertical_precedent():
    """Velo3D / CEAD / Relativity Space match the AM vertical but are
    NOT the named subject. is_named_subject_match must be False so the
    worker downgrades evidence_strength to vertical_precedent."""
    anchor = _find_anchor(CARACOL_ANCHOR_ID)
    for non_match in ["Velo3D", "CEAD Group", "Relativity Space", "Landing AI"]:
        assert _is_named_subject_match(anchor, non_match) is False, non_match
        _, _, _, is_match = select_comparable(
            "additive_manufacturing", None, non_match
        )
        assert is_match is False, non_match


def test_bowers_and_wilkins_named_subject_match_exists_in_principle():
    """Hypothetical: if a prospect named 'Bowers & Wilkins' appeared,
    the substring match should fire (anchor's named_subject_company
    is 'Bowers & Wilkins'). Pins the second named anchor's behaviour."""
    anchor = _find_anchor(BW_ANCHOR_ID)
    assert anchor.named_subject_company == "Bowers & Wilkins"
    assert _is_named_subject_match(anchor, "Bowers & Wilkins Worthing") is True
    assert _is_named_subject_match(anchor, "Sony Electronics") is False


def test_unmatched_vertical_returns_honest_decline_untouched():
    """Steel / metal_casting / aerospace / etc still hit
    no_comparable_available. Stage E must not regress the honest-decline
    path — that's the architectural anti-replication guarantee."""
    for vertical in ("metal_casting", "aerospace", "out_of_vertical", "vertical_uncertain"):
        anchor_id, line, dims, is_match = select_comparable(
            vertical, None, "Tata Steel UK"
        )
        assert anchor_id == "no_comparable_available", vertical
        assert line == 0
        assert dims == []
        assert is_match is False


# ─── substring guard against seed-CSV collisions ──────────────────────────


# Phase 1.7 Stage E: seed-CSV entries whose company_name contains
# 'caracol' as a case-insensitive substring AND legitimately ARE
# Caracol (same company, different booths / regional offices). The
# selector's substring match is INTENDED to inflate these to the
# named-subject-match path, just like the rank-1 row. If a NEW
# 'caracol*' company_name appears in a seed CSV that isn't actually
# Caracol, this whitelist must be reviewed and updated.
LEGITIMATE_CARACOL_ROWS = {
    ("Industrial_AI_Summit_2025_leads.csv", "Caracol Aerospace Division"),
    ("Industrial_AI_Summit_2025_leads.csv", "Caracol AM Lombardia"),
    ("Hannover_Messe_2025_leads.csv", "Caracol AM (DE booth)"),
}

# Same idea for the Bowers & Wilkins anchor. There are NO legitimate
# B&W prospects in the current seed CSVs — the empty set is the
# expected state. Bowers/Wilkins fragments that show up below are
# collisions that the CURRENT full-phrase selector rejects.
LEGITIMATE_BW_ROWS: set[tuple[str, str]] = set()


def test_caracol_fragment_in_seed_csvs_matches_only_legitimate_caracol_rows():
    """Loud-guard the substring rule. Any seed_csvs/*.csv row whose
    company_name contains 'caracol' (case-insensitive) MUST be a
    legitimate Caracol row (whitelist above). Adding a non-Caracol
    company that happens to contain 'caracol' as a substring would
    false-positive the named-subject match — the selector would
    promote that prospect to Caracol's strong evidence_strength,
    inflating the named-partnership claim.

    If you intentionally added such a row, either:
      (a) rename the prospect so 'caracol' is no longer a substring, or
      (b) update LEGITIMATE_CARACOL_ROWS and confirm in PR review."""
    found = {
        (csv_name, company)
        for csv_name, company in _all_seed_company_names()
        if "caracol" in company.lower()
    }
    unexpected = found - LEGITIMATE_CARACOL_ROWS
    assert not unexpected, (
        f"Unexpected 'caracol' substring in seed CSV company_name: "
        f"{sorted(unexpected)}. These would false-positive the "
        f"caracol_am named-subject match. Rename the prospect or "
        f"explicitly add to LEGITIMATE_CARACOL_ROWS."
    )


def test_bowers_or_wilkins_fragment_in_seed_csvs_does_not_falsepositive_selector():
    """Loose guard against the second named anchor. Any seed_csvs/*.csv
    row whose company_name contains 'bowers' or 'wilkins'
    (case-insensitive) is flagged; the test then asserts that the
    selector's CURRENT full-phrase match correctly rejects it.

    'Bowers Manufacturing' (UK_Metals_Expo_2025) is a known fragment
    collision that the full-phrase 'Bowers & Wilkins' rule correctly
    rejects. If the matcher is ever tightened to single-token, this
    test fires and forces a rule re-examination."""
    bw_anchor = _find_anchor(BW_ANCHOR_ID)
    fragment_hits = [
        (csv_name, company)
        for csv_name, company in _all_seed_company_names()
        if "bowers" in company.lower() or "wilkins" in company.lower()
    ]
    # Selector must NOT promote any of these unless they're explicitly
    # whitelisted as a legitimate B&W entry.
    for csv_name, company in fragment_hits:
        is_match = _is_named_subject_match(bw_anchor, company)
        is_legitimate = (csv_name, company) in LEGITIMATE_BW_ROWS
        assert is_match == is_legitimate, (
            f"Selector false-positive: {company!r} in {csv_name} → "
            f"is_named_subject_match={is_match} but legitimate B&W "
            f"row={is_legitimate}. Either tighten select._is_named_"
            f"subject_match or rename the prospect."
        )


# ─── schema + KG self-consistency ─────────────────────────────────────────


def test_graph_named_subject_population_is_consistent():
    """The two 'named_customer_*' anchors must carry named_subject_company;
    the two 'unnamed_customer_*' anchors must NOT (they're vertical-level
    and a named_subject_company on them would be a category error)."""
    graph = load_graph()
    for a in graph.anchors:
        if a.evidence_strength.startswith("named_customer_"):
            assert a.named_subject_company, (
                f"Named anchor {a.anchor_id} missing named_subject_company"
            )
        else:
            assert a.named_subject_company is None, (
                f"Unnamed anchor {a.anchor_id} should not carry "
                f"named_subject_company={a.named_subject_company!r}"
            )
