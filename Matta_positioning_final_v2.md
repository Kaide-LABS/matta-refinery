# Matta Brief Architecture — 1F-red Verdict (v2)

## Verdict

**REPOSITION-REQUIRED.**

The pre-sales scoping bottleneck **category** survives the audit substantively — and survives more strongly than the prior 1F-red captured, once Gemini's missed primary-source evidence is restored. The Brief's architectural **form** (stateless, mobile, in-the-moment, 60-second-at-the-booth, lead-capture-flavored) does not survive. The reshape to a stateful, asynchronous, desktop-anchored, deep-research-flavored, pipeline-prioritization-aware sidecar is required.

The recommended form is **Form C — The Refinery**, a stateful sidecar with two output modes that operate over a shared underlying pipeline: (Stage 1) deployment-capacity-aware prioritization queue ingesting trade-show lead lists and waitlist signals, and (Stage 2) on-demand pre-visit dossier generation for the FDE-bound subset. Stage 2 is the demoed Magic Moment; Stage 1 is the verbal tail tease. Justification for selecting C over A or B is in the Form Selection section.

The orchestration spine from `ULTIMATE_PRD.md` continues to transfer at approximately 70%. The schemas, ADC routing rules, demo theater, and knowledge graph all change. The N=3 deep ensemble, conformal prediction set, parallel verifier, durable outbox, Pydantic `extra="forbid"` posture, and Vertex AI europe-west4 pinning carry forward unchanged.

## Verification Findings

Direct verification of the load-bearing quote claims, run against `Matta_Intel_cleaned.md` line-by-line. Gemini's audit had three significant primary-source misses that materially affect the verdict mechanics, though not the directional conclusion.

**Multi-year waitlist quote (load-bearing).** Verified verbatim. Lines 114 and 267, both from Doug's $14M funding announcement post (10/12/25 and 11/12/25 — same post, dual indexing in the substrate): *"we're deploying to around two factories a month and have a multi-year waitlist at the moment – so do reach out and let's see how we can dramatically improve your processes with industrial AI."* Gemini cited this correctly. The quote is the strongest single anchor in the audit and survives the verification pass intact.

**"100s of factories in the pipeline" quote.** Verified verbatim, but misframed by Gemini. Lines 106 and 248. The quote IS Doug's, but it appears in a hiring post (Forward Deployed Engineer JD), not a sales-pipeline post. The next sentence is *"if you are exceptional… we will take you."* The substantive conclusion (massive pipeline volume) holds independently from the multi-year-waitlist quote, so the misframing does not cascade. Note for SOP: Gemini's citation hygiene was sloppy here. Flag.

**Advanced Engineering 2025 trade-show post.** Verified verbatim. Line 284: *"What a start to Advanced Engineering 2025! ⚙️🔥 Day one was a blast - we met over 100 incredible leads from across the manufacturing world… Here's a peek at the action at Booth P198."* Tagged: Doug, Daniel Crimp, Sebastian Pattinson, Bonnie Zhang, Jake Moll, Tom Walker, Ollie Rosen, Damjan Denic, Christos Margadji, Matthew Judge — ten team members including both founders and the CTO. **This is a primary-source miss by Gemini.** Gemini's Claim 1 audit explicitly searched for "MACH 2026" and "Southern Manufacturing" and concluded *"complete absence of empirical evidence supporting the trade-show hypothesis."* The substrate contradicts that conclusion at line 284 (Advanced Engineering 2025), line 187/191 (MACH 2026 — *"come find us on the Matta stand (17-121)… industrial AI chat with Damjan Denic, Carmelo del Coso Ameijide, and Douglas Brion"*), line 234/393 (Southern Manufacturing & Electronics 2026 — *"It also marks one year since our very first trade show (Southern last year)"*), and line 294 (UK Metals Expo Sept 2025 — *"We clocked 124 leads in two days, putting us in the top 5% of exhibitors"*). Four trade shows in twelve months. Doug and Damjan personally attend MACH 2026. Trade shows are not the absent vector Gemini described — they are a verified, founder-attributed, twelve-month-old, named-customer-disclosing acquisition channel.

