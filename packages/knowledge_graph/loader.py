from datetime import datetime
from pathlib import Path
from typing import Annotated, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field

from packages.schemas.lead_prospect import VERTICAL_ENUM

# Phase 1.7 Stage C: evidence_strength captures the gradient of grounding
# for each KG anchor. Damjan's "every KG citation looks the same; I can't
# tell strong from weak" probe is closed by surfacing this asymmetry
# explicitly in §3 Comparable Deployment.
EvidenceStrength = Literal[
    "named_customer_specific_deployment",  # B&W: named customer + named application
    "named_customer_oem_partnership",      # Caracol: named OEM but partnership not deployment
    "unnamed_customer_quantitative_claim", # polymer: no name, but >99% perf claim is specific
    "unnamed_customer_vertical_mention",   # global drinks: no name, no quantitative figure
]


class KnowledgeGraphAnchor(BaseModel):
    model_config = ConfigDict(extra="forbid")
    anchor_id: str
    vertical: VERTICAL_ENUM
    deployment_type: str
    citation_substrate_lines: list[Annotated[int, Field(ge=1, le=100000)]]
    citation_verbatim_excerpt: Annotated[str, Field(min_length=10, max_length=500)]
    permitted_dimensions_of_comparability: list[Annotated[str, Field(max_length=80)]]
    evidence_strength: EvidenceStrength
    # Phase 1.7 Stage D: source provenance fields. Populate from the
    # private kg_anchor_sources.md substrate-mapping file. The Drive UI's
    # KGValidatorIndicator popover renders these as "Verify (live)" and
    # "Verify (Wayback)" links so a Damjan-audit reader clicks straight
    # through to the authoritative source page containing the verbatim
    # excerpt.
    source_url: Optional[Annotated[str, Field(max_length=2048)]] = None
    source_archive_url: Optional[Annotated[str, Field(max_length=2048)]] = None
    source_label: Optional[Annotated[str, Field(max_length=128)]] = None
    # Phase 1.7 Stage E: when this anchor describes a NAMED partner
    # (e.g. Caracol, Bowers & Wilkins), this field carries a
    # distinctive substring of the partner's company name. The
    # comparable-deployment selector uses it to decide whether the
    # briefed prospect IS the named subject (substring match → strong
    # evidence_strength) or merely shares the anchor's vertical
    # (no match → downgrade to vertical_precedent). Null when the
    # anchor is already vertical-level (unnamed_customer_*).
    named_subject_company: Optional[Annotated[str, Field(max_length=128)]] = None

class KnowledgeGraph(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: str
    built_at: datetime
    anchors: list[KnowledgeGraphAnchor]

def load_graph(path: Path = Path("packages/knowledge_graph/graph.json")) -> KnowledgeGraph:
    raw = path.read_text(encoding="utf-8")
    return KnowledgeGraph.model_validate_json(raw)
