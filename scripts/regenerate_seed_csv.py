#!/usr/bin/env python3
"""Phase 1.6 follow-on — realistic data across all 5 trade-show CSVs.

Generates the seeded CSVs under apps/theater_ui/public/seed_csvs/ from a
single parameterized script. Each CSV gets a distinct cohort matching the
trade show's industry character + a deterministic tracer at row 1.

Usage:
    python3 scripts/regenerate_seed_csv.py <csv_id>
    python3 scripts/regenerate_seed_csv.py all

csv_id values:
    uk_metals_expo                  → UK_Metals_Expo_2025_leads.csv (124 rows)
    hannover_messe                  → Hannover_Messe_2025_leads.csv (120 rows)
    imts_chicago                    → IMTS_Chicago_2025_leads.csv (95 rows)
    industrial_ai_summit            → Industrial_AI_Summit_2025_leads.csv (65 rows)
    forging_industry_convention     → Forging_Industry_Convention_2025_leads.csv (90 rows)

Per-CSV tracer (row 1) is tuned to land deterministically rank-1 via the
fitness scoring (packages/scoring/fitness.py rewards vertical_match +
medium/large size + trade_show_provenance). Each tracer ticks all three.

Generation rules per CSV (uniform):
- contact_name: ~80% populated (UK / South Asian / Eastern European /
  Continental EU / Caribbean mix per the trade show's regional character)
- contact_email: ~90% populated, ~5% deliberately malformed (truncated or
  missing domain), ~5% empty
- sector_hint: ~85% populated free-text scanner output, ~10% "unknown"
  ambiguity
- factory_size_band: small ~30% / medium ~40% / large ~30%
  (NO "enterprise" — packages/schemas/lead_intake.py rejects it)
- raw_notes: ~35% populated with realistic interest signals
- NO "Synthetic Company N" placeholders, NO "(generated)" markers
- Deterministic random seed per CSV — re-runnable produces byte-identical
  output

Damjan-auditability: every cohort, every name list, every distribution
rule is visible in this script. No magic. No fixture files to chase down.
"""

import csv
import random
import sys
from pathlib import Path
from typing import Optional, Tuple, List

# ─────────────────────────────────────────────────────────────────────────────
# Generic helpers — name pools, sizing distribution, raw note templates
# ─────────────────────────────────────────────────────────────────────────────

SIZE_BANDS = [
    ("small", 0.30),
    ("medium", 0.40),
    ("large", 0.30),
]

RAW_NOTE_TEMPLATES_GENERIC = [
    "asked about porosity detection retrofit",
    "currently using vendor X for inspection",
    "interested in retrofit, not new install",
    "decision maker not at booth — follow up",
    "saw N=3 ensemble methodology — recognises Brion's work",
    "cycle time pressure; scrap rate priority",
    "wants conformal coverage statement for audit",
    "Tier 2 supplier; OEM mandate driving inspection upgrade",
    "post-process inspection scope; HIP'd parts",
    "calibration drift between morning and afternoon shifts",
    "interested in calibration substrate methodology",
    "expansion planned for next fiscal year",
    "previous vendor missed defects on production run",
    "compliance audit driving inspection investment",
]


def email_from_name(first: str, last: str, domain_hint: str, suffix_choices: List[str]) -> str:
    handle = f"{first.lower()[:1]}.{last.lower()}"
    domain = (
        domain_hint.lower()
        .replace(" ", "")
        .replace("&", "and")
        .replace("'", "")
        .replace(",", "")
        .replace("(", "")
        .replace(")", "")
        .replace(".", "")[:26]
    )
    suffix = random.choice(suffix_choices)
    return f"{handle}@{domain}{suffix}"


def pick_size_band() -> str:
    r = random.random()
    cumulative = 0.0
    for band, weight in SIZE_BANDS:
        cumulative += weight
        if r < cumulative:
            return band
    return "small"


# ─────────────────────────────────────────────────────────────────────────────
# Name pools
# ─────────────────────────────────────────────────────────────────────────────

UK_FIRST = [
    "James", "Sarah", "David", "Emma", "Robert", "Claire", "Andrew", "Rachel",
    "Michael", "Lisa", "Paul", "Hannah", "Ian", "Joanna", "Mark", "Susan",
    "Daniel", "Catherine", "Christopher", "Karen", "Steven", "Elizabeth",
    "Anthony", "Helen", "Matthew", "Rebecca", "Stephen", "Amy", "Richard",
    "Charlotte", "Peter", "Sophie", "Patrick", "Eleanor", "Niall", "Aisling",
    "Raj", "Priya", "Anand", "Meera", "Vikram", "Anita", "Ashwin", "Deepa",
    "Faisal", "Saima", "Imran", "Zara", "Tariq", "Yasmin",
    "Tomasz", "Magda", "Stefan", "Kasia", "Marek", "Eva", "Janusz", "Ola",
    "Adebayo", "Funmi", "Kwame", "Chioma", "Marcus", "Joelle",
]
UK_LAST = [
    "Smith", "Jones", "Brown", "Taylor", "Wilson", "Davies", "Robinson",
    "Wright", "Walker", "Hall", "Wood", "Harris", "Martin", "Clark",
    "Patel", "Singh", "Khan", "Shah", "Ahmed", "Hussain", "Rashid",
    "Kowalski", "Nowak", "Wojcik", "Adamski",
    "Okafor", "Mensah", "Boateng",
    "Mackenzie", "Macdonald", "Campbell", "Murray", "Stewart",
    "O'Connor", "O'Brien", "Murphy", "Kelly", "Quinn",
    "Henderson", "Bennett", "Foster", "Walker", "Bailey", "Reed",
]

DE_FIRST = [
    "Andreas", "Nadia", "Jens", "Ursula", "Jürgen", "Stefan", "Helena", "Marta",
    "Klaus", "Wolfgang", "Ingrid", "Karoline", "Helmut", "Annika", "Bernd",
    "Sabine", "Dieter", "Petra", "Heinrich", "Birgit", "Gunther", "Heike",
    "Marek", "Eva", "Tomáš", "Magdalena",  # Polish / Czech communities in DE
    "Mehmet", "Ayşe", "Burak", "Esra",  # Turkish-German community
    "Hans", "Brigitte", "Erik", "Sofia", "Tobias", "Lena",
]
DE_LAST = [
    "Köhler", "Hofmann", "Brandt", "Weber", "Schmidt", "Becker", "Fischer",
    "Lange", "Müller", "Hartmann", "Stein", "Bauer", "Schneider", "Wagner",
    "Schulz", "Hoffmann", "Klein", "Wolf", "Neumann", "Schwarz", "Zimmermann",
    "Krüger", "Hofer", "Berg", "Schäfer",
    "Kowalski", "Novak", "Yılmaz", "Demir", "Öztürk",  # diaspora surnames
]

US_FIRST = [
    "John", "Mary", "Robert", "Patricia", "Michael", "Linda", "William",
    "Barbara", "David", "Susan", "Richard", "Jessica", "Joseph", "Karen",
    "Thomas", "Sarah", "Christopher", "Lisa", "Charles", "Nancy",
    "Carlos", "Maria", "Jose", "Ana", "Luis", "Sofia",  # Hispanic-American
    "Raj", "Priya", "Arjun", "Anjali",  # Indian-American
    "DeShawn", "Aaliyah", "Marcus", "Imani",  # African-American
    "Daniel", "Rachel", "Benjamin", "Hannah",
]
US_LAST = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Patel", "Shah", "Singh", "Khan",
    "Washington", "Jefferson", "Carter", "Mitchell",
    "Nguyen", "Tran", "Le", "Phan",
]

IT_FIRST = [
    "Marco", "Giulia", "Francesco", "Sara", "Alessandro", "Chiara", "Lorenzo",
    "Martina", "Davide", "Federica", "Stefano", "Valentina", "Paolo", "Elena",
    "Andrea", "Sofia",
]
IT_LAST = [
    "Rossi", "Russo", "Ferrari", "Esposito", "Bianchi", "Romano", "Colombo",
    "Ricci", "Marino", "Greco", "Bruno", "Gallo", "Conti", "De Luca",
    "Mancini", "Costa",
]


def random_name(name_pools: List[Tuple[List[str], List[str], float]]) -> str:
    """name_pools is a list of (first_names, last_names, weight) tuples.
    Returns a "First Last" name drawn from one of the pools per weight."""
    r = random.random()
    cumulative = 0.0
    for firsts, lasts, weight in name_pools:
        cumulative += weight
        if r < cumulative:
            return f"{random.choice(firsts)} {random.choice(lasts)}"
    # fallback
    firsts, lasts, _ = name_pools[-1]
    return f"{random.choice(firsts)} {random.choice(lasts)}"


# ─────────────────────────────────────────────────────────────────────────────
# CSV definitions
# ─────────────────────────────────────────────────────────────────────────────
# Each definition has:
#   filename   — relative to apps/theater_ui/public/seed_csvs/
#   id_prefix  — single-letter prefix for external_lead_id (W/H/I/A/F)
#   seed       — deterministic random.seed
#   target     — total row count target
#   tracer     — (company, sector, size, raw_notes, email_full, contact_name)
#   cohort     — list of (company, sector, size, raw_note_or_None,
#                email_or_None, contact_or_None)
#   pad_regions — list of region prefixes for padding to target count
#   pad_templates — list of (suffix_template, sector, size) for padding
#   name_pools  — list of (firsts, lasts, weight) for random padding
#   email_suffixes — list of TLDs to choose from
# ─────────────────────────────────────────────────────────────────────────────

# ╔═══ UK METALS EXPO 2025 ═══════════════════════════════════════════════════╗

UK_TRACER = (
    "William Cook Sheffield",
    "ductile iron casting",
    "medium",
    "booth-conversation:porosity-spike-on-pour-A",
    "jmitchell@wcook-sheffield.co.uk",
    "James Mitchell",
    "https://www.wcook.co.uk",  # verified canonical URL
)

