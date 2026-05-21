import React, { useState } from 'react';
import type { DemoPhase, DossierPayload, TopProspect } from '../hooks/useWebSocket';
import type { SeedCsv } from './seedCsvs';

interface Props {
  phase: DemoPhase;
  dossier: DossierPayload | null;
  activeCsv: SeedCsv;
  tracerProspect: TopProspect | null;
}

// §0 Company Facts — structured render distinguishing CSV-provided vs
// verified-public provenance buckets. The compose_dossier task emits
// company_facts with csv_provided_facts + verified_public_facts +
// ingest_provenance sub-dicts; the generic renderJsonValue would emit
// a deep nested mess. This component surfaces the provenance distinction
// explicitly so Damjan's "where does this come from" probe has a visible
// answer in the UI.
function renderEnrichmentBlock(label: string, block: unknown): React.ReactNode {
  if (!block || typeof block !== 'object') return null;
  const b = block as { status: string; data?: unknown; reason?: string };

  if (b.status === 'fetched' && b.data) {
    return (
      <div className="dossier-doc__enrich-source dossier-doc__enrich-source--fetched">
        <div className="dossier-doc__enrich-label">
          <span className="dossier-doc__enrich-source-name">{label}</span>
          <span className="dossier-doc__enrich-status dossier-doc__enrich-status--fetched">
            ✓ fetched
          </span>
        </div>
        {renderJsonValue(b.data)}
      </div>
    );
  }

  if (b.status === 'not_applicable') {
    return (
      <div className="dossier-doc__enrich-source dossier-doc__enrich-source--na">
        <span className="dossier-doc__enrich-source-name">{label}</span>
        <span className="dossier-doc__enrich-status dossier-doc__enrich-status--na">
          not applicable
        </span>
        <span className="dossier-doc__enrich-reason">
          {b.reason === 'non_uk_jurisdiction_heuristic'
            ? '(non-UK jurisdiction)'
            : b.reason}
        </span>
      </div>
    );
  }

  // fallback_empty / failed / not_attempted
  return (
    <div className="dossier-doc__enrich-source dossier-doc__enrich-source--empty">
      <span className="dossier-doc__enrich-source-name">{label}</span>
      <span className="dossier-doc__enrich-status dossier-doc__enrich-status--empty">
        no data
      </span>
      <span className="dossier-doc__enrich-reason">{b.reason}</span>
    </div>
  );
}

function renderCompanyFacts(facts: Record<string, unknown>): React.ReactNode {
  const csv = facts.csv_provided_facts as Record<string, string> | undefined;
  const verified = facts.verified_public_facts as Record<string, unknown> | undefined;
  const ingest = facts.ingest_provenance as Record<string, string> | undefined;

  return (
    <div className="dossier-doc__company-facts">
      <div className="dossier-doc__facts-header">
        <span className="dossier-doc__facts-name">
          {(facts.company_name as string) || '—'}
        </span>
        <span className="dossier-doc__facts-vertical">
          {(facts.vertical as string) || 'vertical_uncertain'}
        </span>
        <span className="dossier-doc__facts-size">
          {(facts.factory_size_band as string) || 'unknown'}
        </span>
      </div>

      {csv && (
        <div className="dossier-doc__facts-block dossier-doc__facts-block--csv">
          <div className="dossier-doc__facts-block-label">
            From the trade-show lead CSV
          </div>
          <dl className="dossier-kv">
            {csv.contact_name && <><dt>contact_name</dt><dd>{csv.contact_name}</dd></>}
            {csv.contact_email && <><dt>contact_email</dt><dd>{csv.contact_email}</dd></>}
            {csv.sector_hint && <><dt>sector_hint</dt><dd>{csv.sector_hint}</dd></>}
            {csv.raw_notes && <><dt>booth_notes</dt><dd>{csv.raw_notes}</dd></>}
          </dl>
        </div>
      )}

      {verified && (
        <div className="dossier-doc__facts-block dossier-doc__facts-block--verified">
          <div className="dossier-doc__facts-block-label">
            Verified from public sources
          </div>
          {renderEnrichmentBlock('Companies House', verified.companies_house)}
          {renderEnrichmentBlock('Website (scrape)', verified.website_capabilities)}
          {renderEnrichmentBlock('Recent news', verified.recent_news)}
        </div>
      )}

      {ingest && (
        <div className="dossier-doc__facts-block dossier-doc__facts-block--provenance">
          <details>
            <summary>Ingest provenance</summary>
            <dl className="dossier-kv">
              <dt>batch_id</dt><dd><code>{ingest.batch_id}</code></dd>
              <dt>file_sha256</dt><dd><code>{(ingest.file_sha256 || '').slice(0, 16)}…</code></dd>
              <dt>ingest_day</dt><dd>{ingest.ingest_day}</dd>
            </dl>
          </details>
        </div>
      )}
    </div>
  );
}

