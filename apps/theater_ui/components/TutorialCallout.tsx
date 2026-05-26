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
            Doug just got back from a trade show with 65 leads. Normally that means
            three nights of triage before the team knows which factories matter.
            Refinery does the ranking, briefing, and CRM update in 7 minutes — and
            delivers the result to Slack, HubSpot, and Drive simultaneously. The
            team never leaves the tools they already live in.
          </p>
          <p>Click Run Demo to start.</p>
        </>
      ),
    },
    {
      id: 'ingesting',
      isMainStep: true,
      title: 'Step 1 of 11 — ingest',
      targets: [],
      matches: (x) => x.phase === 'ingesting',
      body: (
        <>
          <p>
            CSV posted to /ingest/batch with an idempotency-keyed Postgres write.
            The Action Domain Classifier (ADC) routes the batch to PRIORITIZATION —
            Stage 1 is about to fan out across 65 prospects.
          </p>
          <p>
            What's verifiable: the ADC is deterministic Python in
            packages/adc/rules.py — zero LLM calls in routing. Damjan can grep this.
          </p>
        </>
      ),
    },
    {
      id: 'stage1',
      isMainStep: true,
      title: 'Step 2 of 11 — Stage 1 temperature-varied ensemble scoring',
      targets: [],
      matches: (x) => x.phase === 'stage1',
      body: (
        <>
          <p>
            Each lead runs through an N=3 ensemble for vertical classification,
            then through a deterministic fit-scoring function against calibrated
            weights. ~5 minutes for the 65-lead cohort.
          </p>
          <p>
            Why ensemble: a single LLM call disagrees with itself on borderline
            verticals. Three independent samples + an inter-model agreement floor
            forces stability before the prospect enters the dossier pipeline.
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
          65 leads ranked in 5 minutes with no human triage. In production, this
          is where Doug's Monday morning starts — with the top 12 already in
          Slack, ranked by fit-to-Matta, before the team has finished coffee.
        </p>
      ),
    },
    {
      id: 'm3',
      isMainStep: true,
      title: 'Step 3 of 11 — Stage 1 complete',
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
            Slack, HubSpot, and Drive all updated in one Postgres transaction via
            the transactional outbox — three surfaces, no half-states. If any of
            the three writes fails, the whole thing rolls back.
          </p>
          <p>
            In production: Doug clicks "Generate Briefing" inside Slack. The
            click is embedded in this view so you can see what fires.
          </p>
          <p>
            <em>Implementation: Slack interaction event → /slack/interactions.</em>
          </p>
        </>
      ),
    },
    {
      id: 'm4',
      isMainStep: true,
      title: 'Step 4 of 11 — briefing dispatched',
      targets: [],
      matches: (x) => x.phase === 'stage2_requesting',
      body: (
        <>
          <p>
            Slack interaction event accepted. Refinery generated a dossier_id and
            enqueued the {tracer} briefing. Five sections will render in order:
            process taxonomy, defect hypothesis, comparable deployment,
            integration risk register, suggested approach.
          </p>
          <p>
            Each section is its own Celery task with deterministic dependencies —
            defect hypothesis can't start until process taxonomy succeeds.
          </p>
        </>
      ),
    },
    {
      id: 'm5',
      isMainStep: true,
      title: 'Step 5 of 11 — process taxonomy',
      targets: ['[data-section="process_taxonomy"]'],
      matches: (x) => x.phase === 'stage2' && x.stage2Progress.process_taxonomy === 'active',
      body: (
        <>
          <p>
            First section rendering. The LLM extracts the prospect's process
            geometry — but the vocabulary is constrained per vertical by the
            knowledge graph. For additive manufacturing: deposition rate, layer
            thickness, robot path class. For metal casting: pour temperature,
            casting type, geometry class. For bottling: line speed, fill rate.
          </p>
          <p>
            The LLM can't drift outside known process structures because the
            allowed terms are loaded from the verified KG, not inferred.
          </p>
        </>
      ),
    },
    {
      id: 'm6',
      isMainStep: true,
      title: 'Step 6 of 11 — defect hypothesis (N=3 ensemble agreement)',
      targets: ['[data-section="defect_hypothesis"]'],
      matches: (x) => x.phase === 'stage2' && x.stage2Progress.defect_hypothesis === 'active',
      body: (
        <>
          <p>
            Three independent Gemini Flash samples at temperatures 0.1 / 0.5 /
            0.9, then an inter-model agreement gate at ≥0.90 with per-class
            calibrated thresholds. The hypothesis only ships if the ensemble
            votes the same defect class with sufficient concurrence.
          </p>
          <p>
            Disagreement is honest: if the three samples can't cluster, the
            section returns "deferred for human review" instead of inventing
            consensus.
          </p>
          <p style={{ fontSize: '11px', opacity: 0.7, marginTop: '6px' }}>
            <em>
              Methodology note: this is ensemble agreement gating, not formal
              split-conformal prediction (Vovk/Shafer). See
              docs/CALIBRATION.md for the methodology and known limitations.
            </em>
          </p>
        </>
      ),
    },
    {
      id: 'm7',
      isMainStep: true,
      title: 'Step 7 of 11 — comparable deployment (the load-bearing safety rail)',
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
          <p>This is the most important section in the dossier.</p>
          <p>
            The comparable Matta deployment is selected by the knowledge-graph
            selector, not the LLM. The LLM only writes prose against the anchor
            the KG selects. If the prospect's vertical doesn't match a verified
            KG anchor, the LLM gets nothing to write against — and the section
            returns "no comparable deployment available" instead of fabricating.
          </p>
          <p>
            This is how the dossier can't invent a Matta customer that doesn't
            exist.
          </p>
          <p>
            Click the KG ✓ in the header to see the 4 verified anchors with
            Cambridge IfM Wayback proof.
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
          LLM dossier failure mode #1 is hallucinated customer references — the
          model confidently citing deployments that don't exist. Refinery makes
          that failure mode structurally impossible: the LLM writes against
          verified ground truth, never its training data.
        </p>
      ),
    },
    {
      id: 'm8',
      isMainStep: true,
      title: 'Step 8 of 11 — integration risk register',
      targets: ['[data-section="risk_register"]'],
      matches: (x) => x.phase === 'stage2' && x.stage2Progress.risk_register === 'active',
      body: (
        <>
          <p>
            Each risk is tied to a pillar (infrastructure, environmental,
            compliance) with a severity score and a verbatim knowledge-graph
            anchor. No free-form LLM speculation about risks Matta hasn't
            actually encountered.
          </p>
          <p>
            If a risk type isn't in the KG, the section omits it rather than
            fabricating.
          </p>
        </>
      ),
    },
    {
      id: 'm9',
      isMainStep: true,
      title: 'Step 9 of 11 — suggested approach',
      targets: ['[data-section="suggested_approach"]'],
      matches: (x) => x.phase === 'stage2' && x.stage2Progress.suggested_approach === 'active',
      body: (
        <>
          <p>
            Phased plan assembling — two-camera pilot scaffold with deterministic
            phase breakdown: kickoff → shadow → parallel → handoff.
          </p>
          <p>
            The phase template is hardcoded; the LLM only fills in the
            prospect-specific details for each phase against KG-anchored
            deployment patterns.
          </p>
        </>
      ),
    },
    {
      id: 'm12',
      isMainStep: true,
      title: 'Step 11 of 11 — briefing ready',
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
            The dossier shipped to all three surfaces in one Postgres transaction
            — no half-states, no Slack-succeeded-HubSpot-failed split.
          </p>
          <p>
            Total elapsed: {fmtElapsed(p.elapsedSec)}.
            <br />
            Byte-density ratio: {ratioCopy} (floor 0.60).
            <br />
            Sections shipped: 5/5.
            <br />
            KG anchors verified: 4/4.
          </p>
          <p>
            This is what Doug's Monday morning looks like with Refinery in
            place. Click Reset to generate a briefing for a different prospect.
          </p>
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
