from datetime import datetime
from pathlib import Path
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

from packages.schemas.lead_prospect import VERTICAL_ENUM

class KnowledgeGraphAnchor(BaseModel):
    model_config = ConfigDict(extra="forbid")
    anchor_id: str
    vertical: VERTICAL_ENUM
    deployment_type: str
    citation_substrate_lines: list[Annotated[int, Field(ge=1, le=100000)]]
    citation_verbatim_excerpt: Annotated[str, Field(min_length=10, max_length=500)]
    permitted_dimensions_of_comparability: list[Annotated[str, Field(max_length=80)]]

class KnowledgeGraph(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: str
    built_at: datetime
    anchors: list[KnowledgeGraphAnchor]

def load_graph(path: Path = Path("packages/knowledge_graph/graph.json")) -> KnowledgeGraph:
    raw = path.read_text(encoding="utf-8")
    return KnowledgeGraph.model_validate_json(raw)