function renderJsonValue(value: unknown, depth = 0): React.ReactNode {
  if (value === null || value === undefined) return <span className="dossier-empty">—</span>;
  if (typeof value === 'string') return <span>{value}</span>;
  if (typeof value === 'number' || typeof value === 'boolean') return <span>{String(value)}</span>;
  if (Array.isArray(value)) {
    if (value.length === 0) return <span className="dossier-empty">[]</span>;
    return (
      <ul className="dossier-list">
        {value.slice(0, 6).map((v, i) => (
          <li key={i}>{renderJsonValue(v, depth + 1)}</li>
        ))}
        {value.length > 6 && <li className="dossier-more">+ {value.length - 6} more</li>}
      </ul>
    );
  }
  if (typeof value === 'object') {
    const entries = Object.entries(value as Record<string, unknown>);
    return (
      <dl className="dossier-kv">
        {entries.slice(0, 8).map(([k, v]) => (
          <React.Fragment key={k}>
            <dt>{k}</dt>
            <dd>{renderJsonValue(v, depth + 1)}</dd>
          </React.Fragment>
        ))}
      </dl>
    );
  }
  return <span>{String(value)}</span>;
}

// Stylized document corner icon — recognizable as "doc" without cloning Google
// Drive's exact trademark glyph. Two-tone: navy body + peach corner fold.
const DocumentIcon = () => (
  <svg
    className="drive-doc-icon"
    width="18"
    height="22"
    viewBox="0 0 18 22"
    fill="none"
    aria-hidden="true"
  >
    <path d="M2 0 L12 0 L18 6 L18 22 L2 22 Z" fill="#1F242C" />
    <path d="M12 0 L18 6 L12 6 Z" fill="#F2C2A5" />
    <rect x="4.5" y="10" width="9" height="1.3" fill="#FFFFFF" opacity="0.55" />
    <rect x="4.5" y="13" width="9" height="1.3" fill="#FFFFFF" opacity="0.55" />
    <rect x="4.5" y="16" width="6" height="1.3" fill="#FFFFFF" opacity="0.55" />
  </svg>
);

function nowTimestamp(): string {
  const d = new Date();
  const hh = d.getHours() % 12 || 12;
  const mm = d.getMinutes().toString().padStart(2, '0');
  const ap = d.getHours() >= 12 ? 'PM' : 'AM';
  return `${d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })}, ${hh}:${mm} ${ap}`;
}

