// Mirror of packages/scoring/weights.py — kept in sync manually.
// These constants drive the deterministic Stage 1 fitness scoring per
// packages/scoring/fitness.py. The frontend uses them to render the
// per-prospect score-breakdown tooltip so the math is transparent
// (vs. opaque) to any technical reviewer.
//
// If the backend weights change, this file must be updated to match.
// CI / pre-commit grep for these constant names should land in Phase 1.7
// to guarantee no drift.
//
// Verified against packages/scoring/weights.py via Nia read at commit
// time: 0.40 / 0.25 / 0.20 / 0.15.

export const VERTICAL_MATCH_WEIGHT = 0.40;
export const SIZE_BAND_WEIGHT = 0.25;
export const TRADE_SHOW_PROVENANCE_WEIGHT = 0.20;
export const CAPACITY_DECAY_WEIGHT = 0.15;

export interface FitnessBreakdownInput {
  vertical: string;
  factory_size_band: string;
  trade_show_provenance: boolean;
  capacity_decay: number; // 0.0 to 1.0
}

export interface FitnessBreakdownComponent {
  label: string;
  contribution: number;
  contributes: boolean;
}

/**
 * Compute the per-component breakdown for a prospect's fitness score.
 * Mirrors packages/scoring/fitness.py.compute_fitness exactly.
 */
export function computeFitnessBreakdown(
  input: FitnessBreakdownInput
): FitnessBreakdownComponent[] {
  const verticalMatches =
    input.vertical !== 'out_of_vertical' && input.vertical !== 'vertical_uncertain';
  const sizeBandMatches =
    input.factory_size_band === 'medium' || input.factory_size_band === 'large';
  const capacityFactor = 1 - input.capacity_decay;

  return [
    {
      label: `vertical_match (${input.vertical})`,
      contribution: verticalMatches ? VERTICAL_MATCH_WEIGHT : 0,
      contributes: verticalMatches,
    },
    {
      label: `size_band (${input.factory_size_band})`,
      contribution: sizeBandMatches ? SIZE_BAND_WEIGHT : 0,
      contributes: sizeBandMatches,
    },
    {
      label: 'trade_show_provenance',
      contribution: input.trade_show_provenance ? TRADE_SHOW_PROVENANCE_WEIGHT : 0,
      contributes: input.trade_show_provenance,
    },
    {
      label: `capacity_decay × (1 - ${input.capacity_decay.toFixed(1)})`,
      contribution: CAPACITY_DECAY_WEIGHT * capacityFactor,
      contributes: capacityFactor > 0,
    },
  ];
}
