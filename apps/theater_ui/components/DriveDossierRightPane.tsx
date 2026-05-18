import React, { useState } from 'react';
import type { DemoPhase, DossierPayload } from '../hooks/useWebSocket';

interface Props {
  phase: DemoPhase;
  dossier: DossierPayload | null;
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

export default function DriveDossierRightPane({ phase, dossier }: Props) {
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
            <header className="dossier-doc__header">
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
            </header>

            {dossier?.company_facts ? (
              <section className="dossier-doc__section" data-doc-section="company_facts">
                <h3>§0 Company Facts</h3>
                {renderJsonValue(dossier.company_facts)}
              </section>
            ) : null}

            {dossier?.process_taxonomy ? (
              <section className="dossier-doc__section" data-doc-section="process_taxonomy">
                <h3>§1 Process Taxonomy</h3>
                {renderJsonValue(dossier.process_taxonomy)}
              </section>
            ) : null}

            {dossier?.defect_hypothesis ? (
              <section className="dossier-doc__section" data-doc-section="defect_hypothesis">
                <h3>§2 Defect Hypothesis (N=3 conformal)</h3>
                {renderJsonValue(dossier.defect_hypothesis)}
              </section>
            ) : null}

            {dossier?.comparable_deployment ? (
              <section
                className="dossier-doc__section dossier-doc__section--anchor"
                data-tutorial-anchor="comparable-anchor"
                data-doc-section="comparable_deployment"
              >
                <div className="dossier-doc__anchor-tag">
                  Deterministic KG selection — LLM did not pick this anchor
                </div>
                <h3>§3 Comparable Matta Deployment</h3>
                {renderJsonValue(dossier.comparable_deployment)}
              </section>
            ) : null}

            {dossier?.risk_register ? (
              <section className="dossier-doc__section" data-doc-section="risk_register">
                <h3>§4 Integration Risk Register</h3>
                {renderJsonValue(dossier.risk_register)}
              </section>
            ) : null}

            {dossier?.suggested_approach ? (
              <section className="dossier-doc__section" data-doc-section="suggested_approach">
                <h3>§5 Suggested Approach</h3>
                {renderJsonValue(dossier.suggested_approach)}
              </section>
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
