from packages.schemas.defect_hypothesis import LikelyDefectClassHypothesis

MODEL = "gemini-2.5-flash"
THINKING_LEVEL = "minimal"
TEMPS = (0.1, 0.5, 0.9)
MAX_OUT = 512
RESPONSE_SCHEMA = LikelyDefectClassHypothesis

DEFECT_PROMPT = """Classify the likely defect classes for this manufacturing process. Output
strict JSON conforming to LikelyDefectClassHypothesis. Do NOT invent defect categories outside
the enum. Do NOT claim high coverage when your evidence is thin.

Process context:
- Vertical: {vertical}
- Process taxonomy: {process_taxonomy_json}
- Allowed evidence whitelist: {allowed_evidence}

Allowed defect classes (your conformal_set field is a subset of these):
- porosity, dimensional_drift, surface_inclusions, tool_wear, calibration_drift,
- material_defect, process_drift, unknown

Decision rules:
- If the process is well-understood and you have specific evidence, include the 1-3 most likely
  defect classes in conformal_set and set coverage to your honest estimate (0.0-1.0).
- If evidence is weak or the process is out-of-vertical, return an empty conformal_set or
  include only "unknown"; the system will mark for human review.
- The calibration_version field will be overwritten by the system; populate as best-effort.

Output JSON only."""
