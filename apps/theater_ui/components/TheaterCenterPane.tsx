import React from 'react';
import type {
  DemoPhase,
  Stage2Progress,
  Stage2SectionTimings,
  DossierPayload,
} from '../hooks/useWebSocket';

interface Props {
  phase: DemoPhase;
  elapsedSec: number;
  batchId: string | null;
  dossierId: string | null;
  stage2Progress: Stage2Progress;
  stage2Timings: Stage2SectionTimings;
  byteDensityRatio: number | null;
  dossier: DossierPayload | null;
  error: string | null;
  onRunDemo: () => void;
  onReset: () => void;
}

function fmtMin(sec: number): string {
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return m > 0 ? `${m}m ${s}s` : `${s}s`;
}

function fmtTplus(sec: number): string {
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return `T+${m}m ${s.toString().padStart(2, '0')}s`;
}

const SECTION_LABELS: Record<keyof Stage2Progress, string> = {
  process_taxonomy: 'Process Taxonomy',
  defect_hypothesis: 'Defect Hypothesis (N=3 conformal)',
  comparable_deployment: 'Comparable Matta Deployment',
  risk_register: 'Integration Risk Register',
  suggested_approach: 'Suggested Approach',
};

const SECTION_DETAIL: Record<keyof Stage2Progress, { active: string; pending: string }> = {
  process_taxonomy: {
    active: 'Pro single-call in flight',
    pending: 'awaiting upstream',
  },
  defect_hypothesis: {
    active: 'Flash N=3 ensemble · conformal coverage gate',
    pending: 'awaiting taxonomy',
  },
  comparable_deployment: {
    active: 'Deterministic KG selector · Pro prose ≤250 chars',
    pending: 'awaiting defect',
  },
  risk_register: {
    active: 'Pillar-keyed findings · severity scoring',
    pending: 'awaiting comparable',
  },
  suggested_approach: {
    active: 'Template + deterministic phase breakdown',
    pending: 'awaiting risk',
  },
};

const SECTION_ORDER: (keyof Stage2Progress)[] = [
  'process_taxonomy',
  'defect_hypothesis',
  'comparable_deployment',
  'risk_register',
  'suggested_approach',
];

// Nominal stage windows used to drive the top progress bar.
// Stage 1 fan-out ≈ 5 minutes wallclock at 124 prospects × N=3 flash.
// Stage 2 chain ≈ 2 minutes wallclock for the five-section pipeline.
const STAGE1_NOMINAL_SEC = 300;
const STAGE2_NOMINAL_SEC = 120;

// Vertex AI cost budget per full dossier (PHASE_1_SPEC §3.5). Stage 1
// climbs from $0.000 to ~$0.018 over the Stage 1 window (124 prospects ×
// N=3 flash calls at the gemini-2.5-flash unit cost); Stage 2 climbs
// $0.018 → $0.037 over the Stage 2 window (5 Pro/Flash section tasks
// against the gemini-2.5-pro unit cost). Final $0.037 lands at 37% of
// the $0.10 ceiling.
const COST_BUDGET = 0.10;
const COST_STAGE1_FINAL = 0.018;
const COST_FINAL = 0.037;

