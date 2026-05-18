import React, { useEffect, useState } from 'react';
import type { DemoPhase } from '../hooks/useWebSocket';

interface Props {
  phase: DemoPhase;
}

// HubSpot's brand orange — adjacent but not pixel-matched to their exact
// trademark color. Recognizably their family without being a clone.
const HUBSPOT_ORANGE = '#FF7A59';

function nowTimestamp(): string {
  const d = new Date();
  const hh = d.getHours() % 12 || 12;
  const mm = d.getMinutes().toString().padStart(2, '0');
  const ap = d.getHours() >= 12 ? 'PM' : 'AM';
  return `${d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' })} · ${hh}:${mm} ${ap}`;
}

interface FieldRow {
  label: string;
  value: string;
  emphasis?: 'pulse-on-load' | null;
}

export default function CRMRecordInset({ phase }: Props) {
  const preStage1 =
    phase === 'idle' || phase === 'ingesting' || phase === 'stage1';
  const stage1Done =
    phase === 'stage1_complete' ||
    phase === 'stage2_requesting' ||
    phase === 'stage2' ||
    phase === 'complete';
  const stage2Done = phase === 'complete';

  // Trigger field-update pulse animations once at Stage 1 completion
  const [scorePulse, setScorePulse] = useState(false);
  const [slotPulse, setSlotPulse] = useState(false);
  const [lastScored, setLastScored] = useState<string | null>(null);

  useEffect(() => {
    if (stage1Done && !lastScored) {
      setLastScored(nowTimestamp());
      setScorePulse(true);
      setSlotPulse(true);
      const t = window.setTimeout(() => {
        setScorePulse(false);
        setSlotPulse(false);
      }, 1200);
      return () => window.clearTimeout(t);
    }
  }, [stage1Done, lastScored]);

  const fields: FieldRow[] = preStage1
    ? [
        { label: 'refinery_fit_score', value: '—' },
        { label: 'vertical', value: '—' },
        { label: 'slot_readiness', value: 'pending' },
        { label: 'requires_human_review', value: '—' },
        { label: 'last_scored_at', value: '—' },
      ]
    : [
        { label: 'refinery_fit_score', value: '0.84', emphasis: scorePulse ? 'pulse-on-load' : null },
        { label: 'vertical', value: 'metal_casting' },
        { label: 'slot_readiness', value: 'ready_for_dossier', emphasis: slotPulse ? 'pulse-on-load' : null },
        { label: 'requires_human_review', value: 'false' },
        { label: 'last_scored_at', value: lastScored ?? '—' },
      ];

  return (
    <div className="crm-inset" data-tutorial-anchor="crm-inset">
      <div className="crm-inset__header">
        <div className="crm-inset__brand">
          <span
            className="crm-inset__logo-dot"
            style={{ background: HUBSPOT_ORANGE }}
            aria-hidden="true"
          />
          <span className="crm-inset__logo">HubSpot</span>
          <span className="crm-inset__type">· Contact</span>
        </div>
        <button
          className="crm-inset__menu"
          type="button"
          aria-label="Record actions"
          title="Record actions"
        >
          ⋯
        </button>
      </div>

      <div className="crm-inset__identity">
        <div className="crm-inset__avatar">
          {preStage1 ? '—' : 'WCS'}
        </div>
        <div className="crm-inset__name-block">
          <div className="crm-inset__contact">William Cook Sheffield</div>
          <div className="crm-inset__company">Sheffield · UK · Manufacturing</div>
        </div>
      </div>

      <div className="crm-inset__section-label">Properties</div>
      <dl className="crm-inset__kv" data-tutorial-anchor="crm-properties">
        {fields.map((f) => (
          <React.Fragment key={f.label}>
            <dt data-field={f.label}>{f.label}</dt>
            <dd
              data-field-value={f.label}
              className={f.emphasis === 'pulse-on-load' ? 'crm-inset__value crm-inset__value--pulse' : 'crm-inset__value'}
            >
              {f.value}
            </dd>
          </React.Fragment>
        ))}
      </dl>

      {stage2Done && (
        <div className="crm-inset__note">
          <span className="crm-inset__note-icon">📄</span>
          <div>
            <div className="crm-inset__note-title">Pre-Visit Dossier attached</div>
            <a className="crm-inset__note-link" href="#">drive.google.com/d/wc-sheffield</a>
          </div>
        </div>
      )}
    </div>
  );
}
