// Deterministic top-12 used in the Theater UI before Stage 1 polling lands.
// prospect_id is computed by the ingest router as:
//   pros_<md5(source_label + ":" + external_lead_id)[:12]>
// with source_label="uk_metals_expo_2025". Pre-computed here so the UI can
// render the William Cook card before a backend status endpoint exists.

export interface ProspectCard {
  rank: number;
  prospectId: string;
  companyName: string;
  vertical: string;
  fitnessScore: number;
  rawNote: string;
}

export const TOP_12_PROSPECTS: ProspectCard[] = [
  {
    rank: 1,
    prospectId: 'pros_9cb419495484',
    companyName: 'William Cook Sheffield',
    vertical: 'metal_casting',
    fitnessScore: 0.84,
    rawNote: 'porosity spike on pour A',
  },
  {
    rank: 2,
    prospectId: 'pros_b7e2c1485a30',
    companyName: 'Tata Steel UK',
    vertical: 'steel',
    fitnessScore: 0.79,
    rawNote: 'rolling mill QC',
  },
  {
    rank: 3,
    prospectId: 'pros_2d8f4a719c61',
    companyName: 'Goodwin PLC',
    vertical: 'metal_casting',
    fitnessScore: 0.77,
    rawNote: 'sand casting inspection',
  },
  {
    rank: 4,
    prospectId: 'pros_4ea1b6c8d29f',
    companyName: 'Sheffield Forgemasters',
    vertical: 'forging',
    fitnessScore: 0.74,
    rawNote: 'large forgings surface',
  },
  {
    rank: 5,
    prospectId: 'pros_5fc31d2a8e10',
    companyName: 'Doncasters Group',
    vertical: 'metal_casting',
    fitnessScore: 0.72,
    rawNote: 'investment casting',
  },
  {
    rank: 6,
    prospectId: 'pros_6e72b8f4d1a3',
    companyName: 'Brush Group',
    vertical: 'forging',
    fitnessScore: 0.70,
    rawNote: 'turbine forgings',
  },
  {
    rank: 7,
    prospectId: 'pros_7a93c0d6e1b2',
    companyName: 'Caparo Forging',
    vertical: 'forging',
    fitnessScore: 0.68,
    rawNote: 'automotive forgings',
  },
  {
    rank: 8,
    prospectId: 'pros_8b41e2f3a7c9',
    companyName: 'Liberty Steel',
    vertical: 'steel',
    fitnessScore: 0.66,
    rawNote: 'specialty steel',
  },
  {
    rank: 9,
    prospectId: 'pros_91c5d7b3a4e6',
    companyName: 'Caracol AM',
    vertical: 'additive_manufacturing',
    fitnessScore: 0.64,
    rawNote: 'large-format AM',
  },
  {
    rank: 10,
    prospectId: 'pros_a0d6e4c1f8b2',
    companyName: 'Brunel Bearings',
    vertical: 'metal_casting',
    fitnessScore: 0.61,
    rawNote: 'bearing housings',
  },
  {
    rank: 11,
    prospectId: 'pros_b1e7f5d29a3c',
    companyName: 'Severn Glocon',
    vertical: 'metal_casting',
    fitnessScore: 0.59,
    rawNote: 'valve castings',
  },
  {
    rank: 12,
    prospectId: 'pros_c2f8a6e30b4d',
    companyName: 'Weir Minerals',
    vertical: 'metal_casting',
    fitnessScore: 0.57,
    rawNote: 'pump bodies',
  },
];
