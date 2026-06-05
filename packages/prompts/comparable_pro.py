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


# Stage E Named-Subject prompt: used when the briefed prospect IS the
# anchor's named partner (Caracol clicking Caracol). This is an internal
# FDE pre-visit briefing — sober, analytic, third-person. State the
# verified deployment as established fact; do NOT address the customer or
# slip into Matta sales/marketing voice.
COMPARABLE_PROMPT_NAMED = """A deterministic rules engine has PRE-SELECTED the comparable Matta
deployment anchor for this prospect. The prospect IS Matta's named, verified partner for this
anchor. Write a single analytic sentence, for an internal pre-visit briefing, that states the
deployment as established fact and names which permitted dimension is the operative axis.

PRE-SELECTED anchor (do NOT propose a different anchor): {matta_customer_anchor}
Anchor citation substrate line: {citation_substrate_line}
Permitted dimensions of comparability for this anchor (choose ONE or compose from this set ONLY):
{permitted_dimensions_of_comparability}

Prospect (the named partner):
- Company name: {company_name}
- Vertical: {vertical}
- Process taxonomy: {process_taxonomy_json}

Register (this is an INTERNAL analytic briefing, NOT customer-facing marketing):
- Third person only. Refer to "Matta" by name. NEVER use "we", "our", or "us".
- State the deployment as established fact (e.g., "Matta's verified deployment with {company_name}...").
- Name the operative dimension explicitly from the permitted list.
- Mirror this register exactly: "Matta's verified deployment with Caracol (oem_closed_loop_partnership)
  is the operative precedent on the large_format_robot_am_cell dimension."

Strict constraints:
- Do NOT propose a different anchor. Do NOT cite a different Matta deployment.
- Do NOT exceed 250 characters in your prose.
- Do NOT use forward-looking sales language ("excited to", "shared vision", "build together",
  "build on this foundation", "testament"). No first-person voice. Do NOT address the customer.

Output JSON with a single field `prose` containing the <=250-char string."""


# Stage E Vertical-Precedent prompt: used when the prospect shares the
# anchor's vertical but is NOT the named subject. The prose must be
# honest about this — frame the precedent positively as "they would be
# next" rather than negatively as "we don't have them."
COMPARABLE_PROMPT_PRECEDENT = """A deterministic rules engine has PRE-SELECTED the comparable Matta
deployment anchor for this prospect by vertical match. The prospect is NOT a current Matta
customer; the anchor is a verified DEPLOYMENT in the same vertical that serves as the technical
precedent.

PRE-SELECTED anchor (do NOT propose a different anchor): {matta_customer_anchor}
Anchor's named subject (Matta's current partner in this vertical): {anchor_named_subject}
Anchor citation substrate line: {citation_substrate_line}
Permitted dimensions of comparability for this anchor (choose ONE or compose from this set ONLY):
{permitted_dimensions_of_comparability}

Prospect (NOT a current Matta customer):
- Company name: {company_name}
- Vertical: {vertical}
- Process taxonomy: {process_taxonomy_json}

Strict constraints:
- Do NOT propose a different anchor. Do NOT cite a different Matta deployment.
- Do NOT exceed 250 characters in your prose.
- Frame as forward-looking opportunity: "{company_name} would be a net-new deployment on the same
  {{dimension}} pattern Matta validated with {anchor_named_subject}."
- Do NOT imply {company_name} is a current Matta customer.
- Name the operative dimension explicitly from the permitted list.

Output JSON with a single field `prose` containing the <=250-char string."""


# Backward-compatible alias for any caller still importing
# COMPARABLE_PROMPT directly. Phase 1.7 Stage E: dossier_section_comparable
# now picks between COMPARABLE_PROMPT_NAMED and COMPARABLE_PROMPT_PRECEDENT
# based on the selector's is_named_subject_match flag.
COMPARABLE_PROMPT = COMPARABLE_PROMPT_PRECEDENT
