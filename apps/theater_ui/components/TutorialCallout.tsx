import React, { useEffect, useMemo, useRef, useState } from 'react';
import type { DemoPhase, Stage2Progress } from '../hooks/useWebSocket';

interface Props {
  phase: DemoPhase;
  elapsedSec: number;
  stage2Progress: Stage2Progress;
  byteDensityRatio: number | null;
}

// Each step is keyed to a derived demo-state condition rather than a wallclock
// timer, so the callout never drifts out of sync with what's actually on
// screen. The 'derive' function picks one step per render — the active step.
// Each step also carries an array of CSS selectors pointing at the DOM
// element(s) the callout is referring to; those elements receive a
// `.tutorial-target` class while the step is active and lose it on transition.
interface Step {
  id: string;
  title: string;
  body: string;
  targets: string[];
}

function fmtElapsed(sec: number): string {
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return `${m}:${s.toString().padStart(2, '0')}`;
}

function deriveStep(
  phase: DemoPhase,
  elapsedSec: number,
  stage2: Stage2Progress,
  ratio: number | null
): Step {
  if (phase === 'idle') {
    return {
      id: 'idle',
      title: 'Start the demo',
      body:
        '124 UK Metals Expo leads arrived in Slack. Click Run Demo to ingest them. The Refinery will score fit, rank the top 12, and route them across Slack, the CRM, and Drive — simultaneously.',
      targets: ['[data-tutorial-anchor="run-demo"]', '[data-tutorial-anchor="csv-attachment"]'],
    };
  }
  if (phase === 'ingesting') {
    return {
      id: 'ingesting',
      title: 'Uploading the batch',
      body: 'CSV posted to /ingest/batch with idempotency-keyed Postgres write. ADC routes to PRIORITIZATION — Stage 1 is about to fan out.',
      targets: [],
    };
  }
  if (phase === 'stage1') {
    return {
      id: 'stage1',
      title: 'Stage 1 — deep-ensemble scoring in flight',
      body: `Each lead runs through an N=3 ensemble for vertical classification, followed by deterministic fit scoring against the calibrated weights. ~5 minutes for 124 leads. Elapsed: ${fmtElapsed(elapsedSec)}.`,
      targets: [],
    };
  }
  if (phase === 'stage1_complete') {
    return {
      id: 'm3',
      title: 'Stage 1 complete — top 12 ranked',
      body: 'Slack, CRM, and Drive updated in one Postgres transaction via the outbox. Click any prospect card to generate the full briefing.',
      targets: [
        '[data-tutorial-anchor="slack-shortlist"]',
        '[data-tutorial-anchor="crm-inset"]',
        '[data-tutorial-anchor="drive-header"]',
        '[data-tutorial-anchor="stage1-complete"]',
        '[data-tutorial-anchor="prospect-anchor"]',
      ],
    };
  }
  if (phase === 'stage2_requesting') {
    return {
      id: 'm4',
      title: 'Stage 2 dispatched',
      body: 'Slack-style click handler accepted. Refinery generated a dossier_id and enqueued the William Cook briefing. Five sections will render in order.',
      targets: [],
    };
  }
  if (phase === 'stage2') {
    if (stage2.suggested_approach === 'active') {
      return {
        id: 'm9',
        title: 'Approach template',
        body: 'Suggested approach assembling: two-camera pilot scaffold with deterministic phase breakdown (kickoff, shadow, parallel, handoff).',
        targets: ['[data-section="suggested_approach"]'],
      };
    }
    if (stage2.risk_register === 'active') {
      return {
        id: 'm8',
        title: 'Integration risk register',
        body: 'Each risk tied to a pillar (infrastructure, environmental, compliance) with severity score and a verbatim knowledge-graph anchor — no free-form LLM speculation.',
        targets: ['[data-section="risk_register"]'],
      };
    }
    if (stage2.comparable_deployment === 'active' || stage2.comparable_deployment === 'complete') {
      return {
        id: 'm7',
        title: 'Comparable deployment — deterministic anchor',
        body: 'The comparable Matta deployment is selected by the knowledge-graph selector, not the LLM. The LLM writes prose against that anchor. This is the load-bearing safety rail.',
        targets: ['[data-section="comparable_deployment"]', '[data-tutorial-anchor="comparable-anchor"]'],
      };
    }
    if (stage2.defect_hypothesis === 'active') {
      return {
        id: 'm6',
        title: 'Defect hypothesis — N=3 conformal',
        body: 'Three independent samples at temperatures 0.1 / 0.5 / 0.9, then a conformal-coverage gate at ≥0.90. The hypothesis only ships if the ensemble agrees within calibration.',
        targets: ['[data-section="defect_hypothesis"]'],
      };
    }
    if (stage2.process_taxonomy === 'active') {
      return {
        id: 'm5',
        title: 'Process taxonomy',
        body: 'First section rendering — extracting the process geometry (casting type, pour temperature, geometry class) from the verified facts in the knowledge graph.',
        targets: ['[data-section="process_taxonomy"]'],
      };
    }
    return {
      id: 'stage2-generic',
      title: 'Stage 2 in flight',
      body: 'Five briefing sections rendering. Each section is Pydantic-validated against extra="forbid"; the byte-density gate at the end enforces deterministic content ≥0.60 of the bytes.',
      targets: [],
    };
  }
  if (phase === 'complete') {
    const ratioCopy =
      ratio !== null ? ` Byte-density ratio: ${ratio.toFixed(3)} (floor 0.60).` : '';
    return {
      id: 'm12',
      title: 'Briefing ready',
      body: `The dossier shipped to all three surfaces in one Postgres transaction — no half-states. Total elapsed ${fmtElapsed(elapsedSec)}.${ratioCopy} Reset to run again.`,
      targets: [
        '[data-tutorial-anchor="slack-shortlist"]',
        '[data-tutorial-anchor="crm-inset"]',
        '[data-tutorial-anchor="dossier-doc"]',
        '[data-tutorial-anchor="dossier-complete"]',
      ],
    };
  }
  if (phase === 'error') {
    return {
      id: 'error',
      title: 'Something went wrong',
      body: 'The Refinery hit an error. Reset the demo and try again, or check the API health endpoint at :8080/health.',
      targets: [],
    };
  }
  return { id: 'unknown', title: '', body: '', targets: [] };
}

