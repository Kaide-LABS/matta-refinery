import React from 'react';
import type { DemoPhase, Stage2Progress } from '../hooks/useWebSocket';

interface Props {
  phase: DemoPhase;
  elapsedSec: number;
  batchId: string | null;
  dossierId: string | null;
  stage2Progress: Stage2Progress;
  byteDensityRatio: number | null;
  error: string | null;
  onRunDemo: () => void;
  onReset: () => void;
}

function fmtElapsed(sec: number): string {
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return `${m}:${s.toString().padStart(2, '0')}`;
}

const SECTION_LABELS: Record<keyof Stage2Progress, string> = {
  process_taxonomy: 'Process Taxonomy',
  defect_hypothesis: 'Defect Hypothesis (N=3 conformal)',
  comparable_deployment: 'Comparable Matta Deployment',
  risk_register: 'Integration Risk Register',
  suggested_approach: 'Suggested Approach',
};

const SECTION_ORDER: (keyof Stage2Progress)[] = [
  'process_taxonomy',
  'defect_hypothesis',
  'comparable_deployment',
  'risk_register',
  'suggested_approach',
];

export default function TheaterCenterPane({
  phase,
  elapsedSec,
  batchId,
  dossierId,
  stage2Progress,
  byteDensityRatio,
  error,
  onRunDemo,
  onReset,
}: Props) {
  const idle = phase === 'idle';
  const ingesting = phase === 'ingesting';
  const stage1 = phase === 'stage1';
  const stage1Done = phase === 'stage1_complete';
  const stage2Active = phase === 'stage2_requesting' || phase === 'stage2';
  const done = phase === 'complete';
  const errored = phase === 'error';

  return (
    <div className="theater-pane">
      <div className="theater-pane__header">
        <h2 className="theater-pane__title">Theater Console</h2>
        {!idle && (
          <div className="theater-pane__elapsed">T+{fmtElapsed(elapsedSec)}</div>
        )}
      </div>

      {idle && (
        <div className="theater-cta">
          <button
            className="btn btn-primary"
            onClick={onRunDemo}
            type="button"
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

      {(stage1 || stage1Done || stage2Active || done) && batchId && (
        <div className="theater-section">
          <div className="theater-section__label">ADC Route</div>
          <div className="adc-pill">PRIORITIZATION</div>

          <div className="theater-section__label" style={{ marginTop: 12 }}>
            Idempotency
          </div>
          <code className="theater-mono">batch:{batchId.slice(0, 8)}…</code>
        </div>
      )}

      {stage1 && (
        <div className="theater-section">
          <div className="theater-section__heading">
            Stage 1 — Deep Ensemble Scoring
          </div>
          <div className="theater-progress">
            <div className="theater-progress__bar">
              <div
                className="theater-progress__fill"
                style={{ width: `${Math.min(100, (elapsedSec / 300) * 100)}%` }}
              />
            </div>
            <div className="theater-progress__label">
              Classifying vertical · scoring fit · 124 leads × N=3
            </div>
          </div>
        </div>
      )}

      {stage1Done && !stage2Active && !done && (
        <div className="theater-section theater-section--moment">
          <div className="theater-section__heading">Magic Moment 1 fired</div>
          <div className="theater-section__body">
            Top 12 ranked · Slack canvas, CRM fields, Drive priority index updated.
            Click a prospect card to generate the full briefing.
          </div>
        </div>
      )}

      {(stage2Active || done) && dossierId && (
        <div className="theater-section">
          <div className="theater-section__heading">
            Stage 2 — William Cook Briefing
          </div>
          <code className="theater-mono">dossier:{dossierId.slice(0, 8)}…</code>
          <ul className="section-list">
            {SECTION_ORDER.map((s) => {
              const state = stage2Progress[s];
              return (
                <li key={s} className={`section-row section-row--${state}`}>
                  <span className="section-row__indicator">
                    {state === 'complete' ? '✓' : state === 'active' ? '●' : '○'}
                  </span>
                  <span className="section-row__name">{SECTION_LABELS[s]}</span>
                </li>
              );
            })}
          </ul>
        </div>
      )}

      {byteDensityRatio !== null && (
        <div className="theater-section">
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
        <div className="theater-section theater-section--moment">
          <div className="theater-section__heading">Magic Moment 2 fired</div>
          <div className="theater-section__body">
            Briefing materialized across Slack canvas, CRM note, and Drive document.
            Total elapsed {fmtElapsed(elapsedSec)}.
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
    </div>
  );
}