UK_COHORT = [
    # Ranks 2-12 — verified real UK foundries with canonical URLs (Nia web search, Phase 1.7 Stage C-prelim).
    ("Sheffield Forgemasters", "steel foundry & open-die forging / defence & nuclear castings", "large", "currently evaluating in-line metrology vendors", "d.brennan@sheffieldforgemasters.com", "David Brennan", "https://www.sheffieldforgemasters.com"),
    ("Newby Foundries", "iron/steel/aluminium sand & investment casting", "medium", None, "claire.foster@newbyfoundries.co.uk", "Claire Foster", "https://www.newbyfoundries.co.uk"),
    ("Furniss & White Foundries", "SG iron & grey iron castings for rail and industrial", "medium", "rail OEM Tier-1", "rpatel@f-w-f.co.uk", "Rajesh Patel", "https://www.f-w-f.co.uk"),
    ("Cerdic Foundries", "Lloyds-registered sand castings / OEM Tier-1", "medium", None, "michael.walker@cerdicfoundries.co.uk", "Michael Walker", "https://www.cerdicfoundries.co.uk"),
    ("J&J Siddons", "grey & ductile (SG) iron specialists", "medium", "Tata supplier; calibration drift discussion", "amrit.singh@jjsiddons.co.uk", "Amrit Singh", "https://www.jjsiddons.co.uk"),
    ("The Boro' Foundry", "iron, steel & alloy castings / heavy industrial", "medium", None, "emma.thompson@borofoundry.co.uk", "Emma Thompson", "https://borofoundry.co.uk"),
    ("Lestercast", "investment / lost-wax casting for OEMs", "medium", "asked about bearing-race finish inspection", "p.murphy@lestercast.co.uk", "Paul Murphy", "https://lestercast.co.uk"),
    ("PI Castings", "ferrous & non-ferrous precision investment castings", "medium", None, "r.foster@pi-castings.co.uk", "Rachel Foster", "https://pi-castings.co.uk"),
    ("Investacast", "precision investment castings / aerospace & defence", "medium", "decision maker not at booth — follow up", "a.macdonald@investacast.com", "Andrew Macdonald", "https://investacast.com"),
    ("C.H. Coward Foundry", "ferrous & non-ferrous Sheffield foundry", "small", "F1 supply chain; cycle time pressure", "l.bennett@chcsheffield.co.uk", "Lisa Bennett", "https://chcsheffield.co.uk"),
    ("TD Foundry", "sand-cast foundry services / Midlands", "small", "sand-cast jobbing shop", "j.harrison@tdfoundry.co.uk", "Joanna Harrison", "https://www.tdfoundry.co.uk"),
    # Ranks 13+ — legacy real-ish names without verified URLs (fall through to derive-from-email).
    ("Goodwin PLC", "investment casting", "medium", None, "g.holdings@goodwin-plc.co.uk", "G. Holdings"),
    ("Doncasters Group", "investment casting / aerospace alloys", "large", "expanding Lincoln site Q3 2026", "supplier@doncasters.com", "Supplier Rep"),
    ("Tata Steel UK", "steel", "large", "asked about hot-strip mill QC retrofit", "s.henderson@tatasteel.com", "Sarah Henderson"),
    ("Brush Group Loughborough", "turbine generator forgings", "large", None, "m.walker@brush.co.uk", "M. Walker"),
    ("Caparo Forging", "automotive forging tier 2", "medium", None, "a.singh@caparoforge.com", "A. Singh"),
    ("Liberty Steel Rotherham", "specialty steel bar", "large", None, "e.thompson@libertysteel.com", "E. Thompson"),
    ("Brunel Bearings", "precision bearings", "medium", None, "p.murphy@brunelbearings.co.uk", "P. Murphy"),
    ("Severn Glocon", "valve castings", "medium", None, "r.foster@severnglocon.com", "R. Foster"),
    ("Weir Minerals Todmorden", "pump impeller castings", "large", None, "a.macdonald@weirgroup.com", "A. Macdonald"),
    ("Cosworth Manufacturing", "high-performance engine castings", "medium", None, "l.bennett@cosworth.com", "L. Bennett"),
    ("Renishaw Castings Division", "metrology-grade castings", "medium", None, "j.harrison@renishaw.com", "Joanna Harrison"),
    ("Hayward Tyler", "submersible motor components", "medium", "asked specifically about porosity Pareto", "s.kowalski@haywardtyler.com", "Stefan Kowalski"),
    ("Edwards Vacuum Burgess Hill", "vacuum pump castings", "large", None, "j.taylor@edwardsvacuum.com", "Joanne Taylor"),
    ("Smiths Detection Watford", "precision aerospace assemblies", "large", None, None, None),
    ("Spirit AeroSystems Belfast", "aerospace composite skins", "large", "Airbus A220 fuselage supply", "n.oconnor@spiritaero.com", "Niamh O'Connor"),
    ("Bridon-Bekaert Doncaster", "high-tensile steel cable", "medium", None, "d.chowdhury@bridon-bekaert.com", "Dipak Chowdhury"),
    ("BAE Land Systems Telford", "armoured vehicle weld inspection", "large", "OFFICIAL-SENSITIVE channel only", None, "Group inquiry"),
    ("Castings PLC Brownhills", "iron casting jobbing foundry", "medium", "cycle time spike on grade EN-GJL-300", "p.shaw@castingsplc.com", "Peter Shaw"),
    ("Yorkshire Casting Co", "ductile iron casting", "small", None, "h.kaur@yorkshirecasting.co.uk", "Harpreet Kaur"),
    ("Sheffield Castings", "iron casting", "small", None, "b.akhtar@sheffieldcastings.co.uk", "Bilal Akhtar"),
    ("Birmingham Forge Works", "drop forging", "medium", "expanding heat-treat capacity", "t.collins@bhamforge.co.uk", "Tom Collins"),
    ("Coventry Precision", "5-axis precision machining", "medium", None, "k.adamson@coventryprecision.co.uk", "Karen Adamson"),
    ("Black Country Foundry", "non-ferrous casting", "small", None, "j.evans@bcfoundry.co.uk", "Jamie Evans"),
    ("Northern Steel & Alloys", "specialty steel distribution", "small", "distributor — limited inspection scope", None, None),
    ("Manchester Iron Works", "structural iron casting", "medium", None, "f.ahmed@manchesteriron.co.uk", "Fariha Ahmed"),
    ("Wolverhampton Pressings", "deep-drawn pressings", "medium", "automotive tier 2 — surface defect priority", "g.wright@wolvepressings.co.uk", "Graham Wright"),
    ("Stoke Ceramics & Refractory", "ceramic substrate casting", "small", None, "p.bailey@stokeceramics.co.uk", "Phillip Bailey"),
    ("Leeds Cast Metals", "aluminium die casting", "medium", "Mercedes supplier; ITAR-adjacent", "i.rashid@leedscastmetals.com", "Imran Rashid"),
    ("Newcastle Steel Erectors", "structural steel fabrication", "medium", None, "h.thompson@newcastlesteel.co.uk", "Hannah Thompson"),
    ("Aero Engineering Services Bristol", "airframe component machining", "medium", "BAE / Rolls partnership", "n.fletcher@aero-bristol.com", "Nathaniel Fletcher"),
    ("Filton Composites", "aerospace composite layup", "medium", None, "z.ali@filtoncomposites.co.uk", "Zara Ali"),
    ("Prestwick Aerospace", "wing-component machining", "medium", None, "c.macleod@prestwickaero.co.uk", "Catherine Macleod"),
    ("Magellan Aerospace Wrexham", "engine component castings", "medium", "interested in N=3 ensemble methodology — saw paper", "v.kumar@magellan-wrexham.com", "Vikram Kumar"),
    ("Meggitt Aerospace Coventry", "thermal management components", "large", None, "j.allen@meggitt.com", "Jennifer Allen"),
    ("Harland & Wolff Belfast", "marine-grade plate fabrication", "large", "asked specifically about hull-section weld inspection", "d.murphy@harland-wolff.com", "Declan Murphy"),
    ("Caledonian Forge Glasgow", "shipbuilding-grade forgings", "medium", None, "m.fraser@caledonianforge.co.uk", "Mhairi Fraser"),
    ("Babcock Marine Rosyth", "submarine pressure hull", "large", "OFFICIAL-SENSITIVE — limited substrate", None, None),
    ("Clyde Engineering", "marine engineering castings", "medium", None, None, "team@clydeengineering.co.uk"),
    ("Brüggen Metallwerke GmbH", "sheet steel forming", "large", None, "a.koehler@brueggen-metall.de", "Andreas Köhler"),
    ("Klüber Lubrication Munich", "seal-grade polymer extrusion", "medium", None, "n.hofmann@klueber.com", "Nadia Hofmann"),
    ("Heller Maschinenfabrik Nürtingen", "5-axis machining centres", "medium", "wants to qualify our system for Heller line", "j.brandt@heller-machines.de", "Jens Brandt"),
    ("Doosan Heavy Changwon (UK rep)", "power-gen forgings", "large", None, None, "UK rep at booth"),
    ("Voith Hydro Heidenheim", "hydroelectric runner casting", "large", "asked about ductile cast surface qc", "u.weber@voith.com", "Ursula Weber"),
    ("Erbslöh Aluminium GmbH", "automotive aluminium extrusion", "medium", None, "j.schmidt@erbsloeh.de", "Jürgen Schmidt"),
    ("ELG Haniel Sheffield (UK subsidiary)", "stainless scrap processing", "medium", None, "s.becker@elg-haniel.co.uk", "Stefan Becker"),
    ("Triumph Group Bristol", "aerospace structures", "large", None, "t.brennan@triumphgroup-uk.com", "Tom Brennan"),
    ("Avon Protection Melksham", "ballistic helmet composites", "medium", "ITAR — limited scope discussion", None, "Booth manager"),
    ("Smiths Group Aerospace Cheltenham", "actuator forgings", "large", None, "a.morgan@smiths.com", "Anna Morgan"),
    ("Rotork Bath", "industrial actuator castings", "medium", None, "p.bennett@rotork.com", "Paul Bennett"),
    ("IMI Plc Birmingham", "fluid control valve castings", "large", "asked about porosity & dimensional drift correlation", "n.shah@imi.com", "Neil Shah"),
    ("Spectris Egham", "test & measurement assemblies", "medium", None, "a.kim@spectris.com", "Alex Kim"),
    ("Vesuvius Plc Doncaster", "refractory ceramic casting", "large", None, "h.elias@vesuvius.com", "Hossam Elias"),
    ("Bodycote Macclesfield", "heat treatment & HIP", "large", "post-process inspection of HIP'd parts", "j.davies@bodycote.com", "Julian Davies"),
    ("Independent Forgings Sheffield", "open-die heavy forging", "medium", "saw fitness scoring methodology demo", "r.singh@indepforgings.com", "Ranjit Singh"),
    ("Hawkins Forge & Stamping Walsall", "automotive stampings", "medium", None, "k.oneill@hawkinsforge.co.uk", "Kerry O'Neill"),
    ("Brookhouse Forgings Oldham", "automotive crankshafts", "medium", "decision maker requested follow-up Q2", "m.tahir@brookhouseforgings.co.uk", "Muhammad Tahir"),
    ("Special Steels Manchester", "tool steel bar", "small", None, "j.dobson@specialsteelsmcr.co.uk", "John Dobson"),
    ("RPC Group Rushden", "polymer injection mouldings", "large", None, "k.osullivan@rpc-bpi.com", "Kieran O'Sullivan"),
    ("Continental Engineering Plastics", "engineering polymer extrusion", "medium", "wall thickness drift after die wear", "m.lange@conti-eng-plastics.com", "Marta Lange"),
    ("Victrex Lancashire", "PEEK polymer extrusion", "large", "high-temp polymer; aerospace-grade", "l.holt@victrex.com", "Laura Holt"),
    ("Renishaw AM Stone", "laser powder bed fusion", "large", "Renishaw subsidiary; LPBF in-process monitoring", "g.wilkins@renishaw-am.com", "Gareth Wilkins"),
    ("LPW Technology Runcorn", "AM metal powder QC", "small", None, "h.fischer@lpwtechnology.com", "Helena Fischer"),
    ("Croft Additive Manufacturing", "AM filter components", "small", "small batch industrial AM", "d.evans@croftam.co.uk", "Daniel Evans"),
    ("Phoenix Calibration Services", "calibration substrate vendor", "small", "interested in our calibration methodology", "g.hayward@phoenix-calib.co.uk", "Grace Hayward"),
    ("Beswick Engineering Manchester", "precision sub-contract machining", "small", None, "m.kowalski@beswick.co.uk", "Marek Kowalski"),
    ("J&J Castings Glasgow", "small-batch iron casting", "small", None, "j.ferguson@jjcastings.co.uk", "Jamie Ferguson"),
    ("Heat Treatment Services Halifax", "steel heat treatment", "small", None, None, None),
    ("Wilson Welding Inspection", "weld NDT consultancy", "small", "wants to integrate with QMS — out of scope", "t.wilson@wilsonweld.co.uk", "Tom Wilson"),
    ("Penso Composites Coventry", "automotive composite layup", "medium", None, "f.bianchi@penso.co.uk", "Francesca Bianchi"),
    ("Jaguar Land Rover Castle Bromwich", "automotive body-in-white", "large", "JLR Q&A team — assembly line vision", None, None),
    ("Rolls-Royce Civil Aerospace Derby", "turbine blade investment casting", "large", "Trent series; ITAR-adjacent", None, "Group inquiry"),
    ("Airbus UK Broughton", "wing assembly inspection", "large", "Airbus A320 wing line", None, None),
    ("BAE Systems Submarines Barrow", "naval pressure hull", "large", "OFFICIAL-SENSITIVE", None, None),
    ("Nissan Sunderland", "automotive body stamping", "large", "asked about scrap rate reduction Q2 target", None, None),
    ("Toyota Manufacturing UK Burnaston", "engine machining", "large", None, None, None),
    ("Nestle Confectionery York", "food packaging", "large", "out of scope — food sector", None, None),
    ("Unilever Port Sunlight", "personal care packaging", "large", "out of scope — FMCG", None, None),
    ("Diageo Edinburgh", "whisky bottling line", "large", "interesting — global drinks brand parallel", "h.macdonald@diageo.com", "Hamish Macdonald"),
    ("Britvic Lutterworth", "beverage bottling", "large", None, "k.patel@britvic.co.uk", "Kavita Patel"),
    ("Coca-Cola Enterprises Wakefield", "beverage canning", "large", "out of scope — FMCG canning", None, None),
    ("Greenfield Metalworks", "jobbing fabrication", "small", "under 10 employees; one-off work", None, None),
    ("Steve's Welding Sheffield", "small welding shop", "small", "owner-operator; curiosity visit", None, "Steve"),
    ("Heritage Iron Foundry Devon", "artisan iron casting", "small", "art / heritage castings", "owner@heritageironfoundry.co.uk", "John Pearce"),
    ("Industrial Engineering Cambridge", "metal fabrication / sheet metal", "medium", None, "m.brown@industrial-cambridge.co.uk", "Michael Brown"),
    ("Manufacturing Solutions Reading", "aerospace + automotive tier 2", "medium", None, "k.davies@manusol.co.uk", "Kate Davies"),
    ("Precision Group Stoke", "automotive precision components", "medium", None, "p.morris@precisiongroup.co.uk", "Peter Morris"),
    ("Bowers Manufacturing", "unknown - booth signage unclear", "medium", None, "info@bowersmfg", "team"),
    ("Apex Forge & Steel", "", "medium", None, "a.thomas@", "Adam Thomas"),
    ("Northtech Limited", "unknown", "small", None, None, None),
    ("Sigma Metals", "metal processing", "medium", None, "s.metals@example", "Sigma Metals team"),
]

