# LATERAL_PRD_v2.md

## The Concept.

**Broken axes: Ingress shape, Output shape, Statefulness location, Buyer/user surface.** The CRM-Native Deployment Slot Sidecar breaks the Refinery's separate dashboard and Postgres-first product surface. Hubspot or Salesforce becomes the operating surface and primary prospect system of record. The sidecar subscribes to CRM export/webhook events, enriches and scores leads in the background, then writes back a custom object or note: `Matta Deployment Intelligence`.

Stage 1 is not a standalone queue UI. It appears as CRM list views and per-lead fields: `refinery_fit_score`, `vertical`, `slot_readiness`, `requires_human_review`, and `next_best_action`. Stage 2 appears as a dossier note or attached Google Doc link on the promoted prospect. This solves the continuous post-show-to-pre-visit bottleneck without asking Doug or the Special Projects hire to maintain another system.

The lateral breaks a real assumption rather than reskinning the Refinery: state lives in the CRM where the lead already lives. The sidecar keeps only an idempotency/event ledger and cache, not canonical prospect ownership. Anti-Replication holds because Matta is not building CRM workflow software as core IP; this is an adjacent integration layer that can be unplugged without touching any Matta product surface.

## The Strategic Hook.

The strongest hook is "do not add another place to look." `Matta_Intel_cleaned.md` line 294 says UK Metals Expo produced "124 leads in two days," and line 284 says Advanced Engineering produced "over 100 incredible leads" on day one. The existing workflow almost certainly starts in a CRM or export because the modernized PRD already names Hubspot/Salesforce export as a valid Refinery source. This lateral accepts that gravitational center and turns the CRM itself into the triage board.

The CRM-native output also matches the Special Projects job. Line 625 says the hire will support strategy, fundraising, and customer deals, and must turn complex ideas into concise, polished points for corporate partners. A dossier written back to the CRM account/contact record is immediately reusable for founder review, FDE prep, and follow-up. The FDE JD line 704 names "engaging prospective customers, qualifying leads, scoping problems"; line 705 says the same person moves from trade shows to factories. CRM-native continuity keeps that handoff traceable.

`Matta_Dossier.md` supports the founder-specific psychology. Brion is described as the commercial force driving two-factory-per-month scaling (section 2, line 43) and as pragmatic and metric-driven (section 5, line 67). Damjan's section says he is the gatekeeper for FastAPI, Pydantic, Postgres, SQLAlchemy, Redis, and Celery patterns (line 164), but also that he rejects hand-wavy architecture and demands idempotency (lines 178-183). This lateral gives Brion the least new operational drag and gives Damjan a small, typed integration adapter rather than a new application to own.

## The Agent Architecture.

All model calls route through Vertex AI `europe-west4` via `google-genai`, using only `gemini-3-flash-preview` and `gemini-3.1-pro-preview`. The sidecar remains upstream of deployment and never reads or writes Matta production systems, factory data, camera streams, edge firmware, Manufacturing Foundation Models, or Manufacturing OS surfaces.

Ingress contract: `POST /crm/webhook/hubspot`, `POST /crm/webhook/salesforce`, and `POST /crm/export/email` normalize CRM records into `CRMLeadSignal`. The deterministic ADC routes events by `(crm_provider, object_type, changed_fields, action)` into `PRIORITIZE_RECORD`, `PRIORITIZE_BATCH`, `DOSSIER_REQUEST`, or `HUMAN_REVIEW`. Unknown objects stop at human review. Schemas use `extra="forbid"` and provider-specific adapters map native CRM IDs to `external_lead_id`.

Stage 1: deterministic enrichment runs on changed or newly imported leads. N=3 `gemini-3-flash-preview` classifies vertical with `thinking_level="minimal"` and temperatures 0.1, 0.5, 0.9. Deterministic scoring writes back CRM fields and appends an audit note explaining the score as candidate surfacing, not decision automation. Conformal calibration is not used on the fit score because scoring is deterministic; it is reserved for defect-class hypotheses where the PRD requires it.

Stage 2: the FDE clicks a CRM button or changes `Generate_Dossier__c=true`. The sidecar reads the CRM record plus public enrichment cache and produces `PreVisitDossier`. Process taxonomy uses `gemini-3.1-pro-preview`, N=1, `thinking_level="medium"`. Defect-class hypothesis uses the N=3 Flash ensemble plus conformal calibration. Comparable deployment, risk register, and suggested approach use Pro N=1 `thinking_level="low"` under fixed schemas. Citation-provenance validation runs before the sidecar writes the CRM note or attachment link.

