"""Pins the determinism and bounds of the Stage 1.3 fitness scorer.

compute_fitness is ADC's deterministic gate (zero LLM calls in
routing/ranking) — same input must always produce the same output,
and the result must stay within [0, 1].
"""
from datetime import datetime
from types import SimpleNamespace

import pytest

from packages.schemas.lead_prospect import LeadProspect
from packages.scoring.fitness import compute_fitness


def _prospect(
    vertical: str = "additive_manufacturing",
    factory_size_band: str = "medium",
    trade_show_provenance: bool = True,
) -> LeadProspect:
    return LeadProspect(
        id="pros_test01",
        external_lead_id="L001",
        source_system="csv_upload",
        company_name="Test Co",
        vertical=vertical,  # type: ignore[arg-type]
        factory_size_band=factory_size_band,  # type: ignore[arg-type]
        trade_show_provenance=trade_show_provenance,
        fitness_score=0.0,
        enrichment_status="complete",
        signal_hash="0" * 16,
        last_scored_at=datetime(2026, 1, 1),
    )


def test_fitness_is_deterministic():
    p = _prospect()
    qs = SimpleNamespace(capacity_decay=0.1)
    a = compute_fitness(p, qs)
    b = compute_fitness(p, qs)
    assert a == b


def test_fitness_bounded_0_1():
    p = _prospect()
    qs = SimpleNamespace(capacity_decay=0.1)
    score = compute_fitness(p, qs)
    assert 0.0 <= score <= 1.0


def test_fitness_zero_for_out_of_vertical_small_no_show():
    p = _prospect(
        vertical="out_of_vertical",
        factory_size_band="small",
        trade_show_provenance=False,
    )
    qs = SimpleNamespace(capacity_decay=1.0)
    score = compute_fitness(p, qs)
    assert score == 0.0


def test_fitness_monotonic_in_trade_show_provenance():
    qs = SimpleNamespace(capacity_decay=0.0)
    with_show = compute_fitness(_prospect(trade_show_provenance=True), qs)
    without_show = compute_fitness(_prospect(trade_show_provenance=False), qs)
    assert with_show > without_show
