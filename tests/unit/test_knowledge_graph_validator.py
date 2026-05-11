"""Criterion 14 — Knowledge Graph startup validator.

The validator must (a) reject Cummins as a deployment anchor (per MATTA_MASTER_PRD_v2.md §1.F)
and (b) reject any anchor whose citation_substrate_lines reference is out-of-range or whose
citation_verbatim_excerpt does not actually appear in the referenced line.

These tests construct malformed graphs in-memory and invoke validate_graph_or_die through a
monkeypatched loader path. A passing graph (the committed graph.json) must also validate clean.
"""
from datetime import datetime
from pathlib import Path

import pytest

from packages.knowledge_graph import verify as kg_verify
from packages.knowledge_graph.loader import KnowledgeGraph, KnowledgeGraphAnchor
from packages.knowledge_graph.verify import KnowledgeGraphProvenanceError, validate_graph_or_die


def test_committed_graph_passes_validation():
    """Sanity check: the actual committed graph.json must validate against the substrate."""
    # Direct invocation — no monkeypatch. Uses the real graph.json and Matta_Intel_cleaned.md.
    validate_graph_or_die()


def test_cummins_anchor_is_rejected(monkeypatch):
    """Per §1.F audit-trail invariant, no Cummins deployment anchor is permitted."""
    cummins_graph = KnowledgeGraph(
        version="test",
        built_at=datetime.utcnow(),
        anchors=[
            KnowledgeGraphAnchor(
                anchor_id="matta_deployment_cummins_daventry",
                vertical="electronics_assembly",
                deployment_type="engine_qc",
                citation_substrate_lines=[1],
                citation_verbatim_excerpt="placeholder excerpt long enough for min_length",
                permitted_dimensions_of_comparability=["unused"],
            )
        ],
    )
    monkeypatch.setattr(kg_verify, "load_graph", lambda: cummins_graph)

    with pytest.raises(KnowledgeGraphProvenanceError) as exc_info:
        validate_graph_or_die()
    assert "cummins" in str(exc_info.value).lower()


def test_out_of_range_citation_line_is_rejected(monkeypatch, tmp_path):
    """Citation line 999999 (well past substrate end) must be rejected."""
    bad_graph = KnowledgeGraph(
        version="test",
        built_at=datetime.utcnow(),
        anchors=[
            KnowledgeGraphAnchor(
                anchor_id="matta_deployment_bowers_and_wilkins",
                vertical="electronics_assembly",
                deployment_type="precision_speaker_components",
                citation_substrate_lines=[99999],
                citation_verbatim_excerpt="working with Bowers & Wilkins",
                permitted_dimensions_of_comparability=["surface_finish_qc"],
            )
        ],
    )
    monkeypatch.setattr(kg_verify, "load_graph", lambda: bad_graph)

    with pytest.raises(KnowledgeGraphProvenanceError) as exc_info:
        validate_graph_or_die()
    assert "out of range" in str(exc_info.value).lower()


def test_verbatim_excerpt_mismatch_is_rejected(monkeypatch):
    """If the citation_verbatim_excerpt is not actually present in the referenced substrate line,
    the validator must reject — this is the citation-fabrication failure mode the §6.5 runtime
    check exists to catch."""
    fabricated_graph = KnowledgeGraph(
        version="test",
        built_at=datetime.utcnow(),
        anchors=[
            KnowledgeGraphAnchor(
                anchor_id="matta_deployment_bowers_and_wilkins",
                vertical="electronics_assembly",
                deployment_type="precision_speaker_components",
                citation_substrate_lines=[540],
                citation_verbatim_excerpt="this exact phrase is not in line 540",
                permitted_dimensions_of_comparability=["surface_finish_qc"],
            )
        ],
    )
    monkeypatch.setattr(kg_verify, "load_graph", lambda: fabricated_graph)

    with pytest.raises(KnowledgeGraphProvenanceError) as exc_info:
        validate_graph_or_die()
    err = str(exc_info.value).lower()
    assert "not found" in err and "substrate line" in err
