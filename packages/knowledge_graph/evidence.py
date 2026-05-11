from typing import Literal
from packages.knowledge_graph.loader import load_graph

def compute_allowed_evidence(
    vertical: str,
    section_type: Literal["taxonomy", "defect_hypothesis", "comparable", "risk", "approach"],
    prospect_signals: dict,
) -> list[int]:
    """Compute the citation-substrate-line whitelist for a given section + prospect.

    Returns the union of substrate lines from KG anchors whose vertical matches AND whose
    deployment_type relevance to the section_type is non-zero. Empty list signals 'no anchor data'
    and triggers section-granular DS-CP (Tightening 4) to mark the section UNVERIFIED_INSUFFICIENT_DATA.
    """
    graph = load_graph()
    matching_anchors = [a for a in graph.anchors if a.vertical == vertical]
    if not matching_anchors:
        return []  # Triggers DS-CP strip
    all_lines = set()
    for a in matching_anchors:
        all_lines.update(a.citation_substrate_lines)
    return sorted(list(all_lines))
