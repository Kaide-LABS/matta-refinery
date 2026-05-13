from packages.schemas.defect_hypothesis import VerticalClassification

MODEL = "gemini-2.5-flash"
THINKING_LEVEL = "minimal"
TEMPS = (0.1, 0.5, 0.9)
MAX_OUT = 128
RESPONSE_SCHEMA = VerticalClassification

VERTICAL_PROMPT = """You are classifying a UK or EU manufacturing prospect into a vertical
from a fixed enum. Output strict JSON conforming to the schema. Choose `out_of_vertical` if the
prospect is clearly outside the manufacturing surface listed below; do not stretch.

Prospect:
- Company name: {company_name}
- Sector hint (from raw data, may be empty or noisy): {sector_hint}
- Public enrichment summary: {enrichment_summary}
- Raw notes from the trade-show or CRM: {raw_notes}

Allowed vertical values (choose exactly one):
- polymer_extrusion: continuous polymer extrusion, polymer molding, polymer line work
- metal_casting: ductile iron casting, sand casting, investment casting, die casting
- additive_manufacturing: large-format AM, industrial 3D printing, AM cells (OEM partner context: Caracol)
- fnb_bottling: high-speed bottling, F&B packaging, beverage line inspection
- electronics_assembly: precision component assembly, speaker/electronics QC, small-form-factor metrology
- aerospace: aerospace components, plane wings, titanium alloys, aerospace metallurgy
- out_of_vertical: prospect is clearly outside the above set

Output JSON only."""
