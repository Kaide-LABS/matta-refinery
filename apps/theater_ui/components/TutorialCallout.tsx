import React, { ReactNode, useEffect, useMemo, useRef, useState } from 'react';
import type { DemoPhase, Stage2Progress } from '../hooks/useWebSocket';

interface Props {
  phase: DemoPhase;
  elapsedSec: number;
  stage2Progress: Stage2Progress;
  byteDensityRatio: number | null;
  tracerName: string | null;
}

interface TutorialStep {
  id: string;
  title: string;
  body: ReactNode;
  isMainStep: boolean;
  counterLabel?: string;
  targets: string[];
  // matches(props) === true when the demo state should auto-advance to this step.
  // Bridges (isMainStep=false) return false here — they are only reachable
  // manually or via a brief bridge-override timer keyed to a phase transition.
  matches?: (p: Props) => boolean;
}

function fmtElapsed(sec: number): string {
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return `${m}:${s.toString().padStart(2, '0')}`;
}

function buildStepArray(p: Props): TutorialStep[] {
  const tracer = p.tracerName ?? 'the rank-1 prospect';
  const ratioCopy = p.byteDensityRatio !== null ? p.byteDensityRatio.toFixed(3) : '—';

  return [
    {
      id: 'idle',
      isMainStep: true,
      title: 'Why this demo exists',
      targets: ['[data-tutorial-anchor="run-demo"]', '[data-tutorial-anchor="csv-attachment"]'],
      matches: (x) => x.phase === 'idle',
      body: (
        <>
          <p>
            Trade-show leads sit unranked for days. Refinery scores them, briefs
            the top 12, and updates Slack, HubSpot, and Drive in one pass —
            without your team leaving the tools they already use.
          </p>
          <p>Click Run Demo to start.</p>
        </>
      ),
    },
    {
      id: 'ingesting',
      isMainStep: true,
      title: 'Step 1 of 10 — ingest',
      targets: [],
      matches: (x) => x.phase === 'ingesting',
      body: (
        <p>
          65 leads landing in Postgres. Routing decision is deterministic Python
          — no LLM in the path you can grep at packages/adc/rules.py.
        </p>
      ),
    },
    {
      id: 'stage1',
      isMainStep: true,
      title: 'Step 2 of 10 — temperature-varied ensemble scoring',
      targets: [],
      matches: (x) => x.phase === 'stage1',
      body: (
        <>
          <p>
            Each lead through three Gemini Flash calls at temperatures 0.1, 0.5,
            0.9. A single sample disagrees with itself on borderline verticals —
            three voting forces stability.
          </p>
          <p>Elapsed: {fmtElapsed(p.elapsedSec)}.</p>
        </>
      ),
    },
    {
      id: 'bridge_stage1',
      isMainStep: false,
      counterLabel: 'What just happened',
      title: 'What just happened',
      targets: [],
      body: (
        <p>
          65 leads ranked in 5 minutes. In production, the top 12 land in Slack
          before the team has finished morning coffee.
        </p>
      ),
    },
    {
      id: 'm3',
      isMainStep: true,
      title: 'Step 3 of 10 — Stage 1 complete',
      targets: [
        '[data-tutorial-anchor="slack-shortlist"]',
        '[data-tutorial-anchor="crm-sync-line"]',
        '[data-tutorial-anchor="drive-header"]',
        '[data-tutorial-anchor="stage1-complete"]',
        '[data-tutorial-anchor="prospect-anchor"]',
      ],
      matches: (x) => x.phase === 'stage1_complete',
      body: (
        <>
          <p>
            Slack, HubSpot, Drive all written in one Postgres transaction. If
            any of the three fails, the whole thing rolls back. No half-states.
          </p>
          <p>
            Doug clicks "Generate Briefing" in Slack to dispatch Stage 2.
          </p>
        </>
      ),
    },
    {
      id: 'm4',
      isMainStep: true,
      title: 'Step 4 of 10 — briefing dispatched',
      targets: [],
      matches: (x) => x.phase === 'stage2_requesting',
      body: (
        <p>
          Stage 2 enqueued for {tracer}. Five sections in order: taxonomy →
          defect → comparable → risk → approach. Each section a Celery task
          with explicit dependencies.
        </p>
      ),
    },
    {
      id: 'm5',
      isMainStep: true,
      title: 'Step 5 of 10 — process taxonomy',
      targets: ['[data-section="process_taxonomy"]'],
      matches: (x) => x.phase === 'stage2' && x.stage2Progress.process_taxonomy === 'active',
      body: (
        <p>
          First section rendering. The LLM extracts process geometry from a
          vocabulary the KG defines per vertical — it can't drift outside known
          process structures.
        </p>
      ),
    },
    {
      id: 'm6',
      isMainStep: true,
      title: 'Step 6 of 10 — defect hypothesis',
      targets: ['[data-section="defect_hypothesis"]'],
      matches: (x) => x.phase === 'stage2' && x.stage2Progress.defect_hypothesis === 'active',
      body: (
        <>
          <p>
            Three Gemini Flash samples agree on a defect class above a per-class
            threshold, or the section defers to human review. No invented
            consensus.
          </p>
          <p style={{ fontSize: '11px', opacity: 0.7, marginTop: '6px' }}>
            <em>
              Note: ensemble-agreement gating, not split-conformal prediction.
              See docs/CALIBRATION.md.
            </em>
          </p>
        </>
      ),
    },
    {
      id: 'm7',
      isMainStep: true,
      title: 'Step 7 of 10 — comparable deployment',
      targets: [
        '[data-section="comparable_deployment"]',
        '[data-tutorial-anchor="comparable-anchor"]',
      ],
      matches: (x) =>
        x.phase === 'stage2' &&
        (x.stage2Progress.comparable_deployment === 'active' ||
          x.stage2Progress.comparable_deployment === 'complete'),
      body: (
        <>
          <p>
            The KG selector picks the anchor; the LLM only writes prose against
            it. No matching anchor → the section says so, doesn't fabricate.
          </p>
          <p>
            The dossier can't invent a Matta customer that doesn't exist.
          </p>
        </>
      ),
    },
    {
      id: 'bridge_m7',
      isMainStep: false,
      counterLabel: 'What this guarantees',
      title: 'What this guarantees',
      targets: [],
      body: (
        <p>
          The #1 LLM dossier failure mode is hallucinated customer references.
          Refinery makes that failure structurally impossible — the LLM writes
          against verified ground truth, not training data.
        </p>
      ),
    },
    {
      id: 'm8',
      isMainStep: true,
      title: 'Step 8 of 10 — integration risk register',
      targets: ['[data-section="risk_register"]'],
      matches: (x) => x.phase === 'stage2' && x.stage2Progress.risk_register === 'active',
      body: (
        <p>
          Each risk tied to a pillar (infrastructure, environmental, compliance)
          with a verbatim KG anchor. Risks Matta hasn't actually encountered
          don't appear.
        </p>
      ),
    },
    {
      id: 'm9',
      isMainStep: true,
      title: 'Step 9 of 10 — suggested approach',
      targets: ['[data-section="suggested_approach"]'],
      matches: (x) => x.phase === 'stage2' && x.stage2Progress.suggested_approach === 'active',
      body: (
        <p>
          Two-camera pilot scaffold: kickoff → shadow → parallel → handoff. The
          template is hardcoded; the LLM fills in prospect-specific details
          against KG-anchored patterns.
        </p>
      ),
    },
    {
      id: 'm12',
      isMainStep: true,
      title: 'Step 10 of 10 — briefing ready',
      targets: [
        '[data-tutorial-anchor="slack-shortlist"]',
        '[data-tutorial-anchor="crm-strip"]',
        '[data-tutorial-anchor="dossier-doc"]',
        '[data-tutorial-anchor="dossier-complete"]',
      ],
      matches: (x) => x.phase === 'complete',
      body: (
        <>
          <p>
            Dossier written to all three surfaces in one Postgres transaction.
          </p>
          <p>
            Total: {fmtElapsed(p.elapsedSec)} · Byte-density {ratioCopy} (floor
            0.60) · Sections 5/5 · KG anchors verified 4/4.
          </p>
          <p>Click Reset to brief another prospect.</p>
        </>
      ),
    },
  ];
}

