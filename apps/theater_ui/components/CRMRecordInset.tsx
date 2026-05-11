import React from 'react';

interface TheaterEvent {
  type: string;
  timestamp: string;
  payload: any;
}

export default function CRMRecordInset({ events }: { events: TheaterEvent[] }) {
  const stage1Complete = events.some(e => e.type === 'stage1.complete');
  const stage2Complete = events.some(e => e.type === 'stage2.complete');
  
  if (!stage1Complete) return null;

  return (
    <div className="fixed bottom-4 right-4 w-80 h-48 bg-white border border-orange-300 shadow-xl rounded-lg p-4 overflow-y-auto z-50">
      <div className="font-bold text-orange-600 border-b border-orange-100 pb-2 mb-2 text-sm">Hubspot Contact: William Cook Sheffield</div>
      <div className="text-xs space-y-1 text-gray-700">
        <div><strong>refinery_fit_score:</strong> 0.84</div>
        <div><strong>vertical:</strong> metal_casting</div>
        <div><strong>slot_readiness:</strong> ready_for_dossier</div>
        <div><strong>requires_human_review:</strong> false</div>
      </div>
      {stage2Complete && (
        <div className="mt-2 text-xs bg-yellow-50 p-2 rounded border border-yellow-200">
          <strong>Note:</strong> Pre-Visit Dossier generated 2026-05-11, link: drive.google.com/...
        </div>
      )}
    </div>
  );
}
