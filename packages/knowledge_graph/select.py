from packages.schemas.dossier import MATTA_CUSTOMER_ANCHOR_ENUM, ProcessTaxonomy
from packages.knowledge_graph.loader import load_graph, KnowledgeGraphAnchor


def _find_anchor_by_id(anchor_id: str) -> KnowledgeGraphAnchor:
    graph = load_graph()
    for anchor in graph.anchors:
        if anchor.anchor_id == anchor_id:
            return anchor
    raise ValueError(f"Anchor {anchor_id} not found in graph")


def _enum_for_anchor_id(anchor_id: str) -> MATTA_CUSTOMER_ANCHOR_ENUM:
    return anchor_id  # type: ignore


def _is_named_subject_match(anchor: KnowledgeGraphAnchor, prospect_company_name: str) -> bool:
    """True iff this prospect IS the anchor's named subject.

    Phase 1.7 Stage E: distinguishes "this prospect is the named
    partner Matta has" from "this prospect merely shares the anchor's
    vertical". Used to gate evidence_strength downgrade so non-named
    prospects can't inherit a named partner's strong label.

    Match rule: case-insensitive substring of anchor.named_subject_company
    inside prospect_company_name. Distinctive substrings ("Caracol",
    "Bowers & Wilkins") are safe for the current and seeded cohorts —
    tests/unit/test_comparable_evidence_strength.py asserts no other
    seeded company name false-positives.

    Returns False if the anchor has no named subject (unnamed
    vertical-level anchors), or if either string is empty.
    """
    if not anchor.named_subject_company or not prospect_company_name:
        return False
    return anchor.named_subject_company.lower() in prospect_company_name.lower()


def select_comparable(
    vertical: str,
    process_taxonomy: ProcessTaxonomy | None,
    prospect_company_name: str = "",
) -> tuple[MATTA_CUSTOMER_ANCHOR_ENUM | str, int, list[str], bool]:
    """Deterministic comparable selection (v4 Stage 2.3a contribution).

    Returns (anchor_id, citation_substrate_line, permitted_dimensions,
    is_named_subject_match).

    Returns ('no_comparable_available', 0, [], False) if no anchor
    matches the prospect's vertical. The honest-decline path is
    unchanged by Stage E — that's the right behavior for verticals
    with no verified Matta deployment.

    Stage E: the 4th tuple element is True iff the prospect IS the
    anchor's named subject (Caracol clicking Caracol, hypothetical
    B&W clicking B&W). Non-named prospects in an anchored vertical
    get False so the worker can downgrade evidence_strength from
    the anchor's strong label to "vertical_precedent".
    """
    # Phase 1 rules: 1-to-1 vertical → anchor mapping, demoted to multi-key when verticals expand.
    vertical_to_anchor = {
        "electronics_assembly": "matta_deployment_bowers_and_wilkins",
        "additive_manufacturing": "matta_deployment_caracol_am",
        "fnb_bottling": "matta_deployment_global_drinks_brand",
        "polymer_extrusion": "matta_deployment_polymer_unnamed",
        # aerospace, metal_casting, out_of_vertical, vertical_uncertain →
        #   no_comparable_available (honest decline)
    }
    anchor_id = vertical_to_anchor.get(vertical)
    if anchor_id is None:
        return ("no_comparable_available", 0, [], False)
    anchor = _find_anchor_by_id(anchor_id)
    return (
        _enum_for_anchor_id(anchor_id),
        anchor.citation_substrate_lines[0],
        anchor.permitted_dimensions_of_comparability,
        _is_named_subject_match(anchor, prospect_company_name),
    )