UK_PAD_REGIONS = [
    "Aberdeen", "Dundee", "Stirling", "Galway", "Cork", "Limerick",
    "Cardiff", "Swansea", "Bangor", "Newport", "Wrexham", "Carlisle",
    "Plymouth", "Exeter", "Brighton", "Crawley", "Reading", "Slough",
    "Luton", "Watford", "Romford", "Croydon", "Maidstone", "Canterbury",
    "Pendragon", "Albion", "Mercia", "Wessex", "Anglia", "Highland",
    "Border", "Tyne", "Wear Valley", "Pennine", "Cumbria", "Lakeland",
]
UK_PAD_TEMPLATES = [
    ("{region} Engineering", "machining", "small"),
    ("{region} Forge", "small forging", "small"),
    ("{region} Castings Ltd", "iron casting", "small"),
    ("{region} Steel Services", "steel distribution", "small"),
    ("{region} Industrial Solutions", "fabrication", "small"),
]


# ╔═══ HANNOVER MESSE 2025 ═══════════════════════════════════════════════════╗

HM_TRACER = (
    "Brüggen Metallwerke GmbH",
    "sheet steel forming",
    "large",
    "wants in-line surface-defect detection for cold-rolled coil; specific interest in stamping-press inspection retrofit",
    "a.koehler@brueggen-metall.de",
    "Andreas Köhler",
    "https://www.brueggen-metall.de",  # canonical URL inferred from email TLD; not verified via Nia
)

HM_COHORT = [
    # Ranks 2-12 — verified German/EU manufacturers with canonical URLs (Nia web search, Phase 1.7 Stage C-prelim).
    ("Schaeffler Group", "precision bearings & motion technology for automotive/industrial", "large", "Tier 1 automotive supplier; race-component inspection", "h.fischer@schaeffler.com", "Helena Fischer", "https://www.schaeffler.com"),
    ("ZF Friedrichshafen AG", "driveline & chassis Tier-1 for passenger/commercial vehicles", "large", "EV transmission housings", "m.lange@zf.com", "Marta Lange", "https://www.zf.com"),
    ("TRUMPF SE + Co. KG", "sheet-metal laser cutting & machine tool manufacturer", "large", "interested in laser-marker defect detection", "s.becker@trumpf.com", "Stefan Becker", "https://www.trumpf.com"),
    ("MAHLE GmbH", "powertrain & thermal management Tier-1 supplier", "large", "piston ring + valve seat QC", "s.hofer@mahle.com", "Sabine Hofer", "https://www.mahle.com"),
    ("KIRCHHOFF Automotive", "complex sheet-metal forming & body-in-white assemblies", "large", "BIW assembly QC", "j.brandt@kirchhoff-automotive.com", "Jens Brandt", "https://kirchhoff-automotive.com"),
    ("DMG MORI", "CNC machine tools & turning/milling centers", "large", "wants OEM-bundled inspection in next-gen machines", "b.krueger@dmgmori.com", "Bernd Krüger", "https://en.dmgmori.com"),
    ("BENTELER International AG", "tube & metal-forming Tier-1 for automotive chassis", "large", "automotive chassis tube forming", "k.bauer@benteler.com", "Karoline Bauer", "https://www.benteler.com"),
    ("Mubea (Muhr und Bender KG)", "lightweight springs & precision stamped components", "medium", "stamping-press wear monitoring", "n.hofmann@mubea.com", "Nadia Hofmann", "https://www.mubea.com"),
    ("Wagon Automotive Nagold GmbH", "press shop & body assemblies Tier-2 supplier", "medium", None, "j.schmidt@wagon-automotive.de", "Jürgen Schmidt", "https://wagon-automotive.de"),
    ("voestalpine Metal Forming", "hot-formed automotive components & tubes/sections", "large", "hot-formed safety-critical parts", "u.weber@voestalpine.com", "Ursula Weber", "https://www.voestalpine.com/metalforming/"),
    ("GKN Automotive", "driveline systems & precision forged components", "large", "driveline forging QC", "w.hartmann@gknautomotive.com", "Wolfgang Hartmann", "https://www.gknautomotive.com"),
    # Ranks 13+ — legacy entries (no verified URLs).
    ("Audi Production Ingolstadt", "automotive body-in-white", "large", "asked about scrap-rate Pareto correlation", None, "Audi quality group"),
    ("MTU Aero Engines Munich", "turbine blade investment casting", "large", "Tier-1 aero engines; ITAR-adjacent", "h.brigitte@mtu.de", "Brigitte Hoffmann"),
    ("Salzgitter Flachstahl", "hot-rolled steel coil", "large", None, "e.klein@salzgitter-flachstahl.de", "Erik Klein"),
    ("thyssenkrupp Steel Europe Duisburg", "blast furnace steelmaking", "large", "huge plant; piloting digital QC across one line", "s.wolf@thyssenkrupp.com", "Sofia Wolf"),
    ("Schmolz + Bickenbach Düsseldorf", "specialty steel forging", "large", "high-alloy steel; aerospace customers", "d.neumann@schmolz-bickenbach.com", "Dieter Neumann"),
    ("Knorr-Bremse Munich", "brake-system castings", "medium", "rail-grade brake disc inspection", "p.schwarz@knorr-bremse.com", "Petra Schwarz"),
    ("Liebherr Ehingen", "crane component machining", "large", None, "h.zimmermann@liebherr.com", "Heinrich Zimmermann"),
    ("DMG Mori Bielefeld", "machine tool manufacturing", "large", "wants OEM-bundled inspection in next-gen machines", "b.krueger@dmgmori.com", "Bernd Krüger"),
    ("Mahle Stuttgart", "engine component castings", "large", "piston ring + valve seat QC", "s.hofer@mahle.com", "Sabine Hofer"),
    ("Continental Tires Hannover", "tire production", "large", "out of scope — rubber rather than metal", None, None),
    ("Wittmann Battenfeld Polymer", "injection moulding", "medium", None, "t.berg@wittmann-group.com", "Tobias Berg"),
    ("Hella Lippstadt", "automotive lighting assemblies", "large", "headlamp lens injection moulding QC", "l.schaefer@hella.com", "Lena Schäfer"),
    ("Webasto Stockdorf", "automotive thermal systems", "medium", "sunroof glass + frame inspection", "m.demir@webasto.com", "Mehmet Demir"),
    ("Brose Coburg", "automotive door-system mechatronics", "medium", None, "a.oezturk@brose.com", "Ayşe Öztürk"),
    ("Henkel KGaA Düsseldorf", "industrial adhesives", "large", "out of scope — chemical industry", None, None),
    ("ifm electronic Essen", "industrial sensors", "medium", "supplier curiosity, not a buyer", "b.yilmaz@ifm.com", "Burak Yılmaz"),
    ("Siemens Mobility Berlin", "rail-grade castings", "large", "ICE bogie inspection", "e.demir@siemens.com", "Esra Demir"),
    ("SEW-Eurodrive Bruchsal", "gear motor castings", "large", None, "h.kowalski@sew-eurodrive.de", "Hans Kowalski"),
    ("Wagner Group Reutlingen", "industrial fasteners", "medium", "thread inspection on rolled fasteners", "j.novak@wagner-group.com", "Janusz Novak"),
    ("Putzmeister Aichtal", "concrete pump castings", "medium", None, "t.brandt@putzmeister.com", "Tomáš Brandt"),
    ("Bilstein Group Hagen", "cold-rolled steel strip", "large", "automotive door reinforcement", "m.lange@bilstein-group.com", "Magdalena Lange"),
    ("Bilfinger Mannheim", "industrial plant fabrication", "large", "process plant tank inspection", "u.weber@bilfinger.com", "Ursula Weber"),
    ("Buderus Edelstahl Wetzlar", "specialty tool steel", "medium", "die-steel surface finish", "k.becker@buderus-edelstahl.de", "Karoline Becker"),
    ("Saarstahl Völklingen", "rail and bar steel", "large", None, "h.mueller@saarstahl.com", "Hans Müller"),
    ("Outokumpu Krefeld", "stainless steel processing", "large", "expanding pickling line; surface QC priority", "s.kowalski@outokumpu.com", "Stefan Kowalski"),
    ("AluFlexpack Reinach", "aluminium foil packaging", "medium", "pinhole detection on foil", None, "Production team"),
    ("Aurubis Hamburg", "copper smelting & refining", "large", None, "p.zimmermann@aurubis.com", "Petra Zimmermann"),
    ("Wieland-Werke Ulm", "copper alloy extrusion", "large", "automotive connector strip", "d.wagner@wieland.com", "Dieter Wagner"),
    ("Linde Engineering Pullach", "cryogenic plant fabrication", "large", "weld quality on LNG vessels", "j.fischer@linde.com", "Jens Fischer"),
    ("KraussMaffei Munich", "polymer extrusion equipment", "medium", "OEM-bundled QC for extrusion lines", "s.bauer@kraussmaffei.com", "Sofia Bauer"),
    ("Schuler Group Göppingen", "metal forming presses", "large", "OEM partnership — wants our QC in their press cells", "a.schmidt@schulergroup.com", "Andreas Schmidt"),
    ("Komatsu Hannover", "construction equipment castings", "large", None, "h.hofmann@komatsu.com", "Heike Hofmann"),
    ("MAN Truck & Bus Munich", "commercial-vehicle castings", "large", "engine block QC at Salzgitter plant", "k.lange@man.eu", "Klaus Lange"),
    ("Voestalpine Linz", "rail and automotive steel", "large", "rail steel surface defects priority", "e.brandt@voestalpine.com", "Eva Brandt"),
    ("Kuka Augsburg", "industrial robotics", "large", "OEM partnership opportunity for inspection cells", "m.weber@kuka.com", "Magdalena Weber"),
    ("Tetra Pak Manufacturing Karlsruhe", "carton packaging", "medium", "out of scope — packaging", None, None),
    ("Müller Maschinenbau Hessen", "small machine-building shop", "small", None, "h.hofmann@mueller-mb.de", "Heinrich Hofmann"),
    ("Schmidt Präzisionsteile Stuttgart", "precision machined components", "small", "small-batch aerospace work", "p.becker@schmidt-prazi.de", "Petra Becker"),
    ("Becker Industrietechnik Bremen", "industrial fabrication", "small", None, "s.fischer@becker-it.de", "Stefan Fischer"),
    ("Hartmann Druckguss Köln", "die casting jobbing shop", "small", "owner asked about porosity baseline", "w.hartmann@hartmann-dg.de", "Wolfgang Hartmann"),
    ("Wagner Stahlbau Dresden", "structural steel fabrication", "medium", None, "k.mueller@wagner-stahl.de", "Klaus Müller"),
    ("Stein Edelstahl Bremen", "stainless steel processing", "small", None, "i.stein@stein-edelstahl.de", "Ingrid Stein"),
    ("Bauer Maschinenfabrik Augsburg", "machine building", "small", None, "k.bauer@bauer-mb.de", "Karoline Bauer"),
    ("Schneider Werkzeugbau", "tool & die making", "small", None, "h.brigitte@schneider-wz.de", "Brigitte Schneider"),
    ("Wagner Industrieservice", "industrial maintenance", "small", "service company, not buyer", None, None),
    ("Schulz Metallbau Hannover", "metal fabrication", "small", None, "t.schulz@schulz-metall.de", "Tobias Schulz"),
    ("Hoffmann Stahl Westfalen", "steel service centre", "medium", "distributor — limited inspection scope", None, None),
    ("Klein Industriewerke", "industrial components", "small", None, "e.klein@klein-iw.de", "Erik Klein"),
    ("Wolf Maschinenbau Bayern", "machine tooling", "small", None, "s.wolf@wolf-mb.de", "Sofia Wolf"),
    ("Neumann Stahlguss", "steel casting", "small", "small foundry; jobbing work", "d.neumann@neumann-stahl.de", "Dieter Neumann"),
    ("Schwarz Engineering", "precision engineering", "small", None, "p.schwarz@schwarz-eng.de", "Petra Schwarz"),
    ("Zimmermann Druckguss", "die casting", "small", None, "h.zimmermann@zimm-dg.de", "Heinrich Zimmermann"),
    ("Krüger Stahlbau Ruhr", "structural steel", "medium", None, "b.krueger@krueger-stahl.de", "Bernd Krüger"),
    ("Hofer Gussteile", "iron casting", "small", None, "s.hofer@hofer-guss.de", "Sabine Hofer"),
    ("Berg Industriebau", "industrial construction", "small", None, "t.berg@berg-ib.de", "Tobias Berg"),
    ("Schäfer Walzwerk Köln", "steel rolling mill", "medium", "expansion plan 2026", "l.schaefer@schaefer-walz.de", "Lena Schäfer"),
    # Polish / Eastern European subsidiaries with German operations
    ("Kowalski Präzision Berlin", "polish-owned precision machining", "small", None, "h.kowalski@kowalski-prazi.de", "Hans Kowalski"),
    ("Novak Stahlbau Hamburg", "structural steel", "small", None, "j.novak@novak-stahl.de", "Janusz Novak"),
    # Turkish-German cluster
    ("Yılmaz Metallwerke Köln", "metal fabrication", "small", None, "b.yilmaz@yilmaz-metall.de", "Burak Yılmaz"),
    ("Demir Industrietechnik Berlin", "industrial components", "small", None, "m.demir@demir-it.de", "Mehmet Demir"),
    ("Öztürk Stahlhandel", "steel trading", "small", "distributor", None, None),
    # AM cluster
    ("EOS GmbH Krailling", "laser powder bed fusion", "large", "AM machine OEM — partnership prospect", "e.demir@eos.info", "Esra Demir"),
    ("Concept Laser Lichtenfels", "laser powder bed fusion", "medium", "GE Additive subsidiary", "a.koehler@conceptlaser.com", "Andreas Köhler"),
    ("SLM Solutions Lübeck", "laser powder bed fusion", "medium", "AM machine OEM", "n.hofmann@slm-solutions.com", "Nadia Hofmann"),
    # Polymer & glass
    ("BASF Schwarzheide Polymer", "polymer compounding", "large", "out of scope — chemical", None, None),
    ("Schott AG Mainz", "specialty glass", "large", "pharmaceutical vial inspection — interesting parallel", "j.brandt@schott.com", "Jens Brandt"),
    ("Bystronic Laser Niederönz", "laser sheet metal cutting", "medium", "Swiss subsidiary at booth", "u.weber@bystronic.com", "Ursula Weber"),
    # Italian subsidiaries
    ("Caracol AM (DE booth)", "additive manufacturing", "medium", "Italian; large-format AM cell QC", "m.rossi@caracol-am.com", "Marco Rossi"),
    # Niche / micro
    ("3D-Druck Werkstatt München", "small AM service bureau", "small", None, "h.fischer@3d-druck-mue.de", "Helena Fischer"),
    ("Industrievision GmbH", "vision system integrator", "small", "competitor — limited engagement", None, None),
    # Out of vertical / scope
    ("Bayer Pharma Leverkusen", "pharmaceutical", "large", "out of scope — pharma", None, None),
    ("Lufthansa Technik Hamburg", "aircraft MRO", "large", "engine overhaul inspection — interesting", "m.lange@lufthansa-technik.com", "Magdalena Lange"),
    ("Deutsche Bahn Werke", "rail rolling stock maintenance", "large", None, None, "DB engineering team"),
    ("VW Wolfsburg", "automotive body-in-white", "large", "huge plant — initial scoping conversation", None, "VW production engineering"),
    ("Porsche Stuttgart Production", "engine machining", "large", "specialty engine block QC", "k.lange@porsche.com", "Klaus Lange"),
    # Polymer detail
    ("Röchling Polymer Mannheim", "engineering polymer extrusion", "medium", None, "h.becker@roechling.com", "Hans Becker"),
    ("Igus Köln", "polymer plain bearings", "medium", None, "p.schwarz@igus.com", "Petra Schwarz"),
    ("Boge Kompressoren Bielefeld", "compressor castings", "medium", None, "s.bauer@boge.com", "Sofia Bauer"),
    # Glass
    ("Verallia Stahlglas Mannheim", "container glass manufacturing", "large", "pharma vial inspection priority", "t.schulz@verallia.com", "Tobias Schulz"),
    ("Schott Pharma Mainz", "pharmaceutical glass vials", "medium", "high-speed bottling line QC", "j.fischer@schottpharma.com", "Jens Fischer"),
    ("Heinz Glas Kleintettau", "luxury cosmetic glass", "medium", None, "i.stein@heinz-glas.de", "Ingrid Stein"),
    # Final regional pad
    ("Frankfurt Stahlbau", "structural steel", "small", None, "k.bauer@frankfurt-stahl.de", "Karoline Bauer"),
    ("Stuttgart Präzisionsteile", "precision components", "small", None, "h.brigitte@stuttgart-prazi.de", "Brigitte Hartmann"),
    ("Dresden Maschinen GmbH", "machine building", "small", None, "w.hartmann@dresden-mb.de", "Wolfgang Hartmann"),
    ("Leipzig Edelstahl", "stainless steel processing", "small", None, "m.demir@leipzig-edel.de", "Mehmet Demir"),
]