const ALL_STEP_IDS = [
  'idle',
  'ingesting',
  'stage1',
  'm3',
  'm4',
  'm5',
  'm6',
  'm7',
  'm8',
  'm9',
  'm12',
];

const HIGHLIGHT_CLASS = 'tutorial-target';

export default function TutorialCallout({
  phase,
  elapsedSec,
  stage2Progress,
  byteDensityRatio,
}: Props) {
  const [dismissed, setDismissed] = useState(false);
  const [prevStepId, setPrevStepId] = useState<string | null>(null);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const highlightedRef = useRef<Element[]>([]);

  const step = useMemo(
    () => deriveStep(phase, elapsedSec, stage2Progress, byteDensityRatio),
    [phase, elapsedSec, stage2Progress, byteDensityRatio]
  );

  // ─── Apply / remove .tutorial-target class on the step's targets ────────
  // Runs whenever the active step changes OR the dismissed flag changes (so
  // dismissing the callout also clears any active highlights). The cleanup
  // function strips the class before the next effect run, keeping the DOM
  // tidy across step transitions.
  useEffect(() => {
    if (dismissed || step.targets.length === 0) {
      return;
    }
    // Collect matching elements (selectors are stable; querySelectorAll runs
    // against the current DOM, which by this point in the effect lifecycle
    // includes any newly-rendered section cards).
    const elements: Element[] = [];
    step.targets.forEach((selector) => {
      const matches = document.querySelectorAll(selector);
      matches.forEach((el) => elements.push(el));
    });
    elements.forEach((el) => el.classList.add(HIGHLIGHT_CLASS));
    highlightedRef.current = elements;
    return () => {
      highlightedRef.current.forEach((el) => el.classList.remove(HIGHLIGHT_CLASS));
      highlightedRef.current = [];
    };
  }, [step.id, step.targets, dismissed]);

  // Trigger a fade transition when the step id changes
  useEffect(() => {
    if (prevStepId === null) {
      setPrevStepId(step.id);
      return;
    }
    if (prevStepId !== step.id) {
      setIsTransitioning(true);
      const t = window.setTimeout(() => {
        setIsTransitioning(false);
        setPrevStepId(step.id);
      }, 350);
      return () => window.clearTimeout(t);
    }
  }, [step.id, prevStepId]);

  // Step counter — best-effort, based on a fixed ordering of likely steps
  const stepIndex = ALL_STEP_IDS.indexOf(step.id);
  const stepNumber = stepIndex >= 0 ? stepIndex + 1 : null;
  const stepTotal = ALL_STEP_IDS.length;

  if (dismissed) return null;
  if (!step.title) return null;

  return (
    <aside
      className={`tutorial-callout ${isTransitioning ? 'tutorial-callout--fading' : ''}`}
      role="status"
      aria-live="polite"
    >
      <div className="tutorial-callout__header">
        <span className="tutorial-callout__tag">Guided demo</span>
        <button
          className="tutorial-callout__close"
          aria-label="Dismiss tutorial"
          onClick={() => setDismissed(true)}
          type="button"
        >
          ×
        </button>
      </div>
      <div className="tutorial-callout__body">
        <h3 className="tutorial-callout__title">{step.title}</h3>
        <p className="tutorial-callout__text">{step.body}</p>
      </div>
      {stepNumber !== null && (
        <div className="tutorial-callout__progress">
          <span className="tutorial-callout__progress-text">
            Step {stepNumber} of {stepTotal}
          </span>
          <div className="tutorial-callout__progress-bar">
            <div
              className="tutorial-callout__progress-fill"
              style={{ width: `${(stepNumber / stepTotal) * 100}%` }}
            />
          </div>
        </div>
      )}
    </aside>
  );
}
