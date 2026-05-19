import { useEffect } from 'react';
import type { DemoPhase } from './useWebSocket';

// Mutate document.title in response to demo phase so a presenter who has
// tabbed away can glance at the tab strip and know where the demo is.
//
// Prefix codes:
//   (•) — in-flight (ingesting, stage1, stage2_requesting, stage2)
//   (✓) — milestone reached (stage1_complete, complete)
//   (!) — error
//   no prefix — idle
const BASE = 'Matta Refinery · Theater Console';

function prefixForPhase(phase: DemoPhase): string {
  switch (phase) {
    case 'idle':
      return '';
    case 'ingesting':
    case 'stage1':
    case 'stage2_requesting':
    case 'stage2':
      return '(•) ';
    case 'stage1_complete':
    case 'complete':
      return '(✓) ';
    case 'error':
      return '(!) ';
    default:
      return '';
  }
}

export function useTabTitle(phase: DemoPhase): void {
  useEffect(() => {
    if (typeof document === 'undefined') return;
    document.title = `${prefixForPhase(phase)}${BASE}`;
  }, [phase]);
}