function findStepIndexForPhase(allSteps: TutorialStep[], p: Props): number {
  for (let i = allSteps.length - 1; i >= 0; i--) {
    const s = allSteps[i];
    if (s.matches && s.matches(p)) return i;
  }
  return 0;
}

const HIGHLIGHT_CLASS = 'tutorial-target';
const BRIDGE_DURATION_MS = 6000;

type DockPosition = 'top-right' | 'bottom-right' | 'bottom-left';
const DOCK_CYCLE: DockPosition[] = ['top-right', 'bottom-right', 'bottom-left'];

export default function TutorialCallout(props: Props) {
  const [dismissed, setDismissed] = useState(false);
  const [minimized, setMinimized] = useState(false);
  const [dockPosition, setDockPosition] = useState<DockPosition>('top-right');
  const [manualStep, setManualStep] = useState<number | null>(null);
  const [autoFollow, setAutoFollow] = useState(true);
  const [bridgeOverride, setBridgeOverride] = useState<number | null>(null);
  const highlightedRef = useRef<Element[]>([]);
  const prevPhaseRef = useRef<DemoPhase>(props.phase);
  const prevCmpRef = useRef<string>(props.stage2Progress.comparable_deployment);

  const allSteps = useMemo(() => buildStepArray(props), [props]);
  const mainStepCount = useMemo(
    () => allSteps.filter((s) => s.isMainStep).length,
    [allSteps]
  );

  const phaseStepIndex = useMemo(
    () => findStepIndexForPhase(allSteps, props),
    [allSteps, props]
  );

  // Bridge auto-render: when phase transitions to stage1_complete, briefly
  // show the post-Stage-1 bridge. When comparable_deployment becomes
  // 'complete', briefly show the post-§3 bridge. Cleared after 6s.
  useEffect(() => {
    if (props.phase === 'stage1_complete' && prevPhaseRef.current !== 'stage1_complete') {
      const idx = allSteps.findIndex((s) => s.id === 'bridge_stage1');
      if (idx >= 0) {
        setBridgeOverride(idx);
        const t = window.setTimeout(() => setBridgeOverride(null), BRIDGE_DURATION_MS);
        prevPhaseRef.current = props.phase;
        return () => window.clearTimeout(t);
      }
    }
    prevPhaseRef.current = props.phase;
  }, [props.phase, allSteps]);

  useEffect(() => {
    const cmp = props.stage2Progress.comparable_deployment;
    if (cmp === 'complete' && prevCmpRef.current !== 'complete') {
      const idx = allSteps.findIndex((s) => s.id === 'bridge_m7');
      if (idx >= 0) {
        setBridgeOverride(idx);
        const t = window.setTimeout(() => setBridgeOverride(null), BRIDGE_DURATION_MS);
        prevCmpRef.current = cmp;
        return () => window.clearTimeout(t);
      }
    }
    prevCmpRef.current = cmp;
  }, [props.stage2Progress.comparable_deployment, allSteps]);

  const currentStepIndex = !autoFollow && manualStep !== null
    ? manualStep
    : bridgeOverride !== null
    ? bridgeOverride
    : phaseStepIndex;

  const currentStep = allSteps[currentStepIndex];

  // Step counter — main-step number only (bridges show counterLabel)
  const mainNumber = useMemo(() => {
    if (!currentStep?.isMainStep) return null;
    return allSteps.slice(0, currentStepIndex + 1).filter((s) => s.isMainStep).length;
  }, [allSteps, currentStepIndex, currentStep]);

  const goPrev = () => {
    setAutoFollow(false);
    setManualStep(Math.max(0, currentStepIndex - 1));
  };
  const goNext = () => {
    setAutoFollow(false);
    setManualStep(Math.min(allSteps.length - 1, currentStepIndex + 1));
  };
  const resumeAuto = () => {
    setAutoFollow(true);
    setManualStep(null);
  };
  const cycleDock = () => {
    setDockPosition((prev) => DOCK_CYCLE[(DOCK_CYCLE.indexOf(prev) + 1) % DOCK_CYCLE.length]);
  };

  // Apply target highlights for currently displayed step
  useEffect(() => {
    if (dismissed || !currentStep || currentStep.targets.length === 0) return;
    const elements: Element[] = [];
    currentStep.targets.forEach((selector) => {
      document.querySelectorAll(selector).forEach((el) => elements.push(el));
    });
    elements.forEach((el) => el.classList.add(HIGHLIGHT_CLASS));
    highlightedRef.current = elements;
    return () => {
      highlightedRef.current.forEach((el) => el.classList.remove(HIGHLIGHT_CLASS));
      highlightedRef.current = [];
    };
  }, [currentStep, dismissed]);

  if (dismissed) return null;
  if (!currentStep) return null;

  const counterText = currentStep.isMainStep
    ? `Step ${mainNumber} of ${mainStepCount}`
    : currentStep.counterLabel ?? 'Bridge';

  if (minimized) {
    return (
      <button
        className="tutorial-pill"
        type="button"
        data-tutorial-anchor="guided-demo-card"
        data-tutorial-state="minimized"
        data-dock-position={dockPosition}
        onClick={() => setMinimized(false)}
        aria-label={`Expand guided demo (${counterText})`}
      >
        <span className="tutorial-pill__step">{counterText}</span>
        <span className="tutorial-pill__sep">·</span>
        <span className="tutorial-pill__title">{currentStep.title}</span>
        {currentStep.isMainStep && mainNumber !== null && (
          <div className="tutorial-pill__progress">
            <div
              className="tutorial-pill__progress-fill"
              style={{ width: `${(mainNumber / mainStepCount) * 100}%` }}
            />
          </div>
        )}
      </button>
    );
  }

  return (
    <aside
      className={`tutorial-callout ${!autoFollow ? 'tutorial-callout--manual' : ''}`}
      role="status"
      aria-live="polite"
      data-tutorial-anchor="guided-demo-card"
      data-tutorial-state="expanded"
      data-dock-position={dockPosition}
    >
      <div className="tutorial-callout__header">
        <span className="tutorial-callout__tag">Guided demo</span>
        <div className="tutorial-callout__controls">
          <button
            className="tutorial-callout__ctrl"
            aria-label={`Dock to next corner (currently ${dockPosition})`}
            title="Cycle dock position"
            onClick={cycleDock}
            type="button"
          >
            ⊡
          </button>
          <button
            className="tutorial-callout__ctrl"
            aria-label="Minimize tutorial"
            title="Minimize"
            onClick={() => setMinimized(true)}
            type="button"
          >
            ⊟
          </button>
          <button
            className="tutorial-callout__ctrl tutorial-callout__close"
            aria-label="Dismiss tutorial"
            title="Dismiss"
            onClick={() => setDismissed(true)}
            type="button"
          >
            ×
          </button>
        </div>
      </div>

      <div className="tutorial-callout__nav">
        <button
          className="tutorial-callout__nav-btn"
          onClick={goPrev}
          disabled={currentStepIndex === 0}
          aria-label="Previous step"
          type="button"
        >
          ←
        </button>
        <span className="tutorial-callout__counter">{counterText}</span>
        <button
          className="tutorial-callout__nav-btn"
          onClick={goNext}
          disabled={currentStepIndex === allSteps.length - 1}
          aria-label="Next step"
          type="button"
        >
          →
        </button>
      </div>

      <div className="tutorial-callout__body">
        <h3 className="tutorial-callout__title">{currentStep.title}</h3>
        <div className="tutorial-callout__text">{currentStep.body}</div>
      </div>

      {!autoFollow && (
        <button
          className="tutorial-callout__resume"
          onClick={resumeAuto}
          type="button"
        >
          ↻ Resume auto-follow
        </button>
      )}

      {currentStep.isMainStep && mainNumber !== null && (
        <div className="tutorial-callout__progress">
          <div className="tutorial-callout__progress-bar">
            <div
              className="tutorial-callout__progress-fill"
              style={{ width: `${(mainNumber / mainStepCount) * 100}%` }}
            />
          </div>
        </div>
      )}
    </aside>
  );
}
