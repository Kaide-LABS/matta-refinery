"""Pins KG substrate-pinning validator behaviour.

The KG validator is load-bearing: it runs at API container boot and
refuses to start the process if any anchor's verbatim quote drifts
from the substrate. These tests pin both the happy path (current
shipping graph + substrate validates) and the failure path
(corrupted excerpt raises).
"""
import json
from pathlib import Path

import pytest

from packages.knowledge_graph.verify import (
    KnowledgeGraphProvenanceError,
    SUBSTRATE_PATH,
    validate_graph_or_die,
)


def test_substrate_path_exists():
    assert SUBSTRATE_PATH.exists(), (
        f"KG substrate expected at {SUBSTRATE_PATH} — moved in Stage E "
        "audit cleanup. If you moved it again, update verify.py."
    )


def test_shipping_graph_validates():
    # Must not raise — the graph as currently shipped passes its own
    # verification. If this fails, an anchor's citation_verbatim_excerpt
    # has drifted from the substrate line it claims.
    validate_graph_or_die()


def test_out_of_range_line_raises(tmp_path, monkeypatch):
    """An anchor citing a line beyond the substrate length must raise."""
    from packages.knowledge_graph import loader, verify as verify_mod

    # Build a tiny substrate and a graph that points past its end.
    sub = tmp_path / "substrate.md"
    sub.write_text("line 1\nline 2\n", encoding="utf-8")

    monkeypatch.setattr(verify_mod, "SUBSTRATE_PATH", sub)

    fake_graph = type(
        "FG", (), {
            "anchors": [type("A", (), {
                "anchor_id": "fake_anchor",
                "citation_substrate_lines": [9999],
                "citation_verbatim_excerpt": "anything",
            })()],
        }
    )()
    monkeypatch.setattr(verify_mod, "load_graph", lambda: fake_graph)

    with pytest.raises(KnowledgeGraphProvenanceError, match="out of range"):
        validate_graph_or_die()


def test_drifted_excerpt_raises(tmp_path, monkeypatch):
    """An anchor whose excerpt doesn't appear on its cited line must raise."""
    from packages.knowledge_graph import verify as verify_mod

    sub = tmp_path / "substrate.md"
    sub.write_text("line one says hello world\n", encoding="utf-8")
    monkeypatch.setattr(verify_mod, "SUBSTRATE_PATH", sub)

    fake_graph = type(
        "FG", (), {
            "anchors": [type("A", (), {
                "anchor_id": "drifted_anchor",
                "citation_substrate_lines": [1],
                "citation_verbatim_excerpt": "this does not appear",
            })()],
        }
    )()
    monkeypatch.setattr(verify_mod, "load_graph", lambda: fake_graph)

    with pytest.raises(KnowledgeGraphProvenanceError, match="not found in substrate"):
        validate_graph_or_die()
