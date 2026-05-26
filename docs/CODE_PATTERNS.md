# Code patterns watchlist

Living notes on patterns we have intentionally chosen, patterns we have
intentionally avoided, and historical bugs that taught us why.

## "Returns bool, caller try/excepts"

The Phase 1.7 Stage E audit surfaced a critical instance:
`packages/adapters/slack/signature.py:verify()` returned `False` on
signature failure instead of raising. The callers in
`apps/refinery_api/routers/slack_{events,interactions}.py` wrapped the
call in `try/except Exception` and discarded the return value, so
unsigned POSTs passed through authentication.

Fix: `signature.verify()` now raises `SlackSignatureError` on any
failure; the routers catch the explicit exception type and return 401.

**Rule for new code:** when a function's failure mode matters, prefer
raising a typed exception over returning `False`/`None`. Bool returns
are appropriate only for true predicates (`is_uk_prospect`,
`has_pending_writes`) where the caller already branches on the value.

**Pattern audit (Stage E sweep):**
- `packages/adapters/slack/signature.verify` — **FIXED** (now raises).
- `packages/knowledge_graph/verify.validate_graph_or_die` — already
  raises `KnowledgeGraphProvenanceError`; safe.
- `packages/enrichment/companies_house.CompaniesHouseEnricher.is_uk_prospect`
  — true predicate, caller (`enrich` method line 58) checks the bool
  with `if not ...`; safe.
- `packages/outbox/dispatcher.dispatch_outbox_row` — does not return a
  status; commits to DB and raises on adapter failure; safe.
- `packages/ingest/csv_parser.parse_csv_to_batch` — raises
  `ValueError` / Pydantic `ValidationError` on bad input; safe.

No other instances of the pattern at the time of this audit.

## "Check-then-act without lock" (TOCTOU)

The Phase 1.7 Stage E audit surfaced an instance in
`apps/refinery_api/startup_prebake.py`: a SELECT-then-INSERT on
`ingest_batches` with no locking, racing under multi-replica boot.

Fix: wrap the check-and-insert in a single transaction with
`pg_advisory_xact_lock` keyed on `hash(file_sha256 + user_id)`. Lock
auto-releases on commit.

**Rule for new code:** any "check whether X exists, then create X if
not" sequence that crosses replicas must either run under an advisory
lock or use `INSERT ... ON CONFLICT DO NOTHING` with a unique
constraint. Read-then-write without coordination is a bug under
concurrency.

## "Manual JSON parsing after structured-output API"

The Phase 1.7 Stage E audit surfaced this in every
`apps/refinery_worker/tasks/dossier_section_*.py`:

```python
json_str = text[text.find('{'):text.rfind('}')+1] if '{' in text else text
```

— defensive brace-extraction inside a call that already specifies
`response_mime_type="application/json"` and `response_schema=...`. The
brace-search masked schema mismatches and turned them into 8-retry
loops with identical bad input.

Fix: pass `response.text` directly to `model_validate_json`. Pydantic
parse errors propagate honestly to Celery's autoretry.

**Rule for new code:** if you're using a structured-output API, trust
its contract. If you don't trust it, log the raw response and raise —
don't paper over.
