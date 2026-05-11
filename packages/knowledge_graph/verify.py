from pathlib import Path
from packages.knowledge_graph.loader import load_graph

class KnowledgeGraphProvenanceError(RuntimeError):
    pass

SUBSTRATE_PATH = Path("Matta_Intel_cleaned.md")

def validate_graph_or_die() -> None:
    graph = load_graph()
    substrate_lines = SUBSTRATE_PATH.read_text(encoding="utf-8").splitlines()
    for anchor in graph.anchors:
        if "cummins" in anchor.anchor_id.lower():
            raise KnowledgeGraphProvenanceError(
                f"Cummins is excluded as a deployment anchor (MATTA_MASTER_PRD_v2.md §1.F). "
                f"Found: {anchor.anchor_id}"
            )
        for line_no in anchor.citation_substrate_lines:
            if line_no < 1 or line_no > len(substrate_lines):
                raise KnowledgeGraphProvenanceError(
                    f"Anchor {anchor.anchor_id} cites substrate line {line_no} which is out of range "
                    f"(substrate has {len(substrate_lines)} lines)."
                )
            line_text = substrate_lines[line_no - 1]
            if anchor.citation_verbatim_excerpt not in line_text:
                raise KnowledgeGraphProvenanceError(
                    f"Anchor {anchor.anchor_id} citation_verbatim_excerpt "
                    f"'{anchor.citation_verbatim_excerpt}' not found in substrate line {line_no}."
                )