HM_PAD_REGIONS = [
    "Karlsruhe", "Mannheim", "Wiesbaden", "Würzburg", "Augsburg", "Bremen",
    "Hannover", "Münster", "Bonn", "Aachen", "Mainz", "Trier",
    "Salzburg", "Wien", "Zürich", "Basel", "Genf", "Bern",
]
HM_PAD_TEMPLATES = [
    ("{region} Stahlbau GmbH", "structural steel", "small"),
    ("{region} Maschinen", "machining", "small"),
    ("{region} Industrie", "fabrication", "small"),
    ("{region} Werkzeugbau", "tool making", "small"),
    ("{region} Präzisionsteile", "precision parts", "small"),
]


# ╔═══ IMTS CHICAGO 2025 ═════════════════════════════════════════════════════╗

IMTS_TRACER = (
    "Lockheed Martin Aeronautics Fort Worth",
    "aerospace structural machining",
    "large",
    "F-35 forward fuselage machining; specific interest in titanium-machining surface defect detection at 2.5x scale",
    "j.washington@lockheedmartin.com",
    "John Washington",
    "https://www.lockheedmartin.com",  # verified canonical URL
)

IMTS_COHORT = [
    # Ranks 2-12 — verified US aerospace/defense/precision-machining suppliers (Nia web search, Phase 1.7 Stage C-prelim).
    ("Precision Castparts Corp.", "complex metal castings & forgings for aerospace", "large", "engine component castings", "m.jefferson@precast.com", "Marcus Jefferson", "https://www.precast.com"),
    ("Howmet Aerospace", "engine components, fastening systems & structural castings", "large", "turbine airfoil casting QC", "p.singh@howmet.com", "Priya Singh", "https://www.howmet.com"),
    ("Moog Inc.", "precision motion-control actuators for aerospace/defense", "large", "actuator gear-train inspection", "r.patel@moog.com", "Raj Patel", "https://www.moog.com"),
    ("Spirit AeroSystems", "aerostructures Tier-1 (fuselages, wings, nacelles)", "large", "Boeing 787 fuselage section", "l.miller@spiritaero.com", "Linda Miller", "https://www.spiritaero.com"),
    ("Kratos Defense & Security Solutions", "unmanned systems & defense technology manufacturing", "medium", "UAV airframe surface QC", "d.carter@kratosdefense.com", "DeShawn Carter", "https://www.kratosdefense.com"),
    ("Woodward Inc.", "aircraft engine fuel & motion control systems", "large", "fuel-system precision machining", "j.smith@woodward.com", "John Smith", "https://www.woodward.com"),
    ("HEICO Corporation", "FAA-approved aerospace replacement parts & component repair", "medium", "PMA part inspection", "a.davis@heico.com", "Anjali Davis", "https://heico.com"),
    ("TransDigm Group", "proprietary aerospace components (pumps, valves, actuators)", "large", "pump body casting QC", "m.jackson@transdigm.com", "Mary Jackson", "https://www.transdigm.com"),
    ("Curtiss-Wright Corporation", "rugged embedded computing & defense components", "large", "actuator housing QC", "t.brown@curtisswright.com", "Thomas Brown", "https://curtisswright.com"),
    ("Dynomax Inc.", "precision CNC machining for aerospace & defense", "small", None, "s.wilson@dynomaxinc.com", "Sarah Wilson", "https://www.dynomaxinc.com"),
    ("Achilles Aerospace", "AS9100-certified flight-critical precision machining", "small", "AS9100 supplier — wanting OEM-bundled QC", "r.anderson@achillesaerospace.com", "Robert Anderson", "https://www.achillesaerospace.com"),
    # Ranks 13+ — legacy entries (no verified URLs).
    ("Magellan Aerospace Middletown", "aerospace component machining", "medium", None, "k.martinez@magellan.aero", "Karen Martinez"),
    ("Trinity Industries Houston", "rail-car forging & assembly", "large", "rail-grade forging QC", "j.rodriguez@trin.net", "Jose Rodriguez"),
    ("Bell Helicopter Fort Worth", "rotorcraft machining", "large", "rotor hub inspection", "m.taylor@bellflight.com", "Michael Taylor"),
    ("Sikorsky Stratford", "rotorcraft machining", "large", "S-92 helicopter program", "s.thomas@sikorsky.com", "Susan Thomas"),
    ("Midwest Precision Forge", "automotive forging tier-2", "medium", "closed-die forging surface QC priority", "c.garcia@midwestforge.com", "Carlos Garcia"),
    ("Great Lakes Casting Co", "ferrous castings", "medium", "automotive jobbing foundry", "m.lopez@greatlakescasting.com", "Maria Lopez"),
    ("Texas Steel Fabricators Houston", "structural steel fabrication", "medium", "oil & gas structural", "l.hernandez@txsteel.com", "Luis Hernandez"),
    ("California Machining Inc Long Beach", "precision contract machining", "medium", "SpaceX supplier", "s.gonzalez@calmachining.com", "Sofia Gonzalez"),
    ("Detroit Tool & Die", "automotive tooling", "medium", None, "r.thomas@detroit-tool.com", "Richard Thomas"),
    ("Bethlehem Steel Forgings", "heavy forgings", "large", None, "w.smith@bethlehemforgings.com", "William Smith"),
    ("Cleveland-Cliffs Steel Burns Harbor", "integrated steel mill", "large", "hot strip mill surface defects priority", "p.miller@clevelandcliffs.com", "Patricia Miller"),
    ("Allegheny Technologies Pittsburgh", "specialty alloy forging", "large", "titanium & nickel alloys for aerospace", "m.davis@atimetals.com", "Michael Davis"),
    ("Carpenter Technology Reading PA", "specialty alloy steel", "large", "medical-implant grade steel", "l.garcia@cartech.com", "Linda Garcia"),
    ("Howmet Aerospace Whitehall", "investment casting aero alloys", "large", "Trent engine vane casting", "d.washington@howmet.com", "DeShawn Washington"),
    ("Precision Castparts Portland", "aerospace investment casting", "large", "high-volume jet engine blade casting", "s.singh@pccaero.com", "Sarah Singh"),
    ("Doosan Bobcat Statesville", "small machinery castings", "medium", None, "j.patel@doosanbobcat.com", "John Patel"),
    ("Komatsu America Peoria", "construction equipment machining", "medium", None, "m.rodriguez@komatsuamerica.com", "Michael Rodriguez"),
    ("CNH Industrial Racine", "agricultural machinery", "large", "combine harvester body QC", "p.jefferson@cnhind.com", "Patricia Jefferson"),
    ("Mack Trucks Macungie", "heavy truck assembly", "large", "frame rail weld inspection", "r.thomas@macktrucks.com", "Robert Thomas"),
    ("Volvo Trucks Dublin", "commercial vehicle machining", "large", None, "j.brown@volvotrucks.com", "Jessica Brown"),
    ("Hyundai Power Transformers Montgomery", "transformer core stamping", "large", "transformer lamination QC", "k.miller@hyundai-pt.com", "Karen Miller"),
    ("Siemens Energy Charlotte", "gas turbine machining", "large", "F-class turbine blade QC", "l.davis@siemens-energy.com", "Linda Davis"),
    ("GE Power Greenville SC", "gas turbine assembly", "large", "9HA turbine block QC", "t.smith@ge.com", "Thomas Smith"),
    ("Mitsubishi Power Lake Mary", "industrial turbine machining", "large", "M501 turbine blade investment casting", "s.miller@mhipsa.com", "Susan Miller"),
    ("Ford Powertrain Cleveland", "engine block machining", "large", "EcoBoost engine production", None, "Ford production QC"),
    ("GM Powertrain Tonawanda", "engine machining", "large", None, "j.washington@gm.com", "John Washington"),
    ("Stellantis Trenton Engine", "engine machining", "large", "Hemi V8 cylinder head QC", "m.taylor@stellantis.com", "Mary Taylor"),
    ("Tesla Gigafactory Texas", "EV battery + body assembly", "large", "huge facility; piloting digital QC across one line", "r.davis@tesla.com", "Raj Davis"),
    ("SpaceX Hawthorne Production", "rocket structural machining", "large", "Raptor engine block; ITAR-controlled", None, "SpaceX production team"),
    ("Rocket Lab Long Beach", "small launch vehicle structures", "medium", "Electron rocket body manufacturing", "p.gonzalez@rocketlab.com", "Priya Gonzalez"),
    ("Joby Aviation Marina", "eVTOL composite layup", "medium", "composite skin inspection priority", "s.patel@jobyaviation.com", "Sofia Patel"),
    ("Archer Aviation San Jose", "eVTOL composite manufacturing", "medium", None, "j.smith@archeraviation.com", "John Smith"),
    ("Lilium Munich (US booth)", "eVTOL ducted fan assembly", "medium", "interest in ducted fan inspection", "l.brown@lilium.com", "Linda Brown"),
    ("BAE Systems Land & Armaments York PA", "armoured vehicle production", "large", "Bradley fighting vehicle hull QC", None, "BAE production engineering"),
    ("Oshkosh Defense", "military vehicle assembly", "large", "JLTV chassis weld QC", "k.washington@oshkoshcorp.com", "Karen Washington"),
    ("L3Harris Technologies", "defense electronics machining", "large", "ITAR — limited surface", None, "L3Harris business dev"),
    ("Textron Aviation Wichita", "general aviation manufacturing", "medium", "Cessna Citation X assembly", "m.jackson@txtav.com", "Michael Jackson"),
    ("Cessna Beechcraft Wichita", "small aircraft machining", "medium", "wing component machining", "p.miller@txtav.com", "Patricia Miller"),
    ("Gulfstream Savannah", "business jet machining", "large", "G650 fuselage assembly", None, "Gulfstream production"),
    ("Bombardier Mid-Sized Wichita", "business jet machining", "medium", None, "j.davis@bombardier.com", "Jessica Davis"),
    ("Embraer Phenom Florida", "small jet structural assembly", "medium", "Phenom 300 production", "c.rodriguez@embraer.com", "Carlos Rodriguez"),
    ("Pilatus Aircraft (US ops)", "small aircraft assembly", "medium", None, None, "Pilatus US production"),
    ("United Launch Alliance Decatur", "rocket structural assembly", "large", "Vulcan Centaur production; ITAR", None, "ULA production engineering"),
    ("Blue Origin Kent", "rocket engine machining", "large", "BE-4 engine block QC; ITAR-adjacent", "r.miller@blueorigin.com", "Robert Miller"),
    ("Relativity Space Long Beach", "additive-manufactured rockets", "medium", "Terran-R AM print structural QC", "s.singh@relativityspace.com", "Sarah Singh"),
    ("Lockheed Skunk Works Palmdale", "advanced aerospace prototyping", "large", "classified; introductory conversation only", None, "Skunk Works rep"),
    ("Lawrence Livermore National Lab", "additive manufacturing R&D", "medium", None, "k.davis@llnl.gov", "Karen Davis"),
    ("Oak Ridge National Lab MDF", "manufacturing demonstration facility", "medium", "large-format AM research", "p.washington@ornl.gov", "Patricia Washington"),
    ("Sandia National Laboratory", "national security R&D", "medium", "ITAR — surface conversation only", None, None),
    ("Boeing Defense St Louis", "F-18 production", "large", "F-18 wing assembly", "m.davis@boeing.com", "Michael Davis"),
    ("Northrop Grumman Melbourne FL", "MQ-25 production", "large", None, "j.smith@ngc.com", "John Smith"),
    ("Raytheon Andover", "missile production", "large", None, "l.jefferson@raytheon.com", "Linda Jefferson"),
    ("BAE Mojave", "advanced aerospace prototyping", "medium", None, None, None),
    ("Honeywell FM&T Kansas City", "national security manufacturing", "large", "Y-12 supply chain", None, "Honeywell FM&T"),
    ("L3 Mission Integration Greenville TX", "aerospace systems integration", "medium", "C-130 modification", "t.brown@l3harris.com", "Thomas Brown"),
    ("Lockheed Aero Marietta", "C-130J production", "large", "C-130J wing center section", None, "Lockheed Marietta"),
    ("Boeing St Louis Defense", "F-15 production line", "large", None, "p.taylor@boeing.com", "Patricia Taylor"),
    ("Sierra Nevada Corp Madison WI", "aerospace systems", "medium", None, "s.thomas@sncorp.com", "Susan Thomas"),
    ("CrowdHaven Aerospace Austin", "AM aerospace startup", "small", "small contract AM, aerospace customers", "j.patel@crowdhaven.aero", "John Patel"),
    ("Hadrian Automation Torrance", "AI-augmented machining", "small", "machine shop automation startup", "r.brown@hadrian.co", "Raj Brown"),
    ("Atomic Industries Detroit", "AI-driven die machining", "small", "tooling startup; AI-augmented inspection", "m.singh@atomicindustries.com", "Marcus Singh"),
    ("Path Robotics Columbus", "autonomous welding", "small", "robot welding company", "k.davis@path-robotics.com", "Karen Davis"),
    ("Machina Labs Westlake Village", "robotic sheet metal forming", "small", "robotic forming + AI inspection", "p.jefferson@machinalabs.ai", "Patricia Jefferson"),
    ("Vulcan Forms Burlington", "AM precision parts at scale", "medium", "AM startup ramping production", "j.miller@vulcanforms.com", "Jessica Miller"),
    ("Velo3D Campbell", "AM machine OEM", "medium", "selling AM machines; partnership opportunity", "l.smith@velo3d.com", "Linda Smith"),
    ("Markforged Watertown", "AM machine OEM", "medium", None, "t.davis@markforged.com", "Thomas Davis"),
    ("Desktop Metal Burlington", "AM machine OEM", "medium", "high-throughput binder jet", "s.brown@desktopmetal.com", "Susan Brown"),
    ("Mazak North America Florence KY", "machine tool OEM", "large", "OEM-bundling opportunity", "r.miller@mazak.com", "Robert Miller"),
    ("Okuma America Charlotte", "machine tool OEM", "large", None, "j.singh@okuma.com", "John Singh"),
    ("Haas Automation Oxnard", "machine tool OEM", "large", "wants integrated QC for VMC line", "p.washington@haascnc.com", "Patricia Washington"),
    ("Hurco Indianapolis", "machine tool OEM", "medium", None, "m.thomas@hurco.com", "Michael Thomas"),
    ("Methods Machine Tools Sudbury", "machine tool integrator", "medium", None, None, "Methods sales team"),
    ("Kennametal Latrobe", "industrial cutting tools", "large", "tool wear monitoring partnership", "s.davis@kennametal.com", "Sarah Davis"),
    ("Sandvik Coromant US", "cutting tools", "large", "tool-wear ML partnership", "l.jefferson@sandvik.com", "Linda Jefferson"),
    ("Iscar Metals Arlington TX", "cutting tools", "medium", None, "j.taylor@iscar.com", "Jessica Taylor"),
    ("Heidenhain Schaumburg", "machine controls", "medium", "CNC controls partnership", "r.brown@heidenhain.com", "Raj Brown"),
    ("Fanuc America Hoffman Estates", "industrial robotics", "large", "factory automation OEM", "p.jackson@fanucamerica.com", "Patricia Jackson"),
    ("Yaskawa America Waukegan", "industrial robotics", "large", None, "k.smith@yaskawa-america.com", "Karen Smith"),
    ("Universal Robots Ann Arbor", "collaborative robots", "medium", "small-shop cobots", "s.davis@universal-robots.com", "Sarah Davis"),
    # Some out-of-scope
    ("Pepsi Bottling Plano TX", "beverage bottling", "large", "out of scope — FMCG", None, None),
    ("Procter & Gamble Cincinnati", "consumer products", "large", "out of scope — FMCG", None, None),
]

