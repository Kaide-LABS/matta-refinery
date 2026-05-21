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

def select_comparable(
    vertical: str,
    process_taxonomy: ProcessTaxonomy | None,
) -> tuple[MATTA_CUSTOMER_ANCHOR_ENUM | str, int, list[str]]:
    """Deterministic comparable selection (v4 Stage 2.3a contribution).

    Returns (anchor_id, citation_substrate_line, permitted_dimensions_of_comparability).
    Returns ('no_comparable_available', 0, []) if no anchor matches.
    """
    # Phase 1 rules: 1-to-1 vertical → anchor mapping, demoted to multi-key when verticals expand.
    vertical_to_anchor = {
        "electronics_assembly": "matta_deployment_bowers_and_wilkins",
        "additive_manufacturing": "matta_deployment_caracol_am",
        "fnb_bottling": "matta_deployment_global_drinks_brand",
        "polymer_extrusion": "matta_deployment_polymer_unnamed",
        # Phase 1.7 Stage C: metal_casting mapping REMOVED. The prior
        # matta_deployment_metal_casting_unnamed anchor was dropped from
        # graph.json because its citation excerpt could not be substantiated
        # against Matta's verified public sources. Metal-casting prospects
        # (William Cook etc.) now route to no_comparable_available —
        # honest framing, not padded comparability prose.
        # aerospace, metal_casting, out_of_vertical, vertical_uncertain →
        #   no_comparable_available
    }
    anchor_id = vertical_to_anchor.get(vertical)
    if anchor_id is None:
        return ("no_comparable_available", 0, [])
    anchor = _find_anchor_by_id(anchor_id)  # from loaded graph cache
    return (
        _enum_for_anchor_id(anchor_id),  # maps to MATTA_CUSTOMER_ANCHOR_ENUM
        anchor.citation_substrate_lines[0],  # primary citation line
        anchor.permitted_dimensions_of_comparability,
    )
