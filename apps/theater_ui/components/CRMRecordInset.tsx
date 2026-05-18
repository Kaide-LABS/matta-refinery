import React from 'react';
import type { DemoPhase } from '../hooks/useWebSocket';

interface Props {
  phase: DemoPhase;
}

export default function CRMRecordInset({ phase }: Props) {
  const stage1Done =
    phase === 'stage1_complete' ||
    phase === 'stage2_requesting' ||
    phase === 'stage2' ||
    phase === 'complete';
  const stage2Done = phase === 'complete';

  if (!stage1Done) return null;

  return (
    <div className="crm-inset" data-tutorial-anchor="crm-inset">
      <div className="crm-inset__header">
        <span className="crm-inset__logo">HubSpot</span>
        <span className="crm-inset__contact">William Cook Sheffield</span>
      </div>
      <dl className="crm-inset__kv">
        <dt>refinery_fit_score</dt>
        <dd>0.84</dd>
        <dt>vertical</dt>
        <dd>metal_casting</dd>
        <dt>slot_readiness</dt>
        <dd>ready_for_dossier</dd>
        <dt>requires_human_review</dt>
        <dd>false</dd>
      </dl>
      {stage2Done && (
        <div className="crm-inset__note">
          Pre-Visit Dossier · drive.google.com/d/wc-sheffield
        </div>
      )}
    </div>
  );
}