IMTS_PAD_REGIONS = [
    "Cleveland", "Pittsburgh", "Buffalo", "Rochester", "Hartford", "Boston",
    "Dallas", "Houston", "Phoenix", "Denver", "Seattle", "Portland",
]
IMTS_PAD_TEMPLATES = [
    ("{region} Machine Works", "precision machining", "small"),
    ("{region} Forge Co", "small forging", "small"),
    ("{region} Steel Products", "steel fabrication", "small"),
    ("{region} Tool & Die", "tool making", "small"),
]


# ╔═══ INDUSTRIAL AI SUMMIT 2025 ═════════════════════════════════════════════╗

AIS_TRACER = (
    "Caracol Aerospace Division",
    "large-format additive manufacturing",
    "large",
    "AM robot cell for aerospace structural prints; specifically asking about in-process layer-by-layer disposition feedback",
    "m.rossi@caracol-am.com",
    "Marco Rossi",
    "https://www.caracol-am.com",  # verified canonical URL
)

AIS_COHORT = [
    # Ranks 2-12 — verified AM / industrial AI companies with canonical URLs (Nia web search, Phase 1.7 Stage C-prelim).
    ("CEAD Group", "large-format additive manufacturing systems for aerospace/marine", "large", "AM machine OEM partnership prospect", "h.fischer@ceadgroup.com", "Helena Fischer", "https://ceadgroup.com"),
    ("Velo3D", "support-free metal 3D printing for aerospace propulsion", "large", "support-free SLM for rocket engines", "n.hofmann@velo3d.com", "Nadia Hofmann", "https://velo3d.com"),
    ("Relativity Space", "fully 3D-printed reusable rockets (Terran R)", "large", "large-format rocket-body printing", "j.brandt@relativityspace.com", "Jens Brandt", "https://relativityspace.com"),
    ("LEAP 71", "computational engineering models for AM rocket engines", "small", "computational AM engineering models", "g.wilkins@leap71.com", "Gareth Wilkins", "https://leap71.com"),
    ("Landing AI", "LandingLens deep-learning visual inspection for factories", "medium", "LandingLens for AM-process QC", "h.fischer@landing.ai", "Helena Fischer", "https://landing.ai"),
    ("Instrumental", "AI manufacturing engineering control platform / defect detection", "medium", "AM defect-detection platform", "m.miller@instrumental.com", "Mary Miller", "https://instrumental.com"),
    ("Jidoka", "turnkey vision-AI inspection for manufacturing and logistics", "small", "vision-AI inspection plug-and-play", "k.smith@jidoka-tech.ai", "Karen Smith", "https://www.jidoka-tech.ai"),
    ("Indus Vision", "AI visual inspection for zero-defect manufacturing", "small", "zero-defect production line vision", "p.singh@indusvision.ai", "Priya Singh", "https://indusvision.ai"),
    ("Allus AI", "vision foundation model for manufacturing QA", "small", "vision foundation model partnership", "r.patel@allus.ai", "Raj Patel", "https://allus.ai"),
    ("Ethon AI", "industrial AI platform for real-time process deviation analysis", "small", "process-deviation analytics platform", "s.becker@ethon.ai", "Stefan Becker", "https://www.ethon.ai"),
    ("MontBlancAI", "AI production monitoring for process manufacturers", "small", "process-manufacturer AI monitoring", "l.miller@montblanc.ai", "Linda Miller", "https://www.montblanc.ai"),
    # Ranks 13+ — legacy entries (no verified URLs).
    ("3D Systems Rock Hill", "industrial AM", "large", "DMP Factory 500 production", "j.smith@3dsystems.com", "John Smith"),
    ("Stratasys Eden Prairie", "polymer + metal AM", "large", "FDM + Origin polymer AM", "r.patel@stratasys.com", "Raj Patel"),
    ("Markforged Watertown", "composite + metal AM", "medium", "fibre-reinforced composite AM", "p.brown@markforged.com", "Patricia Brown"),
    ("Carbon Inc Redwood City", "DLS polymer AM", "medium", "L1 production printer", "s.singh@carbon3d.com", "Sarah Singh"),
    ("Desktop Metal Burlington", "binder jet metal AM", "medium", "Production System P-50", "t.davis@desktopmetal.com", "Thomas Davis"),
    ("Velo3D Campbell", "support-free LPBF", "medium", "Sapphire XC production printer", "l.smith@velo3d.com", "Linda Smith"),
    ("ExOne North Huntingdon", "binder jet AM", "medium", "Desktop Metal subsidiary", "k.davis@exone.com", "Karen Davis"),
    ("Optomec Albuquerque", "directed energy deposition AM", "medium", "LENS DED systems", "p.miller@optomec.com", "Patricia Miller"),
    ("Croft Additive Manufacturing", "small-batch AM contract manufacturing", "small", "small AM service bureau", "d.evans@croftam.co.uk", "Daniel Evans"),
    ("Bowman Additive Manchester", "AM contract manufacturing", "small", None, "j.harrison@bowmanam.com", "Joanna Harrison"),
    ("AddUp UK Sheffield", "industrial AM systems", "medium", "Michelin-Fives JV; production AM", "k.adamson@addupsolutions.com", "Karen Adamson"),
    ("Wayland Additive Huddersfield", "electron-beam AM", "small", "NeuBeam EBM technology", "g.wilkins@waylandam.com", "Gareth Wilkins"),
    ("Filamentive Bradford", "AM polymer feedstock", "small", "sustainable AM filaments", "m.singh@filamentive.com", "Meera Singh"),
    ("Caracol AM Lombardia", "large-format AM (Italian)", "medium", "robot AM cell — sister booth", "g.rossi@caracol-am.com", "Giulia Rossi"),
    ("Materialise NV Leuven", "AM software + service bureau", "large", "Magics software + AM bureau", "f.colombo@materialise.com", "Francesco Colombo"),
    ("EnvisionTEC Dearborn", "DLP polymer AM", "small", "Desktop Metal subsidiary", "s.thomas@envisiontec.com", "Susan Thomas"),
    ("Sintratec Brugg", "polymer AM", "small", "Swiss AM startup", "l.becker@sintratec.com", "Lisa Becker"),
    ("Nikon SLM Solutions (joint)", "LPBF machine manufacturing", "medium", "Nikon-SLM partnership", "j.brandt@nikon-slm.com", "Jens Brandt"),
    ("HP 3D Printing Barcelona", "MJF polymer AM", "large", "Multi Jet Fusion production", "m.lopez@hp.com", "Maria Lopez"),
    ("Trumpf TruPrint Ditzingen", "industrial laser AM", "large", "machine OEM partnership", "u.weber@trumpf.com", "Ursula Weber"),
    ("Hadrian Automation Torrance", "AI-augmented contract machining", "small", "machine shop automation", "r.singh@hadrian.co", "Raj Singh"),
    ("Atomic Industries Detroit", "AI-driven die machining", "small", "AI tooling startup", "m.davis@atomicindustries.com", "Marcus Davis"),
    ("Vulcan Forms Burlington", "high-throughput AM production", "medium", "AM production ramp; Q3 2026 expansion", "p.miller@vulcanforms.com", "Patricia Miller"),
    ("Machina Labs Westlake Village", "robotic incremental forming", "small", "robotic forming startup", None, "Machina Labs founder team"),
    ("Path Robotics Columbus", "AI welding robots", "small", "robot welding startup; QC partnership", "k.brown@path-robotics.com", "Karen Brown"),
    ("Bright Machines San Francisco", "AI software-defined manufacturing", "medium", "factory automation software", "j.taylor@brightmachines.com", "Jessica Taylor"),
    ("Sight Machine San Francisco", "manufacturing analytics platform", "medium", "data platform — partnership lens", "s.singh@sightmachine.com", "Sofia Singh"),
    ("Augury New York", "machine health AI", "medium", "predictive maintenance AI", "l.washington@augury.com", "Linda Washington"),
    ("Cogniac Berkeley", "computer vision for manufacturing", "small", "competitor — limited engagement", None, None),
    ("Drishti Mountain View", "AI assembly line analytics", "small", "assembly line AI", "p.patel@drishti.com", "Priya Patel"),
    ("Instrumental Palo Alto", "AI electronics inspection", "small", "electronics QC AI", "m.smith@instrumental.com", "Michael Smith"),
    ("ELM Mountain View", "AI factory automation", "small", None, "j.davis@elm.ai", "John Davis"),
    ("Falkonry Sunnyvale", "industrial AI time-series analytics", "small", "predictive maintenance AI", "s.jefferson@falkonry.com", "Susan Jefferson"),
    ("C3 AI Redwood City", "enterprise AI platform", "large", "out of scope — enterprise platform", None, None),
    ("PTC Boston", "PLM + AR for manufacturing", "large", "ThingWorx + Vuforia; partnership lens", "r.miller@ptc.com", "Robert Miller"),
    ("Hexagon Manufacturing Intelligence", "metrology + CAD", "large", "metrology partnership opportunity", "k.brown@hexagon.com", "Karen Brown"),
    ("Faro Technologies Orlando", "3D measurement and imaging", "medium", "metrology partnership", "p.smith@faro.com", "Patricia Smith"),
    ("Zeiss Industrial Metrology", "metrology equipment OEM", "large", "metrology OEM partnership", "h.kowalski@zeiss.com", "Helena Kowalski"),
    ("Mitutoyo America Aurora IL", "metrology + measurement", "medium", "machine tool integrator", None, "Mitutoyo sales"),
    ("Bruker Nano Tucson", "atomic force microscopy", "medium", "advanced metrology", "j.patel@bruker.com", "John Patel"),
    ("Optomec Albuquerque (booth #2)", "directed-energy deposition", "medium", "production AM", "l.davis@optomec.com", "Linda Davis"),
    ("Sciaky Chicago", "electron beam AM", "medium", "EB AM for aerospace structures", "m.washington@sciaky.com", "Marcus Washington"),
    ("Norsk Titanium Plattsburgh", "DED titanium AM", "medium", "rapid plasma deposition AM", "s.patel@norsktitanium.com", "Sarah Patel"),
    ("AddiTec Houston", "DED AM services", "small", "small DED service bureau", "r.brown@additec.com", "Raj Brown"),
    ("Lincoln Electric Additive", "wire arc AM", "medium", "WAAM technology", "j.miller@lincolnelectric.com", "Jessica Miller"),
    ("Glasstech Industrial", "industrial automation systems", "medium", None, "p.davis@glasstech.com", "Patricia Davis"),
    ("MachineMetrics Boston", "machine connectivity platform", "small", "OEE + analytics partnership", "k.singh@machinemetrics.com", "Karen Singh"),
    ("FogHorn Sunnyvale", "industrial IoT edge", "small", "Edge ML — competitor lens", None, None),
    ("Bright Wolf Cary NC", "industrial IoT platform", "small", None, "m.jefferson@brightwolf.com", "Marcus Jefferson"),
    ("Litmus Automation San Jose", "industrial IoT", "small", None, None, "Litmus sales team"),
    ("Bay Area Composites Hayward", "AM-adjacent composite manufacturing", "small", None, "j.brown@baycomposites.com", "John Brown"),
    ("OpenAI Robotics (research booth)", "robotics R&D", "small", "research-only conversation", None, "OpenAI Robotics team"),
    ("Tesla Bot Engineering (research booth)", "humanoid robotics R&D", "small", "research-only; not buyer", None, None),
    ("Anduril Industries Costa Mesa", "defense autonomy", "medium", "ITAR — surface conversation only", None, "Anduril business dev"),
    ("Shield AI San Diego", "defense AI", "small", "defense AI — limited engagement", None, None),
    ("Built Robotics San Francisco", "autonomous construction equipment", "small", "construction AI", "p.brown@builtrobotics.com", "Patricia Brown"),
    ("Saildrone Alameda", "autonomous maritime vehicles", "small", "out of scope — maritime", None, None),
    ("Apex.AI San Jose", "automotive AI middleware", "small", "automotive AI", None, "Apex.AI engineering"),
]

