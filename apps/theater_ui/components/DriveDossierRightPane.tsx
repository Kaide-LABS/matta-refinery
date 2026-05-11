import React from 'react';

interface TheaterEvent {
  type: string;
  timestamp: string;
  payload: any;
}

export default function DriveDossierRightPane({ events }: { events: TheaterEvent[] }) {
  const stage2Complete = events.some(e => e.type === 'stage2.complete');
  return (
    <div className="p-4 bg-gray-50 overflow-y-auto">
      <h2 className="text-lg font-bold text-gray-800 mb-4">Google Drive Mock</h2>
      {stage2Complete ? (
        <div className="bg-white p-6 shadow-lg border border-gray-200">
          <h1 className="text-2xl font-bold mb-4">Matta Pre-Visit Dossier — William Cook Sheffield</h1>
          <p className="text-sm text-gray-500 mb-4">Generated: 2026-05-11 | KG Version: phase1-v1 | Calibration: phase1-demo-v1</p>
          <div className="text-sm mb-4">
            <h3 className="font-bold mb-1">§1 Process Taxonomy</h3>
            <p>Ductile iron casting. Ladle pour at ~1450C.</p>
          </div>
          <div className="text-sm mb-4">
            <h3 className="font-bold mb-1">§2 Defect Hypothesis</h3>
            <p>With 90% coverage, dominant defect classes are in: porosity.</p>
          </div>
          <div className="text-sm mb-4">
            <h3 className="font-bold mb-1">§3 Comparable Matta Deployment</h3>
            <p>matta_deployment_metal_casting_unnamed (Line 271)</p>
            <p className="italic">Dimension: casting_surface_finish_qc</p>
          </div>
          <div className="text-sm mb-4">
            <h3 className="font-bold mb-1">§4 Integration Risk Register</h3>
            <p>calibration_baseline_unknown: identified</p>
          </div>
          <div className="text-sm mb-4">
            <h3 className="font-bold mb-1">§5 Suggested Approach</h3>
            <p>two_camera_pilot</p>
          </div>
          <button className="mt-4 bg-blue-500 text-white px-4 py-2 rounded text-sm hover:bg-blue-600">Share</button>
        </div>
      ) : (
        <div className="text-gray-400 text-sm">Waiting for Stage 2 completion...</div>
      )}
    </div>
  );
}
