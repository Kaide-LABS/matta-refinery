from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

class DimensionOfComparabilityProse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    prose: Annotated[str, Field(max_length=250)]

MODEL = "gemini-2.5-pro"
THINKING_LEVEL = "low"
TEMP = 0.3
MAX_OUT = 256
RESPONSE_SCHEMA = DimensionOfComparabilityProse  # wrapper: { prose: str }

COMPARABLE_PROMPT = """A deterministic rules engine has PRE-SELECTED the comparable Matta
deployment anchor for this prospect. Your job is to write a 1-2 sentence `dimension_of_comparability`
explaining the AXIS on which the comparison holds.

PRE-SELECTED anchor (do NOT propose a different anchor): {matta_customer_anchor}
Anchor citation substrate line: {citation_substrate_line}
Permitted dimensions of comparability for this anchor (choose ONE or compose from this set ONLY):
{permitted_dimensions_of_comparability}

Prospect:
- Company name: {company_name}
- Vertical: {vertical}
- Process taxonomy: {process_taxonomy_json}

Strict constraints:
- Do NOT propose a different anchor. Do NOT cite a different Matta deployment.
- Do NOT exceed 250 characters in your prose.
- Name the dimension explicitly (e.g., 'surface-finish QC stage similarity'); name what does
  NOT carry over (e.g., 'NOT process category, NOT production volume') if relevant in your 250 chars.

Output JSON with a single field `prose` containing the ≤250-char string."""
