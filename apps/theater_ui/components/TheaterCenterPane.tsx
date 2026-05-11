import React from 'react';

interface TheaterEvent {
  type: string;
  timestamp: string;
  payload: any;
}

export default function TheaterCenterPane({ events }: { events: TheaterEvent[] }) {
  const adcRouted = events.find(e => e.type === 'adc.routed');
  const stage2Started = events.some(e => e.type === 'stage2.section_started');
  const stage2Complete = events.some(e => e.type === 'stage2.complete');
  const comparableHighlight = events.some(e => e.type === 'stage2.section_complete' && e.payload?.section === 'comparable');

  return (
    <div className="border-r border-gray-300 p-4 bg-gray-900 text-white overflow-y-auto">
      <h2 className="text-xl font-bold mb-4">Theater Console</h2>
      
      {adcRouted && (
        <div className="mb-4">
          <span className="bg-purple-600 text-white px-2 py-1 rounded text-xs font-bold mr-2">ADC DECISION: {adcRouted.payload.route}</span>
        </div>
      )}
      
      <div className="mb-4 text-sm font-mono text-green-400">
        <div>Idempotency Keys:</div>
        <div>batch:demo_batch</div>
      </div>
      
      {stage2Started && (
        <div className="mt-4 border border-gray-700 p-4 rounded">
          <h3 className="font-bold mb-2">Stage 2 Pipeline</h3>
          <div className="text-sm">
            <div className="bg-gray-800 p-2 mb-2 rounded">Taxonomy: Complete</div>
            <div className="bg-gray-800 p-2 mb-2 rounded">Defect Hypothesis: Conformal Calibration Applied (N=3)</div>
            {comparableHighlight && (
              <div className="bg-yellow-600 text-black font-bold p-2 mb-2 rounded">
                Deterministic selection from KG (LLM did NOT pick this anchor)
              </div>
            )}
            <div className="bg-gray-800 p-2 mb-2 rounded">Risk: Complete</div>
            <div className="bg-gray-800 p-2 mb-2 rounded">Approach: Complete</div>
          </div>
        </div>
      )}
      
      {stage2Complete && (
        <div className="mt-4 p-2 bg-green-800 rounded flex justify-between">
          <div className="text-sm font-bold">Byte Density Cover: &ge; 0.60</div>
          <div className="text-sm font-bold">Cost: ~$0.037</div>
        </div>
      )}
    </div>
  );
}