**Cummins as "hallucinated entity" claim.** Partially refuted. Lines 200, 210, 212–214, 321, 331, 338–340, 345 — Cummins Inc. (specifically Steven Grace, Automation & Technology Leader, and Jonathan Wood, VP-CTO, Cummins Europe) attended the Matta-hosted "Sentient Factories" event at the Royal Academy of Engineering. Steven Grace was on the Matta-organized panel. Cummins is in Matta's verified relationship/event graph. **However**, Cummins is not in the verified deployment footprint — the verbatim deployment list is Bowers & Wilkins, Caracol AM, polymer manufacturing (unnamed customer), metal casting, bottling (the "global drinks brand"), consumer electronics. Gemini's specific framing ("Cummins is hallucinated") is wrong; Gemini's structural concern (using Cummins as a "comparable Matta deployment" anchor in the knowledge graph is not deployment-evidence-grounded) is correct. The implication for the demo: using "Cummins" or a Cummins-adjacent entity as a demo-target name is grounded and safe (Doug knows Cummins, hosted Cummins, has a relationship). Using Cummins as a "comparable deployment pattern" anchor in the dossier output is not safe.

**"Global drinks brand" quote.** Verified verbatim. Lines 540 and 600, both from Matta funding press materials: *"Recent projects range from inspecting high-speed bottling for defects with a global drinks brand to working with Bowers & Wilkins, where Matta's AI rapidly measures speaker components to catch issues before assembly."* **This is a second primary-source miss by Gemini.** The audit flagged this as "Not Verified (Implicit)" — incorrect. The exact phrase is in the substrate.

**FDE JD trade-show responsibilities.** Verified verbatim. Lines 698, 704, 705, 716. The FDE role JD names trade-show responsibilities four times: *"be the face of Matta, interfacing with prospective customers at trade shows"* (698), *"engaging prospective customers, qualifying leads, scoping problems"* (704), *"One week, you'll be the face of Matta, responsible for engaging with engineers and technicians at trade shows, bringing in leads alongside our CEO, Doug (and keeping him on track!). You'll leverage your understanding of our customer's challenges, to qualify and validate their interest in the Matta product."* (705), *"travel (~10-20% time) to trade shows and customers"* (716). **Gemini's audit did not surface any of this.** The Brief_Audit.md focuses entirely on the Special Projects/Chief of Staff JD and never quotes the FDE JD on trade-show or lead-qualification language. This is the third primary-source miss.

**Sebastian's uncertainty-quantification rigor.** Verified. Doug's Cambridge thesis pedigree, Sebastian's Nature Communications 2022 paper on closed-loop neural-network correction, and the substrate's references to "nuclear submarines, waterproof coats and even gourmet cheese" deployment surface confirm the regulated-environment risk-aversion claim. Gemini's Claim 2 use of this evidence holds.

