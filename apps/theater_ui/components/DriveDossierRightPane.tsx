import React from 'react';
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

export default function DriveDossierRightPane({ phase, dossier }: Props) {
  const showWaiting = phase === 'idle' || phase === 'ingesting' || phase === 'stage1' || phase === 'stage1_complete' || phase === 'stage2_requesting';
  const hasContent = dossier !== null;

  return (
    <div className="drive-pane" data-tutorial-anchor="drive-pane">
      <div className="drive-pane__header" data-tutorial-anchor="drive-header">
        <span className="drive-pane__icon">📄</span>
        <span className="drive-pane__breadcrumb">Drive · Matta Pre-Visit Dossiers</span>
      </div>

      {showWaiting && !hasContent && (
        <div className="drive-pane__waiting">Waiting for Stage 2 …</div>
      )}

      {hasContent && (
        <div className="dossier-doc" data-tutorial-anchor="dossier-doc">
          <h1 className="dossier-doc__title">
            Matta Pre-Visit Dossier — William Cook Sheffield
          </h1>
          <div className="dossier-doc__meta">
            <span>KG: phase1-v1</span>
            <span className="dossier-doc__meta-sep">·</span>
            <span>Calibration: phase1-demo-v1</span>
            {typeof dossier?.deterministic_section_ratio === 'number' && (
              <>
                <span className="dossier-doc__meta-sep">·</span>
                <span>Byte-density ratio: {dossier.deterministic_section_ratio.toFixed(3)}</span>
              </>
            )}
          </div>

          {dossier?.company_facts ? (
            <section className="dossier-doc__section">
              <h3>§0 Company Facts</h3>
              {renderJsonValue(dossier.company_facts)}
            </section>
          ) : null}

          {dossier?.process_taxonomy ? (
            <section className="dossier-doc__section">
              <h3>§1 Process Taxonomy</h3>
              {renderJsonValue(dossier.process_taxonomy)}
            </section>
          ) : null}

          {dossier?.defect_hypothesis ? (
            <section className="dossier-doc__section">
              <h3>§2 Defect Hypothesis (N=3 conformal)</h3>
              {renderJsonValue(dossier.defect_hypothesis)}
            </section>
          ) : null}

          {dossier?.comparable_deployment ? (
            <section
              className="dossier-doc__section dossier-doc__section--anchor"
              data-tutorial-anchor="comparable-anchor"
            >
              <div className="dossier-doc__anchor-tag">
                Deterministic KG selection — LLM did not pick this anchor
              </div>
              <h3>§3 Comparable Matta Deployment</h3>
              {renderJsonValue(dossier.comparable_deployment)}
            </section>
          ) : null}

          {dossier?.risk_register ? (
            <section className="dossier-doc__section">
              <h3>§4 Integration Risk Register</h3>
              {renderJsonValue(dossier.risk_register)}
            </section>
          ) : null}

          {dossier?.suggested_approach ? (
            <section className="dossier-doc__section">
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
      )}
    </div>
  );
}