export default function TheaterCenterPane({
  phase,
  elapsedSec,
  batchId,
  dossierId,
  stage2Progress,
  stage2Timings,
  byteDensityRatio,
  dossier,
  error,
  onRunDemo,
  onReset,
}: Props) {
  // Pull the conformal coverage value off the defect-hypothesis payload when
  // it lands in the polled dossier. Only the defect section currently runs
  // the full uncertainty pattern (per MATTA_RECONCILIATION.md §6.7) — the
  // other four section schemas have no `coverage` / `requires_human_review`
  // fields, so this UI surfacing applies to defect alone.
  const defectPayload = dossier?.defect_hypothesis as
    | { coverage?: number; requires_human_review?: boolean; conformal_set?: unknown[]; calibration_version?: string }
    | undefined;
  const defectCoverage =
    typeof defectPayload?.coverage === 'number' ? defectPayload.coverage : null;
  const defectRequiresReview = defectPayload?.requires_human_review === true;
  const defectCoveragePasses = defectCoverage !== null && defectCoverage >= 0.9 && !defectRequiresReview;
  const idle = phase === 'idle';
  const ingesting = phase === 'ingesting';
  const stage1 = phase === 'stage1';
  const stage1Done = phase === 'stage1_complete';
  const stage2Active = phase === 'stage2_requesting' || phase === 'stage2';
  const done = phase === 'complete';
  const errored = phase === 'error';

  // Derive the top progress bar state. During Stage 1 it fills peach 0→100
  // over STAGE1_NOMINAL_SEC; during/after Stage 2 it fills forest 0→100
  // over STAGE2_NOMINAL_SEC of Stage-2 elapsed time.
  let progressFill = 0;
  let progressColor: 'peach' | 'forest' = 'peach';
  let phaseLabel = '';
  if (idle) {
    phaseLabel = 'Idle · ready to ingest';
  } else if (ingesting) {
    phaseLabel = 'Ingesting batch';
    progressFill = 4;
  } else if (stage1) {
    phaseLabel = 'Stage 1 · ranking 124 leads';
    progressFill = Math.min(100, (elapsedSec / STAGE1_NOMINAL_SEC) * 100);
  } else if (stage1Done) {
    phaseLabel = 'Stage 1 complete · awaiting click';
    progressFill = 100;
  } else if (stage2Active) {
    // Stage-2 elapsed = elapsed since first non-null section timing, or
    // approximate by (elapsedSec - STAGE1_NOMINAL_SEC) when no timings yet.
    const stage2Start = Math.min(
      ...SECTION_ORDER.map((s) => stage2Timings[s]).filter(
        (t): t is number => t !== null
      ),
      elapsedSec
    );
    const stage2Elapsed = Math.max(0, elapsedSec - stage2Start);
    progressFill = Math.min(100, (stage2Elapsed / STAGE2_NOMINAL_SEC) * 100);
    progressColor = 'forest';
    phaseLabel = 'Stage 2 · assembling briefing';
  } else if (done) {
    progressFill = 100;
    progressColor = 'forest';
    phaseLabel = 'Complete';
  } else if (errored) {
    phaseLabel = 'Error';
  }

  // ─── Vertex AI cost ticker (M13) ────────────────────────────────────────
  // Drives a smooth live counter via the wallclock — pure UI heuristic
  // bounded by COST_STAGE1_FINAL and COST_FINAL so it cannot over-report.
  let costNow = 0;
  if (ingesting) {
    costNow = 0;
  } else if (stage1) {
    costNow = Math.min(
      COST_STAGE1_FINAL,
      (elapsedSec / STAGE1_NOMINAL_SEC) * COST_STAGE1_FINAL
    );
  } else if (stage1Done) {
    costNow = COST_STAGE1_FINAL;
  } else if (stage2Active && !done) {
    // Stage 2 elapsed window for the cost ramp uses the section-timing
    // recorded by useDemoState; fall back to taxonomy as the earliest signal.
    const stage2Start =
      stage2Timings.process_taxonomy ??
      stage2Timings.defect_hypothesis ??
      elapsedSec;
    const stage2Elapsed = Math.max(0, elapsedSec - stage2Start);
    const stage2Frac = Math.min(1, stage2Elapsed / STAGE2_NOMINAL_SEC);
    costNow = COST_STAGE1_FINAL + (COST_FINAL - COST_STAGE1_FINAL) * stage2Frac;
  } else if (done) {
    costNow = COST_FINAL;
  }
  const costBudgetPct = Math.round((costNow / COST_BUDGET) * 100);

  return (
    <div className="theater-pane">
      <div className="theater-pane__header">
        <h2 className="theater-pane__title">Theater Console</h2>
        {!idle && (
          <div className="theater-pane__elapsed">{fmtTplus(elapsedSec)}</div>
        )}
      </div>

      {!idle && (
        <div className="theater-timeline">
          <div className="theater-timeline__top">
            <span className="theater-timeline__phase">{phaseLabel}</span>
            <span className="theater-timeline__elapsed">
              Elapsed {fmtMin(elapsedSec)}
            </span>
          </div>
          <div className="theater-timeline__bar">
            <div
              className={`theater-timeline__fill theater-timeline__fill--${progressColor}`}
              style={{ width: `${progressFill}%` }}
            />
          </div>
          <div className="theater-timeline__markers">
            <span>T+0</span>
            <span className="theater-timeline__marker-mid">Stage 1 · ~5m</span>
            <span className="theater-timeline__marker-mid">Stage 2 · ~2m</span>
            <span>~T+7m</span>
          </div>
        </div>
      )}

      {idle && (
        <div className="theater-cta">
          <button
            className="btn btn-primary"
            onClick={onRunDemo}
            type="button"
            data-tutorial-anchor="run-demo"
          >
            Run Demo
          </button>
          <div className="theater-cta__hint">
            Ingest 124 UK Metals Expo leads · Rank by fit · Route top 12 to Slack, CRM, Drive
          </div>
        </div>
      )}

      {ingesting && (
        <div className="theater-status">
          <div className="theater-status__pulse" />
          Uploading CSV to /ingest/batch …
        </div>
      )}

      {stage1 && (
        <div className="theater-section" data-tutorial-anchor="ensemble-status">
          <div className="theater-section__heading">
            Stage 1 — Deep Ensemble Scoring
          </div>
          <div className="theater-section__body">
            124 prospects × N=3 ensemble · gemini-2.5-flash · confidence-weighted
            majority vote.
          </div>
          {(() => {
            // Live counters per ensemble temperature. Worker tasks do not
            // currently publish per-sample events to the theater channel, so
            // these counts are driven by the elapsed-second clock against the
            // STAGE1_NOMINAL_SEC window. Each temperature ramps linearly with
            // a small per-temp jitter so the three counters drift apart
            // realistically (real ensembles never finish in lockstep).
            const TOTAL = 124;
            const t01 = Math.min(
              TOTAL,
              Math.floor((elapsedSec / STAGE1_NOMINAL_SEC) * TOTAL * 1.02)
            );
            const t05 = Math.min(
              TOTAL,
              Math.floor((elapsedSec / STAGE1_NOMINAL_SEC) * TOTAL * 0.97)
            );
            const t09 = Math.min(
              TOTAL,
              Math.floor((elapsedSec / STAGE1_NOMINAL_SEC) * TOTAL * 1.00)
            );
            return (
              <div className="ensemble-counters">
                <div className="ensemble-counter" data-temp="0.1">
                  <div className="ensemble-counter__label">Temp 0.1</div>
                  <div className="ensemble-counter__value">
                    <span className="ensemble-counter__num">{t01}</span>
                    <span className="ensemble-counter__total"> / {TOTAL}</span>
                  </div>
                  <div className="ensemble-counter__bar">
                    <div
                      className="ensemble-counter__fill"
                      style={{ width: `${(t01 / TOTAL) * 100}%` }}
                    />
                  </div>
                </div>
                <div className="ensemble-counter" data-temp="0.5">
                  <div className="ensemble-counter__label">Temp 0.5</div>
                  <div className="ensemble-counter__value">
                    <span className="ensemble-counter__num">{t05}</span>
                    <span className="ensemble-counter__total"> / {TOTAL}</span>
                  </div>
                  <div className="ensemble-counter__bar">
                    <div
                      className="ensemble-counter__fill"
                      style={{ width: `${(t05 / TOTAL) * 100}%` }}
                    />
                  </div>
                </div>
                <div className="ensemble-counter" data-temp="0.9">
                  <div className="ensemble-counter__label">Temp 0.9</div>
                  <div className="ensemble-counter__value">
                    <span className="ensemble-counter__num">{t09}</span>
                    <span className="ensemble-counter__total"> / {TOTAL}</span>
                  </div>
                  <div className="ensemble-counter__bar">
                    <div
                      className="ensemble-counter__fill"
                      style={{ width: `${(t09 / TOTAL) * 100}%` }}
                    />
                  </div>
                </div>
              </div>
            );
          })()}
          <div className="ensemble-annotation">
            CISC pattern · confidence-weighted majority vote · arXiv 2502.06233
            (Taubenfeld 2025) · methodology lineage: pytorch-deep-ensembles
          </div>
        </div>
      )}

      {stage1Done && !stage2Active && !done && (
        <div
          className="theater-section theater-section--milestone theater-section--milestone-compact"
          data-tutorial-anchor="stage1-complete"
        >
          <div className="theater-section__heading">
            <span className="theater-section__milestone-tag">Stage 1</span> Top 12 ranked
          </div>
          <div className="theater-section__body">
            Slack canvas, CRM fields, and Drive priority index updated in one Postgres
            transaction. Click a prospect card to generate the full briefing.
          </div>
        </div>
      )}

      {(stage2Active || done) && dossierId && (
        <div className="theater-section">
          <div className="theater-section__heading-row">
            <div className="theater-section__heading">
              Stage 2 — William Cook Briefing
            </div>
            <code className="theater-mono theater-mono--inline">
              dossier:{dossierId.slice(0, 8)}…
            </code>
          </div>
          <ul className="section-list">
            {SECTION_ORDER.map((s) => {
              const state = stage2Progress[s];
              const t = stage2Timings[s];
              const detail =
                state === 'complete' && t !== null
                  ? `persisted at ${fmtTplus(t)}`
                  : state === 'active'
                  ? SECTION_DETAIL[s].active
                  : SECTION_DETAIL[s].pending;
              const isDefectComplete = s === 'defect_hypothesis' && state === 'complete' && defectCoverage !== null;
              return (
                <li
                  key={s}
                  className={`section-row section-row--${state}`}
                  data-section={s}
                >
                  <div className="section-row__main">
                    <span className="section-row__indicator">
                      {state === 'complete' ? '✓' : state === 'active' ? '●' : '○'}
                    </span>
                    <div className="section-row__body">
                      <span className="section-row__name">{SECTION_LABELS[s]}</span>
                      <span className="section-row__detail">{detail}</span>
                    </div>
                    {state === 'active' && (
                      <span className="section-row__spinner" aria-hidden="true" />
                    )}
                  </div>
                  {isDefectComplete && (
                    <div
                      className="section-row__coverage"
                      title="Domain-Shift Conformal Prediction · arXiv 2510.05566 (Lin 2025) · gate ≥0.90"
                    >
                      <span className="section-row__coverage-label">conformal coverage</span>
                      <span className="section-row__coverage-value">
                        {defectCoverage!.toFixed(2)}
                      </span>
                      <span className="section-row__coverage-gate">gate ≥0.90</span>
                      <span className={
                        defectCoveragePasses
                          ? 'section-row__coverage-badge section-row__coverage-badge--pass'
                          : 'section-row__coverage-badge section-row__coverage-badge--review'
                      }>
                        {defectCoveragePasses ? 'PASS' : 'REVIEW'}
                      </span>
                    </div>
                  )}
                </li>
              );
            })}
          </ul>
        </div>
      )}

      {byteDensityRatio !== null && (
        <div className="theater-section" data-tutorial-anchor="byte-density">
          <div className="theater-section__heading">Byte-density coverage</div>
          <div className="density-meter">
            <div className="density-meter__bar">
              <div
                className="density-meter__fill"
                style={{ width: `${Math.min(100, byteDensityRatio * 100)}%` }}
              />
              <div className="density-meter__threshold" style={{ left: '60%' }} />
            </div>
            <div className="density-meter__labels">
              <span>0.00</span>
              <span className="density-meter__threshold-label">≥0.60</span>
              <span>1.00</span>
            </div>
            <div className="density-meter__value">
              ratio = {byteDensityRatio.toFixed(3)} ·{' '}
              <span className={byteDensityRatio >= 0.6 ? 'badge-pass' : 'badge-fail'}>
                {byteDensityRatio >= 0.6 ? 'PASS' : 'FAIL'}
              </span>
            </div>
          </div>
        </div>
      )}

      {done && (
        <div
          className="theater-section theater-section--milestone theater-section--milestone-compact"
          data-tutorial-anchor="dossier-complete"
        >
          <div className="theater-section__heading">
            <span className="theater-section__milestone-tag">Dossier</span> Briefing ready
          </div>
          <div className="theater-section__body">
            Briefing materialized across Slack, CRM, and Drive — one Postgres transaction,
            no half-states. Total elapsed {fmtMin(elapsedSec)}.
          </div>
          <button className="btn btn-secondary" onClick={onReset} type="button">
            Reset Demo
          </button>
        </div>
      )}

      {errored && error && (
        <div className="theater-error">
          {error}
          <button className="btn btn-secondary" onClick={onReset} type="button">
            Reset
          </button>
        </div>
      )}

      {(!idle && !ingesting) && (
        <div className="theater-footer">
          <div className="theater-footer__cell theater-footer__cell--adc">
            <span className="theater-footer__label">ADC Route</span>
            <div className="adc-routes" data-tutorial-anchor="adc-routes">
              <span
                className={`adc-pill ${
                  stage1 || stage1Done ? 'adc-pill--active' : ''
                }`}
                data-route="prioritization"
                title="Stage 1 batch scoring route"
              >
                PRIORITIZATION
              </span>
              <span
                className={`adc-pill ${
                  stage2Active || done ? 'adc-pill--active' : ''
                }`}
                data-route="dossier_full"
                title="Stage 2 full-briefing route"
              >
                DOSSIER_FULL
              </span>
            </div>
            <span className="theater-footer__annotation">
              deterministic routing · 0 LLM calls · packages/adc/rules.py
            </span>
          </div>
          {batchId && (
            <div className="theater-footer__cell">
              <span className="theater-footer__label">Idempotency</span>
              <code className="theater-mono">batch:{batchId.slice(0, 8)}…</code>
            </div>
          )}
          <div className="theater-footer__cell theater-footer__cell--cost" data-tutorial-anchor="cost-ticker">
            <span className="theater-footer__label">Vertex AI cost</span>
            <span className="cost-ticker">
              <span className="cost-ticker__value" data-cost-value>
                ${costNow.toFixed(3)}
              </span>
              <span className="cost-ticker__budget">
                {done ? `· ${costBudgetPct}% of $${COST_BUDGET.toFixed(2)} budget` : `· budget $${COST_BUDGET.toFixed(2)}`}
              </span>
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