**Special Projects/Chief of Staff Gandalf framing.** Verified verbatim. Line 262 (Doug's Chief of Staff hiring post): *"Think Gandalf: the person who quietly works their magic behind the scenes, making sure everything runs smoothly."* Plus line 625 (Special Projects JD): *"steering long-term strategy, supporting fundraising efforts, and helping close customer deals… probably our most important hire."* Gemini's Claim 4 use of this evidence holds. (Note: the role appears to have been posted as both "Chief of Staff" and "Special Projects" — same role, two titles. Either label is supportable in outreach.)

**Net.** Gemini's directional verdict (escalate, reshape required) is correct. Gemini's audit methodology has three primary-source misses (trade-show evidence, "global drinks brand" verbatim, Cummins-in-relationship-graph) that would have softened the Claim 1 and Claim 3 framings substantially. None of those misses recover the original Brief shape, because the form-axis problems (stateless vs stateful, mobile vs desktop, in-the-moment vs asynchronous, lookup vs deep research) are independently load-bearing and survive the corrections.

## Justification

The category-vs-form distinction holds, and it holds harder than the original 1F-red captured.

The category — pre-sales scoping consuming founder, FDE, and Special Projects/Chief-of-Staff hours — is supported by four independent verbatim sources: the multi-year-waitlist quote (Doug, funding post), the FDE JD trade-show language (four separate verbatim references), the Chief of Staff "Gandalf" JD (Doug, hiring post), and the trade-show post-event summaries (124 leads at UK Metals Expo, 100+ at Advanced Engineering 2025, full team tagged at MACH 2026 and Southern Manufacturing 2026). Pre-sales scoping is real, current, founder-attributed, and quantifiable. The category survives the audit by a wide margin.

The form fails because four independent form-axes all collapse under primary-source pressure. (1) Stateful vs stateless: a multi-year waitlist with two-deployments-per-month capacity is by construction a stateful pipeline problem; the prospects sit in queue for months or years before deployment. A stateless sidecar that resets after every interaction cannot model that pipeline. (2) Asynchronous vs in-the-moment: the FDE workflow is "trade show one week, factory deployment the next." The bottleneck sits BETWEEN those two weeks — in the post-show triage and pre-visit prep windows — not in the booth conversation itself. (3) Desktop vs mobile: 124 leads from UK Metals Expo are processed via CSV/Hubspot/Salesforce on a desktop, not via Slack-on-phone at the booth. (4) Deep research vs lookup: Sebastian's verbatim uncertainty-quantification rigor and Doug's nuclear-submarine/aerospace-deployment surface are incompatible with collapsing technical scoping to 60 seconds. All four form-axes point in the same direction; the booth-anchored framing is wrong on every one.

The 1F-sim simulation against Damjan fires cleanly. Damjan reads the cold email at minute 0, sees "60-second pre-call brief, for Hannover and beyond," and within five minutes notes the architectural mismatch: the vendor is optimizing speed at the top of the funnel for a company whose actual constraint is downstream — *which 6 of the 100 leads from last week's show, and which 24 of the 400+ in the multi-year waitlist, do we move into deployment slots this quarter*. He archives. Gemini's implicit 1F-sim signal — *"Matta is actively managing an overwhelming asynchronous pipeline, deploying highly complex physical AI infrastructure into strictly regulated environments"* — fires as a contradiction in his read because the substrate genuinely supports it. This is not Damjan being uncharitable; this is the architecture proposing the wrong end of the pipeline.

## Form Selection

**Form C — The Refinery.** A stateful, asynchronous, desktop-anchored sidecar with two output modes operating over a shared underlying pipeline: Stage 1 (deployment-capacity-aware prioritization queue) and Stage 2 (on-demand pre-visit dossier per FDE-bound deployment). Stage 2 is the demoed Magic Moment in the Vidyard. Stage 1 is the verbal tail tease.

Form A (Pipeline Triage Sidecar in isolation) and Form B (Pre-Deployment Dossier Sidecar in isolation) each fit the verified operational reality, but each has a thin failure mode that Form C resolves. Form A's risk is the strategic-decision ego check: a sidecar that ranks Matta's deployment queue can be perceived as overreaching into territory Doug and Damjan reserve for their own judgment (Caracol OEM partnership status, B&W reference-customer continuity, capacity scheduling against existing FDE travel calendars). Damjan's likely challenge: "We have a Notion doc for this, what does your sidecar know that we don't." Form A survives that challenge but with a thin margin. Form B's risk is the build-vs-buy commodification challenge: deep-research artifact generation is a contested vendor category (Clay, Crystal, ZoomInfo Engage, GPT-Researcher startups) and a bespoke sidecar built around six manufacturing verticals × five defect classes is structurally small enough that Damjan's team could plausibly assemble equivalent capability in a sprint. Damjan's likely challenge: "Why not Clay plus a Cursor agent." Form B survives that challenge but more thinly than Form A.

Form C addresses both weaknesses by combining them. Stage 1 supplies a deployment-capacity-aware prioritization signal that pure data-enrichment vendors cannot produce (Clay does not know Matta's deployment cadence or current FDE travel roster). Stage 2 inherits Stage 1's prioritization signal as input, which means the dossier-generation step is operating on a triaged subset rather than spraying enrichment across the whole pipeline. Stage 1 retains its strategic-decision-respect posture by surfacing CANDIDATES with structured rationale, not making decisions — the FDE team controls which dossiers to actually generate. The two stages share the same orchestration spine (ADC routing, N=3 ensemble, conformal calibration, Pydantic envelopes, durable outbox), so Form C is structurally one product with two output modes, not two products jammed together. Build cost is roughly Form B's cost plus a small Stage-1 prioritization layer, well within the 72-hour sprint envelope given the orchestration spine reuse.

The chosen demo theater (Stage 2) is the more visceral output. Showing a ranked list (Stage 1) is harder to make visually magic in 60 seconds than showing a deep dossier materializing on screen. The verbal tail tease at video end ("there's an upstream prioritization layer that ingests your raw trade-show CSVs and produces the queue feeding into this") is structurally identical to the prior version's Phase 2 tail tease and uses the verbal-only adjacent-idea mechanic from the Identity manifesto.

## Positioning Edits

### FDE Thesis

The Refinery is a stateful pre-deployment intelligence sidecar that absorbs the post-trade-show, pre-FDE-deployment scoping load currently distributed across Doug, the FDE team, and the incoming Special Projects/Chief of Staff hire. It ingests trade-show lead lists (CSV/Hubspot/Salesforce export) and inbound waitlist signals, produces a continuously evolving prioritization queue against Matta's two-deployments-per-month capacity, and on-demand generates pre-visit dossiers for the leads that promote into FDE deployment slots. It operates strictly upstream of any factory deployment — it never reads from a Matta camera, agent, foundation model, factory OS surface, or edge firmware. It exists between the trade-show floor and the factory visit, not at either endpoint.

### Magic Moment

The FDE clicks "generate dossier" on the top-ranked candidate from their prioritization queue (e.g., a forging plant from UK Metals Expo, or a polymer line from Advanced Engineering). Sixty to ninety seconds later, a structured eight-page artifact materializes on their desktop: process taxonomy, likely defect classes with conformal sets, comparable Matta deployment patterns drawn from the verified deployment surface (B&W speaker components for precision-machining contexts, Caracol AM for additive contexts, polymer manufacturing for extrusion contexts, bottling for high-speed F&B contexts), integration risk register (legacy CMM infrastructure, lighting variance, network topology, EMF environment), suggested approach. The visceral demo is artifact depth — the document the FDE reads on the flight to the factory the next morning. Explicitly NOT "60 seconds at the booth." The Magic Moment is depth and structure, not speed.

### Sebastian Readiness Check

> The Refinery operates entirely upstream of any factory deployment — it consumes public corporate data, your verified deployment patterns from your published case studies, and the trade-show lead intake your team already collects, then produces formatted intelligence for your FDEs to read before a factory visit. The architecture has zero shared signal path with the closed-loop control work disclosed in your 2022 Nature Communications paper; The Refinery never reads from a Matta camera, an agent emission, or a foundation-model output. Its conformal calibration on defect-class hypotheses respects the uncertainty-quantification posture you've publicly insisted on — when the model is unsure, the dossier says so explicitly rather than hallucinating a confident defect taxonomy.

### Damjan Readiness Check

> You absolutely could build this in-house — a senior FDE plus an MLE plus a manufacturing-vertical knowledge graph plus the prioritization scoring layer plus the deep-research orchestration, call it three to four months and ongoing maintenance for the knowledge graph and scoring rules. We've already built it; you'd have it running against a CSV export from Hubspot or a Salesforce webhook in under two weeks, with the orchestration patterns documented as a reference architecture your team can absorb when the bandwidth fits. The £10k/month is structured against the deployment-slot cost — your two-a-month cadence makes each deployment slot worth a meaningful slice of ARR, and a Refinery-improved deployment-target selection that earns a single Cummins-class commitment pays the year.

### Demo theater (left pane / center pane / right pane)

**Left pane:** Replaced. Booth simulation is dropped. The new left pane is a desktop screen showing a trade-show lead intake — a CSV preview of `UK_Metals_Expo_2025_leads.csv` with 124 rows, file dropped into the Refinery dashboard. Stylized Hubspot-style UI overlay. (Production cost: lower than the trade-show booth simulation; uses Tailwind on a stock SaaS layout.)

**Center pane:** Architecturally identical to the prior version. The pipeline visualization (ingress → ADC → N=3 ensemble → conformal calibration → parallel verifier → narrative generation → outbox → ack) is the same. Schemas and demo data change. The center pane shows two routing paths in the ADC — one for prioritization requests (Stage 1), one for dossier requests (Stage 2). The demo run exercises Stage 2 with a single dossier generation; Stage 1's queue is visible as static data in the left pane to anchor the workflow context.

**Right pane:** Replaced. The Slack mobile mock is dropped. The new right pane is a Notion-style or PDF-preview document panel showing the dossier materializing section by section — process taxonomy first, then defect-class hypothesis with conformal interval, then comparable-deployment section, then integration risk register, then suggested approach. Cost ticker bottom-right, ticks under ten cents per dossier. (Production cost: roughly the same as the Slack mobile mock; standard React/Tailwind document component.)

If a secondary screen is needed for the verbal tail tease at video end, use a 3-second freeze-frame of the prioritization queue from Stage 1 — sourced as the Refinery's own UI mock, not invented external collateral. Visual reference only, not a working demo. Keeps the Stage 1 option open without committing the build.

### Why-video script (~95 seconds)

```
[0:00–0:08]  COLD OPEN — silent. Desktop screen.
             CSV file "UK_Metals_Expo_2025_leads.csv"
             with 124 rows visible. Cursor drags the
             file into the Refinery dashboard.

[0:08–0:18]  SILENT — Refinery's prioritization queue
             materializes. 124 raw leads → ranked list
             with fit scores against Matta's two-a-month
             deployment cadence. Top candidate visible:
             a forging plant from UK Metals Expo.
             FDE clicks "generate dossier."

[0:18–0:35]  DOSSIER MATERIALIZES — document scrolls on
             screen section by section. Process taxonomy.
             Likely defect classes (porosity, dimensional
             drift, surface inclusions) with conformal
             sets. Comparable Matta deployment: polymer
             extrusion case study. Integration risk:
             legacy CMM, lighting variance. Suggested
             approach.

[0:35–0:55]  VOICEOVER (Hafeedh) — "What you just watched
             is The Refinery — a stateful sidecar that
             takes the lead lists you collect at trade
             shows and the inbound signals from your
             waitlist, scores them against your two-a-month
             deployment capacity, and on-demand generates
             pre-visit dossiers for the leads that promote
             into FDE deployment slots. Stateful.
             Asynchronous. Desktop-anchored. Built around
             your actual deployment cadence."

[0:55–1:15]  TECHNICAL WALKTHROUGH — three-pane theater.
             Show the deterministic Action Domain
             Classifier routing prioritization vs dossier
             requests. Show the N=3 Gemini Pro ensemble
             running with conformal calibration on the
             defect-class hypothesis. Show the Pydantic
             schema validation. Cost ticker — under ten
             cents per dossier.

[1:15–1:30]  THE FDE JD CITATION — "Your FDE JD names
             trade-show qualification, lead validation,
             and pre-deployment scoping in the
             responsibilities. The Refinery absorbs the
             slice of that load that today happens between
             the show floor and the factory visit."

[1:30–1:35]  TAIL TEASE (verbal only) — "There's an
             upstream prioritization layer that ingests
             your raw trade-show CSVs and produces the
             queue feeding into the dossier generator.
             Happy to walk that through on a call."

[1:35]       SIGN-OFF.
```

### Cold email — Subject line

`The Refinery: pre-visit dossier sidecar, for Matta's deployment cadence`

### Cold email — Doug's tagged line

> Doug — your team has been on the trade-show calendar all year (UK Metals Expo, Advanced Engineering 2025, MACH 2026, Southern Manufacturing 2026), and the FDE JD makes pre-deployment scoping and lead qualification an explicit part of the role. We built a thing that turns a trade-show lead list — say the 124 you brought back from UK Metals Expo — into a triaged queue against your two-a-month deployment capacity, and generates a deep pre-visit dossier on the leads your team promotes. Built for the work that happens between the show floor and the factory visit, not at either endpoint.

### Cold email — Damjan's tagged line

> Damjan — stateful sidecar, FastAPI ingress, Pydantic everywhere with `extra="forbid"`, deterministic rules engine for the routing decision (no LLM in the load-bearing path), N=3 Gemini Pro ensemble with conformal prediction sets for the defect-class inference, durable outbox so a queued dossier ships even when an FDE drops connectivity in transit. CSV in, structured artifact out. Reference architecture you can read; absorbable in-house when the bandwidth fits.

### Cold email — CTA

> 95-second video at the link — skip to 0:18 if you want the magic moment first, technical walkthrough follows. If the architecture lands, 15 minutes to scope. If not, no follow-up from me.

## Phase 1 Build Implications

### Schema changes (PHASE_1_SPEC.md needs revision)

`MattaDefectEvent` is replaced by `LeadIntakeBatch` (CSV ingest envelope: lead rows with company name, contact, sector hints, trade-show provenance) and `LeadProspect` (per-lead enriched envelope post-Stage-1 scoring). `RootCauseHypothesis` becomes `LikelyDefectClassHypothesis` with the same structural shape (categorical enum, conformal set, confidence band) but a different domain (defect classes for the inferred manufacturing process type). `CMMSWorkOrder` is replaced by `PreVisitDossier` — a structured Pydantic envelope with sections for process taxonomy, defect-class hypothesis, comparable Matta deployment patterns (drawn ONLY from verified deployment surface — Bowers & Wilkins, Caracol AM, polymer manufacturing, metal casting, bottling, consumer electronics; never relationship-edge entities like Cummins), integration risk register, suggested approach.

### Action Domain Classifier rules

Rewritten for two-route discrimination. Route 1: prioritization request (input is `LeadIntakeBatch`, output is `PrioritizedQueue`). Route 2: dossier request (input is a single `LeadProspect`, output is a single `PreVisitDossier`). The deterministic mapping is `(request_type, payload_shape, vertical_keyword) → route_path`. Default route on no-match: `requires_human_review = True`, queued for manual triage.

### Knowledge graph

The six-vertical macro-structure (polymer extrusion, metal casting, additive manufacturing, F&B bottling, electronics assembly, aerospace) holds. Per Gemini's Claim 3 verdict (which holds even after my methodology corrections), the load-bearing entity-level anchors must be cleaned up. Specifically: `Cummins` is removed from any "comparable deployment" anchor (it's a relationship-graph entity, not a deployment-graph entity); the demo-target name of "Cummins Daventry plant" can be retained for the Why-Video because Doug knows Cummins via the RAE event. `global drinks brand` is retained as a deployment-pattern anchor for the F&B bottling vertical because it IS verbatim in the funding press materials. `aerospace composites` is replaced with a broader `aerospace` vertical anchor that includes plane wings, titanium alloys, and metallurgy contexts to avoid the rigid-ontology vulnerability Gemini flagged. The knowledge graph file remains a small hand-built JSON (six verticals, five defect classes each, with citation provenance for each anchor pointing back to a verbatim line in `Matta_Intel_cleaned.md`); approximately eight hours of curation work, two hours longer than the prior version because the citation-provenance pass is now mandatory.

### Demo theater

Per the Demo Theater section above. Left-pane and right-pane mocks are both replaced. Center pane is structurally identical. Production cost is roughly equivalent to the prior version (lower-cost SaaS UI mocks replace a stock-footage-trade-show mock and a Slack-mobile mock).

### Architecture preserved (no changes needed)

The N=3 Gemini ensemble pattern, the conformal prediction set computation, the parallel Stage 2.5 verifier fan-out, the Pydantic `extra="forbid"` posture, the Vertex AI europe-west4 pinning, the deterministic-routing-over-LLM-routing principle, the deep-ensembles voiceover disclaimer, the Damjan idempotency primitives — all transfer unchanged.

### Sprint impact

72-hour sprint envelope holds. Schema rewrite, demo theater change, knowledge-graph citation-provenance pass, and Stage 1 prioritization scoring layer net to roughly the same total work as the original Brief schema change, given that the orchestration spine ports across cleanly. The Vidyard recording flow is unchanged in structure (cold open, technical walkthrough, verbal tail tease) — only the on-screen content changes. Cold-email subject and tagged lines redrafted; structural shape unchanged.

### Outreach delivery sequencing

Cold email CTA links to a Vidyard timestamped to the Magic Moment (0:18). Verbal Phase 2 tease at 1:30 references the upstream prioritization layer (Stage 1). If Doug or Damjan asks about it on the discovery call, Stage 1 is ready to scope as a Phase 2 engagement after Stage 2 proves itself. The dormant CMMS Bridge architecture remains a deeper Phase 3 verbal-only adjacent idea if a third call materializes.

## Meta-Observation for Hafeedh

This is the second mid-sprint architectural-form falsification on Matta inside the same sprint cycle. The pattern across CMMS Bridge → Brief → Refinery is consistent: the FORM-axis problems (stateful vs stateless, mobile vs desktop, in-the-moment vs asynchronous, lookup vs deep research) survived the Step 1A → 1B Master PRD writing process and only died at the 1F or 1F-lite audit gate. Both architectures had verbatim primary-source contradictions of their form-axes already present in the cleaned intel substrate at the time the Master PRD was written. This suggests the four form-axes are a candidate for promotion to the Step 1D divergent-generation gate as an explicit per-axis primary-source justification check, BEFORE the Master PRD is committed. Each of the four binary axes would require a verbatim citation defending the proposed direction. On the Brief, that pre-1B check would have caught the form mismatch before resources were spent on the 1B PRD and the orchestration spine schema work. Secondary observation, smaller weight: Gemini's audit methodology has a consistent retrieval gap (verbatim-present-in-substrate evidence not surfaced — three misses on this audit, one on the prior CMMS Bridge audit). 1F/1F-lite gates may benefit from requiring per-claim line-citations rather than summary verdicts, which would make Gemini's retrieval gaps visible to the audit consumer rather than requiring the consumer to re-derive primary sources. Both observations are SOP-iteration questions, not part of the v2 positioning artifact. Carrying them into the strategy thread for sprint-meta discussion separately.

---

*End of Matta_positioning_final_v2.md. Audit trail preserved: Matta_positioning_final.md (the prior CMMS Bridge kill verdict and Brief proposal) is unchanged.*
