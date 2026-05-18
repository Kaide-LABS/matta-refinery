import React, { useState } from 'react';
import type { DemoPhase } from '../hooks/useWebSocket';
import { TOP_12_PROSPECTS, ProspectCard } from './prospectData';
import CsvPreviewModal from './CsvPreviewModal';
import type { SeedCsv } from './seedCsvs';

interface Props {
  phase: DemoPhase;
  elapsedSec: number;
  activeCsv: SeedCsv;
  onClickProspect: (prospectId: string, companyName: string) => void;
}

function fmtElapsed(sec: number): string {
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return `${m}:${s.toString().padStart(2, '0')}`;
}

export default function SlackLeftPane({ phase, elapsedSec, activeCsv, onClickProspect }: Props) {
  const [hoverTip, setHoverTip] = useState<string | null>(null);
  const [csvModalOpen, setCsvModalOpen] = useState(false);

  const csvPath = activeCsv.publicPath;
  const csvLabel = `${activeCsv.filename} · ${activeCsv.approxLeadCount} leads`;

  const stage1Running = phase === 'stage1';
  const stage1Done =
    phase === 'stage1_complete' ||
    phase === 'stage2_requesting' ||
    phase === 'stage2' ||
    phase === 'complete';
  const clickable = stage1Done;

  return (
    <div className="slack-pane">
      <div className="slack-pane__channel">#fde-lead-refinery</div>
      <div className="slack-pane__msg">
        <span className="slack-pane__author">Doug</span> {activeCsv.dougMessage}
      </div>
      <button
        className="slack-pane__attachment slack-pane__attachment--clickable"
        data-tutorial-anchor="csv-attachment"
        onClick={() => setCsvModalOpen(true)}
        type="button"
        aria-label="Preview CSV input"
      >
        <span className="slack-pane__attachment-icon">📎</span>
        <span className="slack-pane__attachment-label">{csvLabel}</span>
        <span className="slack-pane__attachment-hint">Preview →</span>
      </button>
      <CsvPreviewModal
        open={csvModalOpen}
        csvPath={csvPath}
        csvLabel={csvLabel}
        onClose={() => setCsvModalOpen(false)}
      />

      {stage1Running && (
        <div className="slack-pane__status slack-pane__status--inflight">
          Refinery ranking · {fmtElapsed(elapsedSec)}
        </div>
      )}

      {stage1Done && (
        <div className="slack-pane__shortlist" data-tutorial-anchor="slack-shortlist">
          <div className="slack-pane__shortlist-header">
            <span>Refinery Ranked Shortlist</span>
            <span className="slack-pane__shortlist-count">Top 12 of 124</span>
          </div>
          <ul className="slack-pane__cards">
            {TOP_12_PROSPECTS.map((p: ProspectCard) => {
              const isWilliamCook = p.companyName.toLowerCase().includes('william cook');
              const tooltip = isWilliamCook
                ? 'Generate full dossier for William Cook Sheffield'
                : 'Demo focuses on William Cook Sheffield';
              return (
                <li
                  key={p.prospectId}
                  className={`prospect-card ${isWilliamCook ? 'prospect-card--anchor' : ''} ${
                    !clickable ? 'prospect-card--disabled' : ''
                  }`}
                  onMouseEnter={() => setHoverTip(p.prospectId)}
                  onMouseLeave={() => setHoverTip(null)}
                  onClick={() => clickable && onClickProspect(p.prospectId, p.companyName)}
                  role="button"
                  tabIndex={clickable ? 0 : -1}
                  aria-disabled={!clickable}
                  data-tutorial-anchor={isWilliamCook ? 'prospect-anchor' : undefined}
                >
                  <div className="prospect-card__rank">{p.rank}</div>
                  <div className="prospect-card__body">
                    <div className="prospect-card__name">{p.companyName}</div>
                    <div className="prospect-card__meta">
                      <span>fit {p.fitnessScore.toFixed(2)}</span>
                      <span className="prospect-card__sep">·</span>
                      <span>{p.vertical.replace('_', ' ')}</span>
                    </div>
                    {hoverTip === p.prospectId && (
                      <div className="prospect-card__tooltip">{tooltip}</div>
                    )}
                  </div>
                  {isWilliamCook && <div className="prospect-card__cta">Generate</div>}
                </li>
              );
            })}
          </ul>
        </div>
      )}
    </div>
  );
}
