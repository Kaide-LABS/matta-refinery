import React from 'react';

interface TheaterEvent {
  type: string;
  timestamp: string;
  payload: any;
}

export default function SlackLeftPane({ events }: { events: TheaterEvent[] }) {
  const hasStage1 = events.some(e => e.type === 'stage1.complete');
  return (
    <div className="border-r border-gray-300 p-4 overflow-y-auto">
      <div className="font-bold text-lg mb-4">#fde-lead-refinery</div>
      <div className="mb-4 text-sm text-gray-700">Doug: UK Metals Expo batch — Stew can you triage?</div>
      <div className="p-3 border rounded bg-gray-50 mb-4 text-sm">Attachment: UK_Metals_Expo_2025_leads.csv</div>
      {hasStage1 && (
        <div className="p-4 border border-blue-200 rounded bg-blue-50 mt-4">
          <h3 className="font-bold mb-2">Refinery Ranked Shortlist</h3>
          <ul className="text-sm">
            <li className="mb-2">
              1. William Cook Sheffield - Score: 0.84 
              <button className="ml-2 bg-blue-600 text-white px-2 py-1 rounded text-xs">Generate Full Dossier</button>
            </li>
          </ul>
        </div>
      )}
    </div>
  );
}