AIS_PAD_REGIONS = [
    "Cambridge", "Munich", "Zurich", "Boston", "Austin", "Berlin",
    "Tel Aviv", "Singapore", "Seoul",
]
AIS_PAD_TEMPLATES = [
    ("{region} AM Labs", "AM research", "small"),
    ("{region} Industrial AI", "industrial AI startup", "small"),
    ("{region} Manufacturing Robotics", "manufacturing robotics", "small"),
    ("{region} Smart Factory Solutions", "factory analytics", "small"),
]


# ╔═══ FORGING INDUSTRY CONVENTION 2025 ══════════════════════════════════════╗

FIC_TRACER = (
    "Mettis Aerospace",
    "precision forged & machined aerospace components",
    "large",
    "expanding closed-die forging cell; asking about porosity correlation between forged feedstock and final machined part",
    "d.brennan@mettis-aerospace.com",
    "David Brennan",
    "https://www.mettis-aerospace.com",  # verified canonical URL
)

FIC_COHORT = [
    # Ranks 2-12 — verified real UK forging companies with canonical URLs (Nia web search).
    ("Somers Forge", "open-die forging up to 80 tonnes / aerospace & energy", "large", "evaluating in-line metrology vendors — finalist Q3", "d.brennan@somersforge.com", "David Brennan", "https://www.somersforge.com"),
    ("Independent Forgings & Alloys", "open-die & closed-die forging / aerospace SME", "medium", "saw fitness scoring methodology demo", "r.singh@independentforgings.com", "Ranjit Singh", "https://independentforgings.com"),
    ("Bifrangi UK", "closed-die forging / agricultural & off-highway", "large", "agricultural OEM Tier-1", "p.shaw@bifrangi.co.uk", "Peter Shaw", "http://www.bifrangi.co.uk"),
    ("Brooks Forgings", "drop & upset forging / machining & fabrication", "medium", "decision maker requested follow-up Q2", "m.tahir@brooksforgings.co.uk", "Muhammad Tahir", "https://brooksforgings.co.uk"),
    ("Brockhouse Forgings", "drop-hammer forging 0.5-400kg", "medium", None, "k.oneill@brockhouse.co.uk", "Kerry O'Neill", "https://brockhouse.co.uk"),
    ("W.H. Tildesley", "drop forging / closed-die specialist", "medium", "die-wear monitoring discussion", "a.singh@whtildesley.com", "Amrit Singh", "https://www.whtildesley.com"),
    ("Abbey Forged Products", "modern forging facility / oil, gas, defence & aerospace", "medium", None, "j.patel@abbeyforgedproducts.co.uk", "James Patel", "https://www.abbeyforgedproducts.co.uk"),
    ("Kimber Mills (Kimber Drop Forgings)", "drop forging / hand tool & industrial", "small", None, "s.davies@kimbermills.co.uk", "Susan Davies", "https://www.kimbermills.co.uk"),
    ("KT Forge", "drop & open-die forging / Rotherham", "small", None, "t.brown@ktforge.co.uk", "Tom Brown", "https://ktforge.co.uk"),
    ("Cogent Steel", "open-die forgings 50kg to 50,000kg / West Yorkshire", "medium", None, "h.murphy@cogentsteel.co.uk", "Hannah Murphy", "https://www.cogentsteel.co.uk"),
    ("Intercast UK", "ISO-approved forgings & castings manufacturer", "small", "small-batch ISO 9001 supplier", "c.foster@intercastuk.com", "Claire Foster", "https://www.intercastuk.com"),
    # Ranks 13+ — legacy entries (no verified URLs).
    ("Special Steels Manchester", "tool steel forging", "small", "die-steel surface inspection", "j.dobson@specialsteelsmcr.co.uk", "John Dobson"),
    ("Cosworth Manufacturing Worcester", "high-performance forging", "medium", "F1 supply chain", "l.bennett@cosworth.com", "Lisa Bennett"),
    ("Special Steels Manchester", "tool steel forging", "small", "die-steel surface inspection", "j.dobson@specialsteelsmcr.co.uk", "John Dobson"),
    ("Cosworth Manufacturing Worcester", "high-performance forging", "medium", "F1 supply chain", "l.bennett@cosworth.com", "Lisa Bennett"),
    ("Bethlehem Steel Forgings Coatesville", "heavy forgings (US)", "large", "naval propulsion shaft forging", "w.smith@bethlehemforgings.com", "William Smith"),
    ("Cleveland-Cliffs Steel Burns Harbor", "integrated steel + forging", "large", "looking at hot-strip mill surface inspection", "p.miller@clevelandcliffs.com", "Patricia Miller"),
    ("Allegheny Technologies Pittsburgh", "specialty alloy forging", "large", "titanium aerospace forgings", "m.davis@atimetals.com", "Michael Davis"),
    ("Carpenter Technology Reading PA", "specialty alloy + forging", "large", "medical-implant-grade steel", "l.garcia@cartech.com", "Linda Garcia"),
    ("Wyman-Gordon Houston", "aerospace closed-die forging", "large", "Trent engine forgings", "j.washington@wyman-gordon.com", "John Washington"),
    ("Scot Forge Spring Grove IL", "open-die forging", "medium", "expansion planned 2026", "k.smith@scotforge.com", "Karen Smith"),
    ("Walker Forge Clintonville WI", "closed-die forging", "medium", None, "m.jefferson@walkerforge.com", "Marcus Jefferson"),
    ("Trenton Forging Michigan", "automotive forging", "medium", None, "p.brown@trentonforging.com", "Patricia Brown"),
    ("Buderus Edelstahl Wetzlar", "specialty tool steel forging", "medium", "die-steel for German automotive", "k.becker@buderus-edelstahl.de", "Karoline Becker"),
    ("Saarstahl Völklingen", "rail and bar steel forging", "large", "rail-grade steel", "h.mueller@saarstahl.com", "Hans Müller"),
    ("Outokumpu Krefeld", "stainless steel + forging", "large", "stainless forging line", "s.kowalski@outokumpu.com", "Stefan Kowalski"),
    ("Schmolz + Bickenbach Düsseldorf", "specialty steel forging", "large", "high-alloy steel for aerospace", "d.neumann@schmolz-bickenbach.com", "Dieter Neumann"),
    ("Aubert & Duval Pamiers", "nickel + titanium forging", "large", "aerospace alloys", "f.colombo@aubertduval.com", "Francesco Colombo"),
    ("ArcelorMittal Liège", "steel forging", "large", "rail-grade steel forging", "m.lange@arcelormittal.com", "Magdalena Lange"),
    ("Bharat Forge Pune (UK rep)", "automotive forging", "large", "India-based, exploring UK customers", "r.singh@bharatforge.com", "Raj Singh"),
    ("Cape Forge & Engineering Pretoria", "South African forging", "medium", None, None, "Cape Forge engineering"),
    ("Vincent Industrial Forgings Stockport", "small-batch forging", "small", None, "j.evans@vincentforge.co.uk", "Jamie Evans"),
    ("Pailton Engineering Coventry", "steering forgings", "small", None, "f.ahmed@pailton.com", "Fariha Ahmed"),
    ("Wood-Mizer Forge Indianapolis", "industrial forging", "small", None, "t.washington@woodmizerforge.com", "Tina Washington"),
    ("R.S. Stokvis Forge Rotterdam", "Dutch forging", "small", None, None, None),
    ("Hellberg Engineering Sheffield", "specialty engineering", "small", None, "h.thompson@hellberg.co.uk", "Hannah Thompson"),
    ("Hi-Tech Forge Indianapolis", "automotive forging", "medium", None, "j.smith@hitechforge.com", "John Smith"),
    ("Pratt Industries Conyers GA", "automotive forging", "medium", "wheel hub forging", "k.jefferson@prattind.com", "Karen Jefferson"),
    ("Bayou Steel Group LaPlace", "steel forging", "small", None, None, "Bayou Steel production"),
    ("Steel Dynamics Roanoke", "structural steel forging", "large", None, "p.davis@steeldynamics.com", "Patricia Davis"),
    ("Nucor Forgings Memphis", "structural steel forging", "large", None, "m.thomas@nucor.com", "Michael Thomas"),
    ("US Steel Mon Valley", "integrated steel + forging", "large", None, "r.brown@ussteel.com", "Raj Brown"),
    ("Erie Press Systems Erie PA", "forging press OEM", "medium", "press equipment + integrated QC", "j.miller@eriepress.com", "Jessica Miller"),
    ("Schuler Inc Canton MI", "metal forming presses", "large", "OEM partnership prospect", "l.smith@schulerinc.com", "Linda Smith"),
    ("SMS Group Erlangen", "forging press OEM", "large", "press OEM + monitoring", "u.weber@sms-group.com", "Ursula Weber"),
    ("Ajax Manufacturing Cleveland", "upset forging machines", "medium", None, "s.patel@ajaxmfg.com", "Sarah Patel"),
    ("Hatebur Forming Equipment Reinach", "hot former equipment", "medium", "Swiss machine builder", "h.koehler@hatebur.com", "Helena Köhler"),
    ("National Machinery Tiffin OH", "FORMAX forming machines", "medium", "fastener forming machines", "p.washington@nationalmachinery.com", "Patricia Washington"),
    ("ETS Schäfer Forging Augsburg", "automotive forging", "medium", None, "l.schaefer@ets-schaefer.de", "Lena Schäfer"),
    ("Calmet Industries Birmingham", "non-ferrous forging", "small", None, "c.macleod@calmet.co.uk", "Catherine Macleod"),
    ("Birmingham Wire & Forge", "wire + forging", "small", "wire drawing + flat forging", "g.wright@birminghamwf.co.uk", "Graham Wright"),
    ("Wexham Springs Forge", "small-batch forging", "small", "boutique forging shop", None, None),
    ("Black Country Forge Walsall", "industrial forging", "small", None, "k.adamson@bcforge.co.uk", "Karen Adamson"),
    ("Hereford Forging Co", "agricultural equipment forging", "small", None, "b.akhtar@herefordforging.co.uk", "Bilal Akhtar"),
    ("Border Forge & Steel Carlisle", "specialty forging", "small", None, None, None),
    ("Lakes Forging Cumbria", "small-batch forging", "small", None, "p.bailey@lakesforging.co.uk", "Phillip Bailey"),
    ("Caledonian Forge Glasgow", "shipbuilding-grade forging", "medium", "marine forging — Babcock supply chain", "m.fraser@caledonianforge.co.uk", "Mhairi Fraser"),
    ("Highland Forge & Steel Inverness", "specialty forging", "small", "rural — limited inspection scope", None, None),
    ("Tyne Forge Newcastle", "marine + offshore forging", "medium", "offshore wind component forging", "h.thompson@tyneforge.co.uk", "Hannah Thompson"),
    ("Wear Valley Castings", "iron casting + forging", "small", "small jobbing shop", None, None),
    ("Pennine Precision Forging", "precision forging", "small", None, "n.fletcher@penninepf.co.uk", "Nathaniel Fletcher"),
    ("Greenfield Forge Aberdeen", "oil & gas component forging", "small", "North Sea decline; pivoting to renewables", None, "Greenfield Forge ops"),
    ("Dales Forging Yorkshire", "small-batch forging", "small", None, "j.ferguson@dalesforging.co.uk", "Jamie Ferguson"),
    ("Cotswolds Engineering Bath", "precision engineering", "small", None, "k.davies@cotswoldseng.co.uk", "Kate Davies"),
    ("Surrey Surface Treatment", "post-forge surface treatment", "small", None, None, None),
    ("Kent Casting Services", "non-ferrous casting + forging", "small", None, "j.harrison@kentcasting.co.uk", "Joanna Harrison"),
    ("Essex Forge Works", "small-batch forging", "small", None, None, "Essex Forge ops"),
    ("Suffolk Steel Fabrication", "structural steel + light forging", "small", None, "p.morris@suffolksteel.co.uk", "Peter Morris"),
    ("Norfolk Iron Foundry", "iron casting + forging", "small", None, "h.kaur@norfolkfoundry.co.uk", "Harpreet Kaur"),
    ("Lincolnshire Heavy Forging", "heavy industrial forging", "medium", "wind turbine shaft forging", "i.rashid@lincolnshireforge.co.uk", "Imran Rashid"),
    ("Yorkshire Wire Drawers", "wire + light forging", "small", None, "m.brown@yorkshirewire.co.uk", "Michael Brown"),
    ("Lancashire Sheet Metal & Forge", "sheet metal + forging", "medium", None, "z.ali@lancsmetal.co.uk", "Zara Ali"),
    ("Cheshire Aluminium Forging", "aluminium forging", "medium", None, "p.bennett@cheshirealum.co.uk", "Paul Bennett"),
    ("Staffordshire Precision Forging", "precision aerospace forging", "medium", None, "f.bianchi@staffsforge.co.uk", "Francesca Bianchi"),
    ("Worcestershire Forge", "small-batch forging", "small", None, "t.collins@worcsforge.co.uk", "Tom Collins"),
    ("Shropshire Engineering Forge", "automotive forging", "small", None, "k.osullivan@shropshireforge.co.uk", "Kieran O'Sullivan"),
    ("Buckinghamshire Aerospace Forge", "aerospace forging", "medium", None, "v.kumar@bucksforge.co.uk", "Vikram Kumar"),
    ("Oxfordshire Composites & Forging", "composite + forge hybrid", "small", "hybrid composite + forged components", None, "Oxford team"),
    ("Hampshire Marine Forging", "marine + offshore forging", "small", "yacht industry", "d.murphy@hampsmarine.co.uk", "Declan Murphy"),
    ("Dorset Heavy Forge", "heavy forging", "medium", None, "h.elias@dorsetforge.co.uk", "Hossam Elias"),
    ("Devon Engineering Forge", "small forging", "small", None, None, None),
    ("Cornwall Foundry Penzance", "small foundry", "small", None, "j.allen@cornwallfoundry.co.uk", "Jennifer Allen"),
    ("Bauer-Bodoni Forge", "automotive forging", "small", None, "h.thompson@bauer-bodoni.co.uk", "Hannah Thompson"),
    ("Vincent Forge Pittsburgh", "small-batch forging (US)", "small", None, "j.miller@vincentforge.com", "Jessica Miller"),
    ("Buffalo Forge & Steel", "open-die forging (US)", "medium", None, "p.thomas@buffaloforge.com", "Patricia Thomas"),
    ("Niagara Forge & Steel", "heavy industrial forging", "medium", None, None, "Niagara Forge production"),
    ("Cleveland Steel Forge", "automotive forging", "medium", None, "k.smith@clevelandforge.com", "Karen Smith"),
    ("Pittsburgh Forging", "structural forging", "medium", None, "j.brown@pittsburghforging.com", "John Brown"),
    ("Eaton Forging Cleveland", "industrial forging", "medium", None, "p.brown@eatonforging.com", "Patricia Brown"),
    ("Buckhorn Forging Ohio", "small-batch forging", "small", None, None, None),
    ("Buckeye Forge Akron", "automotive forging", "small", None, "m.davis@buckeyeforge.com", "Michael Davis"),
    ("Steel City Forge Pittsburgh", "structural forging", "medium", None, "r.miller@steelcityforge.com", "Robert Miller"),
]

