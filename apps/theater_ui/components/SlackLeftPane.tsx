import React, { useState } from 'react';
import type { DemoPhase, TopProspect, TracerStatus } from '../hooks/useWebSocket';
import { TOP_12_PROSPECTS, ProspectCard } from './prospectData';
import CsvPreviewModal from './CsvPreviewModal';
import type { SeedCsv } from './seedCsvs';

interface Props {
  phase: DemoPhase;
  elapsedSec: number;
  activeCsv: SeedCsv;
  tracerProspect: TopProspect | null;
  tracerStatus: TracerStatus;
  onClickProspect: (prospectId: string, companyName: string) => void;
}

function fmtElapsed(sec: number): string {
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return `${m}:${s.toString().padStart(2, '0')}`;
}

// Slack timestamp formatting — "Today at 9:42 AM" pattern, derived from
// page-load time so the demo always reads as "today". The Doug message is
// stamped a few minutes before; bot messages are stamped at current load.
function slackTimestamp(offsetMin = 0): string {
  const d = new Date(Date.now() - offsetMin * 60_000);
  const hh = d.getHours() % 12 || 12;
  const mm = d.getMinutes().toString().padStart(2, '0');
  const ap = d.getHours() >= 12 ? 'PM' : 'AM';
  return `Today at ${hh}:${mm} ${ap}`;
}

const DOUG_INITIALS = 'DB';
const REFINERY_ICON_PATH = '/branding/matta_logo_icon.jpg';

