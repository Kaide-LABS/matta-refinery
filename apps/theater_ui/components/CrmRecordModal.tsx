import React, { useEffect } from 'react';
import type { TopProspect, DossierPayload } from '../hooks/useWebSocket';

interface Props {
  open: boolean;
  onClose: () => void;
  prospect: TopProspect | null;
  dossier: DossierPayload | null;
  dossierId: string | null;
}

// Phase 1.7 Stage E: CRM record modal. Backed by the existing outbox
// crm_note write path — shows the field updates that landed in HubSpot
// (mock) when the dossier completed.
export default function CrmRecordModal({ open, onClose, prospect, dossier, dossierId }: Props) {
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [open, onClose]);

  if (!open || !prospect) return null;

  const generatedAt = dossier && (dossier as Record<string, unknown>).generated_at
    ? new Date((dossier as Record<string, unknown>).generated_at as string).toLocaleString()
    : 'pending';

  return (
    <div className="crm-modal-overlay" onClick={onClose} role="presentation">
      <div className="crm-modal" onClick={(e) => e.stopPropagation()} role="dialog">
        <div className="crm-modal__header">
          <h3>CRM Record Update</h3>
          <button className="crm-modal__close" onClick={onClose} aria-label="Close">×</button>
        </div>
        <div className="crm-modal__body">
          <p className="crm-modal__provider">
            Provider: <strong>HubSpot</strong> (mock — Phase 2 wires the real CRM webhook)
          </p>
          <table className="crm-modal__fields">
            <tbody>
              <tr><td>Company</td><td>{prospect.company_name}</td></tr>
              <tr><td>Vertical</td><td>{prospect.vertical}</td></tr>
              <tr><td>Fitness Score</td><td>{prospect.fitness_score.toFixed(2)}</td></tr>
              <tr>
                <td>slot_readiness</td>
                <td><span className="crm-modal__field-update">pending → ready_for_dossier</span></td>
              </tr>
              <tr>
                <td>dossier_attached</td>
                <td>
                  <span className="crm-modal__field-update">
                    null → {dossierId ? dossierId.slice(0, 8) + '…' : 'pending'}
                  </span>
                </td>
              </tr>
              <tr><td>updated_at</td><td>{generatedAt}</td></tr>
            </tbody>
          </table>
          <p className="crm-modal__footer">
            Written via outbox row <code>crm_note</code> (state: delivered, idempotent on dossier_id).
          </p>
        </div>
      </div>
    </div>
  );
}
