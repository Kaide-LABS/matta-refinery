from packages.schemas.dossier import ProcessTaxonomy

MODEL = "gemini-2.5-pro"
THINKING_LEVEL = "medium"
TEMP = 0.2
MAX_OUT = 1024
RESPONSE_SCHEMA = ProcessTaxonomy

TAXONOMY_PROMPT = """You are synthesizing a process taxonomy for a manufacturing prospect.
Output strict JSON conforming to ProcessTaxonomy.

Prospect:
- Company name: {company_name}
- Vertical (already classified by Stage 1.2): {vertical}
- Public enrichment payload: {enrichment_payload}
- Allowed evidence whitelist (lines from substrate, cite only from this list when you reference
  factual claims; do NOT invent claims that require evidence outside this list): {allowed_evidence}

Produce:
- primary_process: the dominant production process at line-level granularity (≤200 chars)
- sub_processes: up to 10 sub-process names (each ≤80 chars)
- line_level_steps: up to 20 step names in the production order (each ≤80 chars)
- rationale: 1-3 sentence explanation tied to vertical + enrichment (≤600 chars)

Output JSON only."""