export default function SlackLeftPane({ phase, elapsedSec, activeCsv, tracerProspect, tracerStatus, onClickProspect }: Props) {
  const [hoverTip, setHoverTip] = useState<string | null>(null);
  const [csvModalOpen, setCsvModalOpen] = useState(false);
  const [refineryIconFailed, setRefineryIconFailed] = useState(false);

  const csvPath = activeCsv.publicPath;
  const csvLabel = `${activeCsv.filename}`;

  const stage1Running = phase === 'stage1';
  const stage1Done =
    phase === 'stage1_complete' ||
    phase === 'stage2_requesting' ||
    phase === 'stage2' ||
    phase === 'complete';
  const stage2Done = phase === 'complete';
  const clickable = stage1Done;

  // Timestamps must be computed client-side only — server-side render runs
  // in the container's UTC timezone while the browser renders in the
  // viewer's local timezone, which produces a hydration mismatch if the
  // timestamp string is materialized during SSR. Initialise null and
  // populate in useEffect after hydration.
  const [dougTimestamp, setDougTimestamp] = useState<string | null>(null);
  const [refineryRankedTimestamp, setRefineryRankedTimestamp] = useState<string | null>(null);
  const [refineryBriefingTimestamp, setRefineryBriefingTimestamp] = useState<string | null>(null);

  // Doug's timestamp is fixed at the first client render (4 minutes earlier
  // than now, so it reads as a recent message in the channel)
  React.useEffect(() => {
    if (dougTimestamp === null) {
      setDougTimestamp(slackTimestamp(4));
    }
  }, [dougTimestamp]);

  // Set bot timestamps the first time each message appears
  React.useEffect(() => {
    if (stage1Done && refineryRankedTimestamp === null) {
      setRefineryRankedTimestamp(slackTimestamp(0));
    }
  }, [stage1Done, refineryRankedTimestamp]);
  React.useEffect(() => {
    if (stage2Done && refineryBriefingTimestamp === null) {
      setRefineryBriefingTimestamp(slackTimestamp(0));
    }
  }, [stage2Done, refineryBriefingTimestamp]);

  const RefineryAvatar = () => {
    if (refineryIconFailed) {
      return <span className="slack-avatar slack-avatar--bot">M</span>;
    }
    return (
      /* eslint-disable-next-line @next/next/no-img-element */
      <img
        className="slack-avatar slack-avatar--img"
        src={REFINERY_ICON_PATH}
        alt="Refinery"
        onError={() => setRefineryIconFailed(true)}
      />
    );
  };

  return (
    <div className="slack-pane">
      <div className="slack-channel-header" data-tutorial-anchor="slack-channel">
        <div className="slack-channel-header__top">
          <span className="slack-channel-header__hash">#</span>
          <span className="slack-channel-header__name">fde-lead-refinery</span>
        </div>
        <div className="slack-channel-header__sub">
          Lead Refinery automated pipeline · Refinery bot posts ranked shortlist + briefings
        </div>
      </div>

      {/* Doug's message */}
      <div className="slack-msg">
        <div className="slack-avatar slack-avatar--doug">{DOUG_INITIALS}</div>
        <div className="slack-msg__body">
          <div className="slack-msg__meta">
            <span className="slack-msg__author">Doug</span>
            <span className="slack-msg__time">{dougTimestamp ?? ''}</span>
          </div>
          <div className="slack-msg__text">{activeCsv.dougMessage}</div>
          <button
            className="slack-attachment slack-attachment--clickable"
            data-tutorial-anchor="csv-attachment"
            onClick={() => setCsvModalOpen(true)}
            type="button"
            aria-label="Preview CSV input"
          >
            <span className="slack-attachment__icon">📎</span>
            <div className="slack-attachment__meta">
              <span className="slack-attachment__filename">{csvLabel}</span>
              <span className="slack-attachment__size">{activeCsv.approxLeadCount} leads · CSV</span>
            </div>
            <span className="slack-attachment__hint">Preview →</span>
          </button>
        </div>
      </div>

      <CsvPreviewModal
        open={csvModalOpen}
        csvPath={csvPath}
        csvLabel={csvLabel}
        onClose={() => setCsvModalOpen(false)}
      />

      {/* Stage 1 in-flight indicator (between Doug's message and the bot reply) */}
      {stage1Running && (
        <div className="slack-typing">
          <div className="slack-avatar slack-avatar--bot slack-avatar--small">
            {refineryIconFailed ? 'M' : (
              /* eslint-disable-next-line @next/next/no-img-element */
              <img src={REFINERY_ICON_PATH} alt="Refinery" onError={() => setRefineryIconFailed(true)} />
            )}
          </div>
          <span className="slack-typing__text">
            Refinery is ranking · {fmtElapsed(elapsedSec)}
          </span>
          <span className="slack-typing__dots" aria-hidden="true">
            <span /><span /><span />
          </span>
        </div>
      )}

      {/* Refinery bot ranked shortlist message */}
      {stage1Done && (
        <div className="slack-msg slack-msg--bot" data-tutorial-anchor="slack-shortlist">
          <RefineryAvatar />
          <div className="slack-msg__body">
            <div className="slack-msg__meta">
              <span className="slack-msg__author">Refinery</span>
              <span className="slack-app-badge">APP</span>
              <span className="slack-msg__time">{refineryRankedTimestamp ?? ''}</span>
            </div>
            <div className="slack-msg__text">
              Ranked the {activeCsv.approxLeadCount} {activeCsv.tradeShowDisplay} leads.
              Top 12 below — click <strong>Generate Briefing</strong> on any prospect to
              produce the full pre-visit dossier.
            </div>

            {tracerStatus === 'unavailable' && (
              <div className="slack-blockkit__hint">
                Awaiting ranking… <span className="slack-blockkit__hint-sub">/api/batch/{'{batch_id}'}/top_prospect returned 404 twice; click handler temporarily disabled.</span>
              </div>
            )}

            <div className="slack-blockkit">
              <ul className="slack-blockkit__cards">
                {TOP_12_PROSPECTS.map((p: ProspectCard) => {
                  // The rank-1 card is the live tracer — substitute its
                  // display fields with the resolved tracer from
                  // /top_prospect (falls back to activeCsv.tracerCompany +
                  // hardcoded fitness while the endpoint is resolving).
                  const isTracer = p.rank === 1;
                  const displayName = isTracer
                    ? tracerProspect?.company_name ?? activeCsv.tracerCompany
                    : p.companyName;
                  const displayProspectId = isTracer
                    ? tracerProspect?.prospect_id ?? p.prospectId
                    : p.prospectId;
                  const displayFit = isTracer && tracerProspect
                    ? tracerProspect.fitness_score
                    : p.fitnessScore;
                  // Tracer card: clickable when Stage 1 done + tracer endpoint
                  // resolved. Non-tracer cards (rank 2-12): NEVER clickable —
                  // they're cosmetic top-12 placeholders. The Generate Briefing
                  // button on those cards is disabled with an explanatory
                  // tooltip. Card itself stays focusable for TutorialCallout
                  // highlighting and screen-reader navigation.
                  const tracerClickable = clickable && tracerStatus !== 'unavailable';
                  const cardClickable = isTracer && tracerClickable;
                  const tooltip = isTracer
                    ? `Triggers Stage 2 dossier generation for ${displayName}`
                    : `Demo wires Stage 2 through the rank-1 tracer · Phase 1 scope`;
                  return (
                    <li
                      key={p.prospectId}
                      className={`prospect-card ${
                        !isTracer ? 'prospect-card--placeholder' : ''
                      } ${
                        isTracer && !cardClickable ? 'prospect-card--disabled' : ''
                      }`}
                      onMouseEnter={() => setHoverTip(p.prospectId)}
                      onMouseLeave={() => setHoverTip(null)}
                      onClick={() => cardClickable && onClickProspect(displayProspectId, displayName)}
                      role="button"
                      tabIndex={cardClickable ? 0 : -1}
                      aria-disabled={!cardClickable}
                      data-prospect-rank={p.rank}
                      data-tutorial-anchor={isTracer ? 'prospect-anchor' : undefined}
                    >
                      <div className="prospect-card__head">
                        <span className="prospect-card__rank">#{p.rank}</span>
                        <span className="prospect-card__name">{displayName}</span>
                        <span className="prospect-card__fit">fit {displayFit.toFixed(2)}</span>
                      </div>
                      <div className="prospect-card__meta">
                        <span>{p.vertical.replace(/_/g, ' ')}</span>
                        <span className="prospect-card__sep">·</span>
                        <span>{activeCsv.tradeShowDisplay}</span>
                      </div>
                      <div className="prospect-card__footer">
                        <button
                          className="prospect-card__cta"
                          type="button"
                          disabled={!cardClickable}
                          onClick={(e) => {
                            e.stopPropagation();
                            if (cardClickable) onClickProspect(displayProspectId, displayName);
                          }}
                        >
                          Generate Briefing
                        </button>
                      </div>
                      {hoverTip === p.prospectId && (
                        <div className="prospect-card__tooltip">{tooltip}</div>
                      )}
                    </li>
                  );
                })}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Refinery bot follow-up after dossier ships */}
      {stage2Done && (
        <div className="slack-msg slack-msg--bot" data-tutorial-anchor="slack-briefing-update">
          <RefineryAvatar />
          <div className="slack-msg__body">
            <div className="slack-msg__meta">
              <span className="slack-msg__author">Refinery</span>
              <span className="slack-app-badge">APP</span>
              <span className="slack-msg__time">{refineryBriefingTimestamp ?? ''}</span>
            </div>
            <div className="slack-blockkit slack-blockkit--briefing-ready">
              <div className="slack-blockkit__header">
                ✅ Pre-visit briefing ready for{' '}
                <strong>{tracerProspect?.company_name ?? activeCsv.tracerCompany}</strong>
              </div>
              <div className="slack-blockkit__summary">
                Process taxonomy · Defect hypothesis (N=3 conformal) · Comparable Matta
                deployment · Integration risks · Suggested approach. Validated against
                the deterministic-byte gate.
              </div>
              <div className="slack-blockkit__actions">
                <button className="slack-blockkit__btn" type="button">
                  📄 View briefing in Drive
                </button>
                <button className="slack-blockkit__btn slack-blockkit__btn--secondary" type="button">
                  📋 Open CRM record
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