FIC_PAD_REGIONS = [
    "Stoke", "Derby", "Nottingham", "Leeds", "Bradford", "Halifax",
    "Doncaster", "Rotherham", "Barnsley", "Wakefield", "Mansfield", "Chesterfield",
]
FIC_PAD_TEMPLATES = [
    ("{region} Forge", "small forging", "small"),
    ("{region} Steel Industries", "structural steel", "small"),
    ("{region} Heavy Forging", "heavy forging", "medium"),
    ("{region} Iron Foundry", "iron casting", "small"),
]


# ─────────────────────────────────────────────────────────────────────────────
# CSV registry
# ─────────────────────────────────────────────────────────────────────────────

CSV_REGISTRY = {
    "uk_metals_expo": {
        "filename": "UK_Metals_Expo_2025_leads.csv",
        "id_prefix": "W",
        "seed": 20260518,
        "target": 124,
        "tracer": UK_TRACER,
        "cohort": UK_COHORT,
        "pad_regions": UK_PAD_REGIONS,
        "pad_templates": UK_PAD_TEMPLATES,
        "name_pools": [(UK_FIRST, UK_LAST, 1.0)],
        "email_suffixes": [".co.uk", ".com", ".co.uk", ".com"],
    },
    "hannover_messe": {
        "filename": "Hannover_Messe_2025_leads.csv",
        "id_prefix": "H",
        "seed": 20260520,
        "target": 120,
        "tracer": HM_TRACER,
        "cohort": HM_COHORT,
        "pad_regions": HM_PAD_REGIONS,
        "pad_templates": HM_PAD_TEMPLATES,
        "name_pools": [(DE_FIRST, DE_LAST, 0.85), (UK_FIRST, UK_LAST, 0.15)],
        "email_suffixes": [".de", ".de", ".de", ".com"],
    },
    "imts_chicago": {
        "filename": "IMTS_Chicago_2025_leads.csv",
        "id_prefix": "I",
        "seed": 20260521,
        "target": 95,
        "tracer": IMTS_TRACER,
        "cohort": IMTS_COHORT,
        "pad_regions": IMTS_PAD_REGIONS,
        "pad_templates": IMTS_PAD_TEMPLATES,
        "name_pools": [(US_FIRST, US_LAST, 1.0)],
        "email_suffixes": [".com", ".com", ".com", ".net"],
    },
    "industrial_ai_summit": {
        "filename": "Industrial_AI_Summit_2025_leads.csv",
        "id_prefix": "A",
        "seed": 20260522,
        "target": 65,
        "tracer": AIS_TRACER,
        "cohort": AIS_COHORT,
        "pad_regions": AIS_PAD_REGIONS,
        "pad_templates": AIS_PAD_TEMPLATES,
        "name_pools": [(US_FIRST, US_LAST, 0.45), (DE_FIRST, DE_LAST, 0.25), (UK_FIRST, UK_LAST, 0.2), (IT_FIRST, IT_LAST, 0.1)],
        "email_suffixes": [".com", ".com", ".ai", ".io"],
    },
    "forging_industry_convention": {
        "filename": "Forging_Industry_Convention_2025_leads.csv",
        "id_prefix": "F",
        "seed": 20260523,
        "target": 90,
        "tracer": FIC_TRACER,
        "cohort": FIC_COHORT,
        "pad_regions": FIC_PAD_REGIONS,
        "pad_templates": FIC_PAD_TEMPLATES,
        "name_pools": [(UK_FIRST, UK_LAST, 0.7), (US_FIRST, US_LAST, 0.3)],
        "email_suffixes": [".co.uk", ".com", ".co.uk", ".com"],
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Generator
# ─────────────────────────────────────────────────────────────────────────────

def generate_csv(csv_id: str) -> None:
    if csv_id not in CSV_REGISTRY:
        print(f"unknown csv_id: {csv_id}; expected one of {list(CSV_REGISTRY)}", file=sys.stderr)
        sys.exit(2)

    cfg = CSV_REGISTRY[csv_id]
    random.seed(cfg["seed"])

    rows = []

    # Row 1 — tracer (fixed). Tracers may be 6-tuple (legacy, no website_url)
    # or 7-tuple (post-Phase-1.7-Stage-C-prelim, with verified website URL).
    tracer = cfg["tracer"]
    tracer_website = tracer[6] if len(tracer) >= 7 else ""
    rows.append({
        "external_lead_id": f"{cfg['id_prefix']}001",
        "company_name": tracer[0],
        "contact_name": tracer[5] or "",
        "contact_email": tracer[4] or "",
        "sector_hint": tracer[1] or "",
        "factory_size_band": tracer[2],
        "raw_notes": tracer[3] or "",
        "website_url": tracer_website or "",
    })

    lead_id = 2
    target = cfg["target"]

    # Curated cohort. Entries may be 6-tuple or 7-tuple (last element =
    # verified website URL). Ranks 2-12 of each CSV carry verified URLs
    # from Nia web search (Phase 1.7 Stage C-prelim); remaining entries
    # are legacy 6-tuples that fall through to WebScraperAdapter's
    # derive-from-email cascade.
    for entry in cfg["cohort"]:
        if lead_id > target:
            break
        if len(entry) == 7:
            company, sector, size, raw_note, email, contact, website = entry
        else:
            company, sector, size, raw_note, email, contact = entry
            website = ""
        rows.append({
            "external_lead_id": f"{cfg['id_prefix']}{lead_id:03d}",
            "company_name": company,
            "contact_name": contact or "",
            "contact_email": email or "",
            "sector_hint": sector or "",
            "factory_size_band": size,
            "raw_notes": raw_note or "",
            "website_url": website or "",
        })
        lead_id += 1

    # Regional pad
    pad_i = 0
    pad_templates = cfg["pad_templates"]
    pad_regions = cfg["pad_regions"]
    while lead_id <= target:
        template, sector, size = pad_templates[pad_i % len(pad_templates)]
        region = pad_regions[pad_i % len(pad_regions)]
        company = template.format(region=region)
        contact_present = random.random() < 0.75
        contact = random_name(cfg["name_pools"]) if contact_present else ""
        email = ""
        if contact and random.random() < 0.88:
            first, last = contact.split(" ", 1)
            email = email_from_name(first, last, company, cfg["email_suffixes"])
        # ~5% deliberate email malformation
        if email and random.random() < 0.05:
            email = email.split("@")[0] + "@"
        raw_note = ""
        if random.random() < 0.32:
            raw_note = random.choice(RAW_NOTE_TEMPLATES_GENERIC)
        # ~10% sector ambiguity
        if random.random() < 0.10:
            sector = "unknown"
        rows.append({
            "external_lead_id": f"{cfg['id_prefix']}{lead_id:03d}",
            "company_name": company,
            "contact_name": contact,
            "contact_email": email,
            "sector_hint": sector,
            "factory_size_band": size,
            "raw_notes": raw_note,
            "website_url": "",  # Regional pad = synthetic, no verified URL
        })
        lead_id += 1
        pad_i += 1

    out_dir = Path(__file__).resolve().parent.parent / "apps" / "theater_ui" / "public" / "seed_csvs"
    out_path = out_dir / cfg["filename"]

    fieldnames = [
        "external_lead_id", "company_name", "contact_name", "contact_email",
        "sector_hint", "factory_size_band", "raw_notes", "website_url",
    ]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    # Sync legacy path for the UK Metals Expo only — other CSVs only live in
    # seed_csvs/ subdirectory
    if csv_id == "uk_metals_expo":
        legacy = out_dir.parent / cfg["filename"]
        with open(legacy, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

    # Sanity checks
    synthetic_count = sum(1 for r in rows if "Synthetic" in r["company_name"] or "synthetic" in r["company_name"].lower())
    generated_count = sum(1 for r in rows if "(generated)" in r["contact_name"] or "(generated)" in r["contact_email"])
    bad_band_count = sum(1 for r in rows if r["factory_size_band"] not in ("small", "medium", "large", "unknown"))
    assert synthetic_count == 0, f"{cfg['filename']}: {synthetic_count} synthetic rows"
    assert generated_count == 0, f"{cfg['filename']}: {generated_count} (generated) markers"
    assert bad_band_count == 0, f"{cfg['filename']}: {bad_band_count} invalid size bands"
    assert rows[0]["external_lead_id"] == f"{cfg['id_prefix']}001"
    assert rows[0]["company_name"] == tracer[0]
    assert rows[0]["factory_size_band"] in ("medium", "large"), \
        f"{cfg['filename']}: tracer size band must be medium/large for rank-1 deterministic"

    print(f"{cfg['filename']}: wrote {len(rows)} rows · tracer = {rows[0]['company_name']}")


def main():
    if len(sys.argv) < 2:
        print("usage: regenerate_seed_csv.py <csv_id|all>", file=sys.stderr)
        print(f"  csv_id options: {list(CSV_REGISTRY)}", file=sys.stderr)
        sys.exit(1)

    arg = sys.argv[1]
    if arg == "all":
        for csv_id in CSV_REGISTRY:
            generate_csv(csv_id)
    else:
        generate_csv(arg)


if __name__ == "__main__":
    main()