export default function DriveDossierRightPane({ phase, dossier, activeCsv, tracerProspect }: Props) {
  const showWaiting =
    phase === 'idle' ||
    phase === 'ingesting' ||
    phase === 'stage1' ||
    phase === 'stage1_complete' ||
    phase === 'stage2_requesting';
  const hasContent = dossier !== null;
  const dossierCount = hasContent ? 1 : 0;

  const [lastModified, setLastModified] = useState<string | null>(null);
  React.useEffect(() => {
    if (hasContent && lastModified === null) {
      setLastModified(nowTimestamp());
    }
  }, [hasContent, lastModified]);

  return (
    <div className="drive-pane" data-tutorial-anchor="drive-pane">
      <div className="drive-pane__header" data-tutorial-anchor="drive-header">
        <DocumentIcon />
        <div className="drive-pane__title-block">
          <div className="drive-pane__title">Matta Pre-Visit Dossiers</div>
          <div className="drive-pane__breadcrumb">
            <span>My Drive</span>
            <span className="drive-pane__crumb-sep">›</span>
            <span>Matta</span>
            <span className="drive-pane__crumb-sep">›</span>
            <span>Pre-Visit Dossiers</span>
          </div>
        </div>
        <div className="drive-pane__count">
          {dossierCount} {dossierCount === 1 ? 'dossier' : 'dossiers'}
        </div>
      </div>

      {showWaiting && !hasContent && (
        <div className="drive-doc-paper drive-doc-paper--empty">
          <div className="drive-doc-paper__placeholder">
            <DocumentIcon />
            <div>Waiting for briefing generation…</div>
            <div className="drive-doc-paper__placeholder-sub">
              Click a prospect card in Slack to trigger Stage 2.
            </div>
          </div>
        </div>
      )}

      {hasContent && (
        <div className="drive-doc-paper" data-tutorial-anchor="dossier-doc">
          <div className="drive-doc-paper__sheet">
            <div className="dossier-doc__crm-strip" data-tutorial-anchor="crm-strip">
              CRM record · {tracerProspect?.company_name ?? activeCsv.tracerCompany}
              {' · '}fit {(tracerProspect?.fitness_score ?? 0.84).toFixed(2)}
              {' · '}vertical: metal_casting
              {' · '}slot_readiness: ready_for_dossier
              {' · '}dossier attached
            </div>
            <header className="dossier-doc__header">
              <div className="dossier-doc__role-label">
                FDE pre-flight briefing · read before factory visit
              </div>
              <h1
                className="dossier-doc__title"
                data-tutorial-anchor="dossier-title"
              >
                Matta Pre-Visit Dossier — William Cook Sheffield
              </h1>
              <div className="dossier-doc__meta">
                <span>Last modified: {lastModified ?? '—'}</span>
                <span className="dossier-doc__meta-sep">·</span>
                <span>KG phase1-v1</span>
                <span className="dossier-doc__meta-sep">·</span>
                <span>Calibration phase1-demo-v1</span>
                {typeof dossier?.deterministic_section_ratio === 'number' && (
                  <>
                    <span className="dossier-doc__meta-sep">·</span>
                    <span>Byte-density {dossier.deterministic_section_ratio.toFixed(3)}</span>
                  </>
                )}
              </div>
              <div className="dossier-doc__purpose">
                This briefing assembles verified public facts and inferred
                operational signals for FDE pre-deployment scoping. It does
                not replace on-site diagnostic work — it eliminates the
                night of unstructured prep that currently happens between
                the trade-show floor and the factory visit.
              </div>
            </header>

            {dossier?.company_facts ? (
              <section className="dossier-doc__section" data-doc-section="company_facts">
                <h3>§0 Company Facts</h3>
                {renderCompanyFacts(dossier.company_facts as Record<string, unknown>)}
              </section>
            ) : null}

            {dossier?.process_taxonomy ? (
              <section className="dossier-doc__section" data-doc-section="process_taxonomy">
                <h3>§1 Process Taxonomy</h3>
                <aside
                  className="dossier-doc__caveat"
                  data-section-caveat="phase1-scope"
                >
                  <div className="dossier-doc__caveat-label">Phase 1 scope</div>
                  <div className="dossier-doc__caveat-body">
                    §1 represents the verified{' '}
                    <code className="dossier-doc__inline-code">metal_casting</code>{' '}
                    baseline; company-specific enrichment (website scrape,
                    employee count, news mentions) is Phase 2 work. The
                    load-bearing sections — §3 Comparable Deployment,
                    §4 Risk Register, §5 Suggested Approach — are anchored
                    to verified Matta intel.
                  </div>
                </aside>
                {renderJsonValue(dossier.process_taxonomy)}
              </section>
            ) : null}

            {dossier?.defect_hypothesis ? (
              <section className="dossier-doc__section" data-doc-section="defect_hypothesis">
                <h3>§2 Defect Hypothesis (N=3 conformal)</h3>
                {(() => {
                  const d = dossier.defect_hypothesis as Record<string, unknown>;
                  const requiresReview = d?.requires_human_review === true;
                  const deferralReason = d?.deferral_reason as string | null | undefined;
                  const agreementScore = d?.inter_model_agreement_score as number | null | undefined;
                  if (requiresReview && deferralReason) {
                    return (
                      <aside
                        className="dossier-doc__deferral-banner"
                        data-doc-section="defect_deferral"
                      >
                        <div className="dossier-doc__deferral-label">
                          Model deferred — recommend human review
                        </div>
                        <div className="dossier-doc__deferral-body">
                          <strong>Reason:</strong> {String(deferralReason).replace(/_/g, ' ')}
                          {typeof agreementScore === 'number' && (
                            <>
                              {' · '}
                              <strong>Inter-model agreement:</strong>{' '}
                              <code>{agreementScore.toFixed(2)}</code>
                            </>
                          )}
                        </div>
                      </aside>
                    );
                  }
                  return null;
                })()}
                {renderJsonValue(dossier.defect_hypothesis)}
              </section>
            ) : null}

            {dossier?.comparable_deployment ? (
              <details
                className="dossier-doc__section dossier-doc__section--anchor dossier-doc__section--collapsible"
                data-tutorial-anchor="comparable-anchor"
                data-doc-section="comparable_deployment"
              >
                <summary className="dossier-doc__summary">
                  <h3>§3 Comparable Matta Deployment</h3>
                  <span className="dossier-doc__peek">verified KG anchor · click to expand</span>
                </summary>
                <div className="dossier-doc__anchor-tag">
                  Deterministic KG selection — LLM did not pick this anchor
                </div>
                {(() => {
                  const cmp = dossier.comparable_deployment as Record<string, unknown>;
                  const strength = cmp?.evidence_strength as string | null | undefined;
                  if (!strength) return null;
                  const FRAMING: Record<string, { label: string; note: string; tone: string }> = {
                    named_customer_specific_deployment: {
                      label: 'Named customer · specific application',
                      note: 'Verified deployment with a named customer and a named defect-detection application.',
                      tone: 'strong',
                    },
                    named_customer_oem_partnership: {
                      label: 'Named OEM partnership',
                      note: 'Verified OEM partnership; specific deployment scope still evolving.',
                      tone: 'medium',
                    },
                    unnamed_customer_quantitative_claim: {
                      label: 'Unnamed customer · quantitative claim',
                      note: 'Customer not publicly named; a quantitative performance figure is publicly stated.',
                      tone: 'medium',
                    },
                    unnamed_customer_vertical_mention: {
                      label: 'Vertical mention only',
                      note: 'Industry mention without customer identification — weakest grounding.',
                      tone: 'weak',
                    },
                  };
                  const f = FRAMING[strength];
                  if (!f) return null;
                  return (
                    <div
                      className={`dossier-doc__evidence-band dossier-doc__evidence-band--${f.tone}`}
                      data-evidence-strength={strength}
                    >
                      <div className="dossier-doc__evidence-label">{f.label}</div>
                      <div className="dossier-doc__evidence-note">{f.note}</div>
                    </div>
                  );
                })()}
                {renderJsonValue(dossier.comparable_deployment)}
              </details>
            ) : null}

            {dossier?.risk_register ? (
              <details
                className="dossier-doc__section dossier-doc__section--collapsible"
                data-doc-section="risk_register"
              >
                <summary className="dossier-doc__summary">
                  <h3>§4 Integration Risk Register</h3>
                  <span className="dossier-doc__peek">risk pillars · click to expand</span>
                </summary>
                {renderJsonValue(dossier.risk_register)}
              </details>
            ) : null}

            {dossier?.suggested_approach ? (
              <details
                className="dossier-doc__section dossier-doc__section--collapsible"
                data-doc-section="suggested_approach"
              >
                <summary className="dossier-doc__summary">
                  <h3>§5 Suggested Approach</h3>
                  <span className="dossier-doc__peek">phased plan · click to expand</span>
                </summary>
                {renderJsonValue(dossier.suggested_approach)}
              </details>
            ) : null}

            {dossier?.unverified_sections && dossier.unverified_sections.length > 0 && (
              <div className="dossier-doc__unverified">
                Sections requiring human review: {dossier.unverified_sections.join(', ')}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
