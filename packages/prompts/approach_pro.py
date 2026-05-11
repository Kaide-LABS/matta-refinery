from packages.schemas.dossier import SuggestedApproach

MODEL = "gemini-3.1-pro-preview"
THINKING_LEVEL = "low"
TEMP = 0.2
MAX_OUT = 768
RESPONSE_SCHEMA = SuggestedApproach

APPROACH_PROMPT = """Produce a suggested-approach recommendation. Output strict JSON conforming
to SuggestedApproach. Use ONLY the fixed template enum; do NOT invent new templates.

Prospect:
- Company name: {company_name}
- Vertical: {vertical}
- Process taxonomy: {process_taxonomy_json}
- Defect-class hypothesis conformal set: {conformal_set}
- Identified risks: {risk_findings}

Fixed approach templates:
- two_camera_pilot, four_camera_pilot, full_line_deployment, caracol_am_oem_partnership

Compose:
- template: one of the enum above.
- rationale: 1-3 sentence explanation tied to vertical + defect + risk (≤600 chars).
- day_one_risks: up to 8 short strings (each ≤120 chars) naming risks the FDE should expect on
  day 1 of deployment (e.g., 'lighting calibration', 'PLC OPC-UA gateway access').

Output JSON only."""