Statefulness location: the CRM owns prospect state. The sidecar owns only `crm_event_ledger`, `signal_hash_cache`, `dossier_generation_runs`, and `knowledge_graph_version`. Idempotency keys are `(crm_provider, crm_object_id, crm_updated_at, changed_field_hash)` for lead updates and `(crm_object_id, signal_hash, knowledge_graph_version)` for dossiers. Graceful degradation: if CRM writeback fails, output goes to a retry queue and Slack fallback; if enrichment is partial, CRM fields explicitly show `partial`; if Vertex AI is unavailable, the CRM note says dossier queued, not failed.

## The Native Environment UI Spec.

The three-pane theater keeps the Vidyard pattern. Left pane is a Hubspot/Salesforce-style lead list after UK Metals Expo import. Rows include William Cook, Tata Steel, Ernest Wright, Centriblast, and Safran Seats GB. As the sidecar runs, the CRM fields fill in: score, vertical, reason, and "Generate dossier."

Center pane is the system theater with webhook event JSON, ADC route, CRM object ID, idempotency hash, worker state, N=3 Flash cards, conformal set, and citation validation. It must show that the CRM is the system of record and the sidecar is a typed adapter.

Right pane is the CRM record detail. The dossier appears as a CRM note with structured sections and a link to a rendered document. Cold-open timing: T+0 CRM webhook receives 124-lead import, T+10 list fields populate for top candidates, T+15 FDE toggles `Generate dossier`, T+30 taxonomy appears in note, T+45 conformal defect set, T+60 comparable deployment citation, T+80 full CRM note with suggested approach. The payoff is under 90 seconds.

## Phase 1 Execution Spec.

Repository structure:

```text
matta-refinery/
  apps/crm_refinery_api/
    routers/hubspot_webhook.py
    routers/salesforce_webhook.py
    routers/crm_actions.py
  apps/refinery_worker/tasks/
    normalize_crm_event.py
    prioritize_crm_batch.py
    writeback_crm_fields.py
    generate_crm_dossier.py
  packages/crm/
    base.py
    hubspot.py
    salesforce.py
    retry_outbox.py
  packages/schemas/crm.py
  packages/schemas/dossier.py
  packages/adc/rules.py
  apps/theater_ui/components/
    CRMLeftPane.tsx
    TheaterStatePane.tsx
    CRMRecordRightPane.tsx
```

Critical schemas:

```python
class CRMLeadSignal(BaseModel):
    model_config = ConfigDict(extra="forbid")
    provider: Literal["hubspot", "salesforce"]
    object_type: Literal["lead", "contact", "account"]
    object_id: str
    updated_at: datetime
    changed_fields: dict[str, str | int | float | None]
    source_label: str | None = None

class CRMWritebackEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    object_id: str
    fit_score: float = Field(..., ge=0, le=1)
    vertical: str
    dossier_url: str | None = None
    requires_human_review: bool
```

FastAPI contracts: webhooks validate provider signature, persist event ledger rows, compute idempotency key, and enqueue Celery tasks. `POST /crm/actions/generate-dossier` accepts a CRM object ID and returns a `DossierAck`. Workers use `task_acks_late=True`, `worker_prefetch_multiplier=1`, and provider writeback retries through a durable outbox.

Prompt templates are identical in reasoning structure to the Refinery but produce CRM-safe summaries. The comparable deployment prompt accepts only knowledge-graph anchors with verified `citation_substrate_line`. Mock data creates a CRM import event for `UK_Metals_Expo_2025` and a Salesforce custom action. Demo recording uses fake CRM UI, not live CRM credentials.

Magic Moment success criteria: CRM fields update without page change; top candidates visible within 10 seconds; dossier note complete within 90 seconds; duplicate webhook delivery creates one ledger entry and one writeback; all generated sections validate with `extra="forbid"`; citation line provenance is visible in the CRM note.

## Lateral-Specific Risk Register.

**Risk 1: CRM dependency slows the 72-hour demo.** Real Hubspot/Salesforce APIs can eat sprint time. Mitigation: build provider adapters against mocked fixtures first, then add one real sandbox only if credentials are available.

**Risk 2: Damjan sees CRM as a messy source of truth.** CRMs contain duplicates and stale fields. Mitigation: make source-of-truth explicit: CRM owns lead identity, sidecar owns only derived intelligence and event ledger. Conflicts go to `requires_human_review`.

**Risk 3: Doug worries CRM writeback creates operational noise.** Too many fields and notes can clutter sales workflow. Mitigation: write only four Stage 1 fields plus one dossier note, and allow per-batch dry-run mode before writeback.
