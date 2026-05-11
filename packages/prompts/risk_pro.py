from packages.schemas.dossier import RiskRegister

MODEL = "gemini-3.1-pro-preview"
THINKING_LEVEL = "low"
TEMP = 0.2
MAX_OUT = 768
RESPONSE_SCHEMA = RiskRegister

RISK_PROMPT = """Produce a risk register for this prospect's likely Matta deployment. Output
strict JSON conforming to RiskRegister. Use ONLY the fixed risk categories below; do NOT invent
new categories.

Prospect:
- Company name: {company_name}
- Vertical: {vertical}
- Process taxonomy: {process_taxonomy_json}
- Public enrichment payload: {enrichment_payload}

Fixed risk categories (your findings list uses these enum values):
- legacy_cmm_infrastructure, lighting_variance, emf_environment, network_topology,
- ot_it_segmentation, regulatory_audit_burden, operator_training_overhead,
- calibration_baseline_unknown

For each finding, set severity = identified | unknown | not_applicable. Provide a 1-2 sentence
note (≤300 chars) anchored to the prospect's vertical and process taxonomy.

Output JSON only."""
