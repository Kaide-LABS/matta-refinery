// Registry of seeded trade-show CSVs the Run Demo button can pick from.
// Each CSV must contain a row at external_lead_id=W001 with
// company_name="William Cook Sheffield" — this is the constant tracer the
// click-to-Stage-2 flow fires on. The supporting prospects (W002+) vary by
// trade-show theme so the demo reads as input-resilient across runs.
//
// source_label is intentionally constant ("uk_metals_expo_2025") across all
// CSVs so the deterministic prospect_id derivation
// (`pros_<md5(source_label:external_lead_id)>`) keeps William Cook's
// prospect_id stable at pros_9cb419495484 — required for the hardcoded
// click handler in useDemoState.

export interface SeedCsv {
  id: string;
  filename: string;
  publicPath: string;
  tradeShowDisplay: string;
  dougMessage: string;
  approxLeadCount: number;
}

export const SEED_CSVS: SeedCsv[] = [
  {
    id: 'uk_metals_expo',
    filename: 'UK_Metals_Expo_2025_leads.csv',
    publicPath: '/seed_csvs/UK_Metals_Expo_2025_leads.csv',
    tradeShowDisplay: 'UK Metals Expo 2025',
    dougMessage: 'UK Metals Expo batch — can someone triage?',
    approxLeadCount: 124,
  },
  {
    id: 'hannover_messe',
    filename: 'Hannover_Messe_2025_leads.csv',
    publicPath: '/seed_csvs/Hannover_Messe_2025_leads.csv',
    tradeShowDisplay: 'Hannover Messe 2025',
    dougMessage: 'Hannover Messe batch — can someone triage?',
    approxLeadCount: 110,
  },
  {
    id: 'imts_chicago',
    filename: 'IMTS_Chicago_2025_leads.csv',
    publicPath: '/seed_csvs/IMTS_Chicago_2025_leads.csv',
    tradeShowDisplay: 'IMTS Chicago 2025',
    dougMessage: 'IMTS Chicago batch — can someone triage?',
    approxLeadCount: 95,
  },
  {
    id: 'industrial_ai_summit',
    filename: 'Industrial_AI_Summit_2025_leads.csv',
    publicPath: '/seed_csvs/Industrial_AI_Summit_2025_leads.csv',
    tradeShowDisplay: 'Industrial AI Summit 2025',
    dougMessage: 'Industrial AI Summit batch — can someone triage?',
    approxLeadCount: 78,
  },
  {
    id: 'forging_convention',
    filename: 'Forging_Industry_Convention_2025_leads.csv',
    publicPath: '/seed_csvs/Forging_Industry_Convention_2025_leads.csv',
    tradeShowDisplay: 'Forging Industry Convention 2025',
    dougMessage: 'Forging Industry Convention batch — can someone triage?',
    approxLeadCount: 102,
  },
];

export function pickRandomSeedCsv(): SeedCsv {
  const idx = Math.floor(Math.random() * SEED_CSVS.length);
  return SEED_CSVS[idx];
}

// Default for first render before Run Demo has fired — UK Metals Expo is the
// canonical / headline demo and reads as the "right" starting state.
export const DEFAULT_SEED_CSV: SeedCsv = SEED_CSVS[0];
