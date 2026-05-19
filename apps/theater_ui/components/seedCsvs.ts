// Registry of seeded trade-show CSVs the Run Demo button can pick from.
// Each CSV has a distinct rank-1 tracer prospect tuned to land at the top of
// the Stage 1 fitness ranking (medium/large size + clean vertical match +
// trade_show_provenance populated). The supporting prospects vary by
// trade-show theme so the demo reads as input-resilient across runs.
//
// source_label is intentionally constant ("uk_metals_expo_2025") across all
// CSVs so the prospect_id derivation
// (`pros_<md5(source_label:external_lead_id)>`) stays deterministic per
// external_lead_id. The /api/batch/{batch_id}/top_prospect endpoint
// (added in Phase 1.6 follow-on Commit 2) returns the actual rank-1
// prospect for the currently-running batch — the front-end click handler
// reads from that endpoint rather than hardcoding any single prospect_id.

export interface SeedCsv {
  id: string;
  filename: string;
  publicPath: string;
  tradeShowDisplay: string;
  dougMessage: string;
  approxLeadCount: number;
  tracerCompany: string;
}

export const SEED_CSVS: SeedCsv[] = [
  {
    id: 'uk_metals_expo',
    filename: 'UK_Metals_Expo_2025_leads.csv',
    publicPath: '/seed_csvs/UK_Metals_Expo_2025_leads.csv',
    tradeShowDisplay: 'UK Metals Expo 2025',
    dougMessage: 'UK Metals Expo batch — can someone triage?',
    approxLeadCount: 124,
    tracerCompany: 'William Cook Sheffield',
  },
  {
    id: 'hannover_messe',
    filename: 'Hannover_Messe_2025_leads.csv',
    publicPath: '/seed_csvs/Hannover_Messe_2025_leads.csv',
    tradeShowDisplay: 'Hannover Messe 2025',
    dougMessage: 'Hannover Messe batch — can someone triage?',
    approxLeadCount: 120,
    tracerCompany: 'Brüggen Metallwerke GmbH',
  },
  {
    id: 'imts_chicago',
    filename: 'IMTS_Chicago_2025_leads.csv',
    publicPath: '/seed_csvs/IMTS_Chicago_2025_leads.csv',
    tradeShowDisplay: 'IMTS Chicago 2025',
    dougMessage: 'IMTS Chicago batch — can someone triage?',
    approxLeadCount: 95,
    tracerCompany: 'Lockheed Martin Aeronautics Fort Worth',
  },
  {
    id: 'industrial_ai_summit',
    filename: 'Industrial_AI_Summit_2025_leads.csv',
    publicPath: '/seed_csvs/Industrial_AI_Summit_2025_leads.csv',
    tradeShowDisplay: 'Industrial AI Summit 2025',
    dougMessage: 'Industrial AI Summit batch — can someone triage?',
    approxLeadCount: 65,
    tracerCompany: 'Caracol Aerospace Division',
  },
  {
    id: 'forging_convention',
    filename: 'Forging_Industry_Convention_2025_leads.csv',
    publicPath: '/seed_csvs/Forging_Industry_Convention_2025_leads.csv',
    tradeShowDisplay: 'Forging Industry Convention 2025',
    dougMessage: 'Forging Industry Convention batch — can someone triage?',
    approxLeadCount: 90,
    tracerCompany: 'Yorkshire Casting Co',
  },
];

export function pickRandomSeedCsv(): SeedCsv {
  const idx = Math.floor(Math.random() * SEED_CSVS.length);
  return SEED_CSVS[idx];
}

// Default for first render before Run Demo has fired — UK Metals Expo is the
// canonical / headline demo and reads as the "right" starting state.
export const DEFAULT_SEED_CSV: SeedCsv = SEED_CSVS[0];
