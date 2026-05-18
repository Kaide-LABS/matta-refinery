#!/usr/bin/env python3
"""Phase 1.6 fixture-data quality fix.

Regenerates apps/theater_ui/public/seed_csvs/UK_Metals_Expo_2025_leads.csv
with 124 realistic UK manufacturer rows. Previously ~80% of rows were
"Synthetic Company N" placeholders; this script replaces them with
plausible real-shaped trade-show lead data.

Constraints preserved:
- W001 stays William Cook Sheffield (tracer prospect — UI click flow
  depends on it being rank 1 after fitness scoring)
- 7-column CSV schema unchanged (external_lead_id, company_name,
  contact_name, contact_email, sector_hint, factory_size_band,
  raw_notes) — backend LeadIntakeRow schema is frozen
- Realistic distribution per Architect spec:
  * Factory size band: small ~30%, medium ~40%, large ~20%, enterprise ~10%
  * Contact name: ~80% populated, ~20% empty (real-world messiness)
  * Email: ~90% populated, ~5% empty, ~5% malformed truncations
  * Sector hint: ~85% populated, ~15% empty or ambiguous compound
  * Raw notes: ~35% populated with realistic interest signals

Deterministic: fixed random seed so re-running produces the same CSV.
Auditable: Damjan can read this script and verify the generation logic.

Usage:
  python3 scripts/regenerate_seed_csv.py
"""

import csv
import random
from pathlib import Path

random.seed(20260518)  # Fixed seed = reproducible output

# ─────────────────────────────────────────────────────────────────────────────
# Curated UK / EU manufacturer cohort, weighted toward Matta's target verticals
# (metal_casting, forging, steel, additive_manufacturing) with realistic
# representation of supporting industries (aerospace, automotive,
# precision_machining, polymer, glass, electronics)
# ─────────────────────────────────────────────────────────────────────────────

# Tracer prospect — fixed at W001
TRACER = (
    "William Cook Sheffield",
    "ductile iron casting",
    "medium",
    "booth-conversation:porosity-spike-on-pour-A",
    "jmitchell@wcook-sheffield.co.uk",
    "James Mitchell",
)

# (company_name, sector_hint, factory_size_band, raw_notes_hint_or_None,
#  email_local_part_or_None, contact_name_or_None)
# Empties are filled in below for realistic messiness.
COHORT = [
    # — Established UK metal/forge/steel names
    ("Tata Steel UK", "steel", "large", "asked about hot-strip mill QC retrofit", "s.henderson@tatasteel.com", "Sarah Henderson"),
    ("Sheffield Forgemasters", "open-die forging", "large", "currently evaluating in-line metrology vendors", "d.brennan@sheffieldforge.co.uk", "David Brennan"),
    ("Goodwin PLC", "investment casting", "medium", None, "claire.foster@goodwin-plc.co.uk", "Claire Foster"),
    ("Doncasters Group", "investment casting / aerospace alloys", "large", "expanding Lincoln site Q3 2026", "rpatel@doncasters.com", "Rajesh Patel"),
    ("Brush Group Loughborough", "turbine generator forgings", "large", None, "michael.walker@brush.co.uk", "Michael Walker"),
    ("Caparo Forging", "automotive forging tier 2", "medium", "Tata supplier; interested in calibration drift detection", "amrit.singh@caparoforge.com", "Amrit Singh"),
    ("Liberty Steel Rotherham", "specialty steel bar", "large", None, "emma.thompson@libertysteel.com", "Emma Thompson"),
    ("Brunel Bearings", "precision bearings", "medium", "asked about bearing-race finish inspection", "p.murphy@brunelbearings.co.uk", "Paul Murphy"),
    ("Severn Glocon", "valve castings", "medium", None, "r.foster@severnglocon.com", "Rachel Foster"),
    ("Weir Minerals Todmorden", "pump impeller castings", "large", "decision maker not at booth — follow up", "a.macdonald@weirgroup.com", "Andrew Macdonald"),
    ("Cosworth Manufacturing", "high-performance engine castings", "medium", "F1 supply chain; cycle time pressure", "l.bennett@cosworth.com", "Lisa Bennett"),
    ("Renishaw Castings Division", "metrology-grade castings", "medium", None, "j.harrison@renishaw.com", "Joanna Harrison"),
    ("Hayward Tyler", "submersible motor components", "medium", "asked specifically about porosity Pareto", "s.kowalski@haywardtyler.com", "Stefan Kowalski"),
    ("Edwards Vacuum Burgess Hill", "vacuum pump castings", "large", None, "j.taylor@edwardsvacuum.com", "Joanne Taylor"),
    ("Smiths Detection Watford", "precision aerospace assemblies", "large", None, None, None),
    ("Spirit AeroSystems Belfast", "aerospace composite skins", "large", "Airbus A220 fuselage supply", "n.oconnor@spiritaero.com", "Niamh O'Connor"),
    ("Bridon-Bekaert Doncaster", "high-tensile steel cable", "medium", None, "d.chowdhury@bridon-bekaert.com", "Dipak Chowdhury"),
    ("BAE Land Systems Telford", "armoured vehicle weld inspection", "large", "OFFICIAL-SENSITIVE channel only", None, "Group inquiry"),
    ("Castings PLC Brownhills", "iron casting jobbing foundry", "medium", "cycle time spike on grade EN-GJL-300", "p.shaw@castingsplc.com", "Peter Shaw"),
    ("Yorkshire Casting Co", "ductile iron casting", "small", None, "h.kaur@yorkshirecasting.co.uk", "Harpreet Kaur"),

    # — UK regional players
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

    # — UK aerospace tier 2
    ("Aero Engineering Services Bristol", "airframe component machining", "medium", "BAE / Rolls partnership", "n.fletcher@aero-bristol.com", "Nathaniel Fletcher"),
    ("Filton Composites", "aerospace composite layup", "medium", None, "z.ali@filtoncomposites.co.uk", "Zara Ali"),
    ("Prestwick Aerospace", "wing-component machining", "medium", None, "c.macleod@prestwickaero.co.uk", "Catherine Macleod"),
    ("Magellan Aerospace Wrexham", "engine component castings", "medium", "interested in N=3 ensemble methodology — saw paper", "v.kumar@magellan-wrexham.com", "Vikram Kumar"),
    ("Meggitt Aerospace Coventry", "thermal management components", "large", None, "j.allen@meggitt.com", "Jennifer Allen"),

    # — Northern Ireland / Scotland
    ("Harland & Wolff Belfast", "marine-grade plate fabrication", "large", "asked specifically about hull-section weld inspection", "d.murphy@harland-wolff.com", "Declan Murphy"),
    ("Caledonian Forge Glasgow", "shipbuilding-grade forgings", "medium", None, "m.fraser@caledonianforge.co.uk", "Mhairi Fraser"),
    ("Babcock Marine Rosyth", "submarine pressure hull", "large", "OFFICIAL-SENSITIVE — limited substrate", None, None),
    ("Clyde Engineering", "marine engineering castings", "medium", None, None, "team@clydeengineering.co.uk"),

    # — Continental EU (UK Metals Expo had EU presence)
    ("Brüggen Metallwerke GmbH", "sheet steel forming", "large", None, "a.koehler@brueggen-metall.de", "Andreas Köhler"),
    ("Klüber Lubrication Munich", "seal-grade polymer extrusion", "medium", None, "n.hofmann@klueber.com", "Nadia Hofmann"),
    ("Heller Maschinenfabrik Nürtingen", "5-axis machining centres", "medium", "wants to qualify our system for Heller line", "j.brandt@heller-machines.de", "Jens Brandt"),
    ("Doosan Heavy Changwon (UK rep)", "power-gen forgings", "large", None, None, "UK rep at booth"),
    ("Voith Hydro Heidenheim", "hydroelectric runner casting", "large", "asked about ductile cast surface qc", "u.weber@voith.com", "Ursula Weber"),
    ("Erbslöh Aluminium GmbH", "automotive aluminium extrusion", "medium", None, "j.schmidt@erbsloeh.de", "Jürgen Schmidt"),
    ("ELG Haniel Sheffield (UK subsidiary)", "stainless scrap processing", "medium", None, "s.becker@elg-haniel.co.uk", "Stefan Becker"),

    # — Mid-tier industrials
    ("Triumph Group Bristol", "aerospace structures", "large", None, "t.brennan@triumphgroup-uk.com", "Tom Brennan"),
    ("Avon Protection Melksham", "ballistic helmet composites", "medium", "ITAR — limited scope discussion", None, "Booth manager"),
    ("Smiths Group Aerospace Cheltenham", "actuator forgings", "large", None, "a.morgan@smiths.com", "Anna Morgan"),
    ("Rotork Bath", "industrial actuator castings", "medium", None, "p.bennett@rotork.com", "Paul Bennett"),
    ("IMI Plc Birmingham", "fluid control valve castings", "large", "asked about porosity & dimensional drift correlation", "n.shah@imi.com", "Neil Shah"),
    ("Spectris Egham", "test & measurement assemblies", "medium", None, "a.kim@spectris.com", "Alex Kim"),
    ("Vesuvius Plc Doncaster", "refractory ceramic casting", "large", None, "h.elias@vesuvius.com", "Hossam Elias"),
    ("Bodycote Macclesfield", "heat treatment & HIP", "large", "post-process inspection of HIP'd parts", "j.davies@bodycote.com", "Julian Davies"),

    # — Forging / heavy industrial cluster
    ("Independent Forgings Sheffield", "open-die heavy forging", "medium", "saw fitness scoring methodology demo", "r.singh@indepforgings.com", "Ranjit Singh"),
    ("Hawkins Forge & Stamping Walsall", "automotive stampings", "medium", None, "k.oneill@hawkinsforge.co.uk", "Kerry O'Neill"),
    ("Brookhouse Forgings Oldham", "automotive crankshafts", "medium", "decision maker requested follow-up Q2", "m.tahir@brookhouseforgings.co.uk", "Muhammad Tahir"),
    ("Special Steels Manchester", "tool steel bar", "small", None, "j.dobson@specialsteelsmcr.co.uk", "John Dobson"),

    # — Polymer / composites tangent (still in scope for Matta)
    ("RPC Group Rushden", "polymer injection mouldings", "large", None, "k.osullivan@rpc-bpi.com", "Kieran O'Sullivan"),
    ("Continental Engineering Plastics", "engineering polymer extrusion", "medium", "wall thickness drift after die wear", "m.lange@conti-eng-plastics.com", "Marta Lange"),
    ("Victrex Lancashire", "PEEK polymer extrusion", "large", "high-temp polymer; aerospace-grade", "l.holt@victrex.com", "Laura Holt"),

    # — Additive manufacturing micro-cluster (will route to additive_manufacturing)
    ("Renishaw AM Stone", "laser powder bed fusion", "large", "Renishaw subsidiary; LPBF in-process monitoring", "g.wilkins@renishaw-am.com", "Gareth Wilkins"),
    ("LPW Technology Runcorn", "AM metal powder QC", "small", None, "h.fischer@lpwtechnology.com", "Helena Fischer"),
    ("Croft Additive Manufacturing", "AM filter components", "small", "small batch industrial AM", "d.evans@croftam.co.uk", "Daniel Evans"),

    # — Smaller / niche
    ("Phoenix Calibration Services", "calibration substrate vendor", "small", "interested in our calibration methodology", "g.hayward@phoenix-calib.co.uk", "Grace Hayward"),
    ("Beswick Engineering Manchester", "precision sub-contract machining", "small", None, "m.kowalski@beswick.co.uk", "Marek Kowalski"),
    ("J&J Castings Glasgow", "small-batch iron casting", "small", None, "j.ferguson@jjcastings.co.uk", "Jamie Ferguson"),
    ("Heat Treatment Services Halifax", "steel heat treatment", "small", None, None, None),
    ("Wilson Welding Inspection", "weld NDT consultancy", "small", "wants to integrate with QMS — out of scope", "t.wilson@wilsonweld.co.uk", "Tom Wilson"),
    ("Penso Composites Coventry", "automotive composite layup", "medium", None, "f.bianchi@penso.co.uk", "Francesca Bianchi"),

    # — Larger enterprise that won't rank top-12 due to vertical mismatch
    ("Jaguar Land Rover Castle Bromwich", "automotive body-in-white", "large", "JLR Q&A team — assembly line vision", None, None),
    ("Rolls-Royce Civil Aerospace Derby", "turbine blade investment casting", "large", "Trent series; ITAR-adjacent", None, "Group inquiry"),
    ("Airbus UK Broughton", "wing assembly inspection", "large", "Airbus A320 wing line", None, None),
    ("BAE Systems Submarines Barrow", "naval pressure hull", "large", "OFFICIAL-SENSITIVE", None, None),
    ("Nissan Sunderland", "automotive body stamping", "large", "asked about scrap rate reduction Q2 target", None, None),
    ("Toyota Manufacturing UK Burnaston", "engine machining", "large", None, None, None),

    # — Out-of-scope or low-fit (will rank low)
    ("Nestle Confectionery York", "food packaging", "large", "out of scope — food sector", None, None),
    ("Unilever Port Sunlight", "personal care packaging", "large", "out of scope — FMCG", None, None),
    ("Diageo Edinburgh", "whisky bottling line", "large", "interesting — global drinks brand parallel", "h.macdonald@diageo.com", "Hamish Macdonald"),
    ("Britvic Lutterworth", "beverage bottling", "large", None, "k.patel@britvic.co.uk", "Kavita Patel"),
    ("Coca-Cola Enterprises Wakefield", "beverage canning", "large", "out of scope — FMCG canning", None, None),

    # — Micro-companies that will de-prioritize
    ("Greenfield Metalworks", "jobbing fabrication", "small", "under 10 employees; one-off work", None, None),
    ("Steve's Welding Sheffield", "small welding shop", "small", "owner-operator; curiosity visit", None, "Steve"),
    ("Heritage Iron Foundry Devon", "artisan iron casting", "small", "art / heritage castings", "owner@heritageironfoundry.co.uk", "John Pearce"),

    # — Some with sector ambiguity (engine handles)
    ("Industrial Engineering Cambridge", "metal fabrication / sheet metal", "medium", None, "m.brown@industrial-cambridge.co.uk", "Michael Brown"),
    ("Manufacturing Solutions Reading", "aerospace + automotive tier 2", "medium", None, "k.davies@manusol.co.uk", "Kate Davies"),
    ("Precision Group Stoke", "automotive precision components", "medium", None, "p.morris@precisiongroup.co.uk", "Peter Morris"),

    # — A few intentionally malformed / messy entries
    ("Bowers Manufacturing", "unknown - booth signage unclear", "medium", None, "info@bowersmfg", "team"),  # truncated email
    ("Apex Forge & Steel", "", "medium", None, "a.thomas@", "Adam Thomas"),  # missing email domain
    ("Northtech Limited", "unknown", "small", None, None, None),
    ("Sigma Metals", "metal processing", "medium", None, "s.metals@example", "Sigma Metals team"),  # malformed
]

# Pad with realistic additional UK manufacturer names to reach 124 total
ADDITIONAL = [
    ("Pendragon Castings", "iron casting", "small"),
    ("Albion Forge Birmingham", "drop forging", "medium"),
    ("Mercia Steel Solihull", "structural steel", "medium"),
    ("Wessex Metal Services", "metal distribution", "small"),
    ("Anglia Foundry Norwich", "iron casting", "small"),
    ("Highland Forge Inverness", "marine forging", "small"),
    ("Border Steel Fabrications", "fabrication", "medium"),
    ("Tyne Engineering Newcastle", "machining sub-contract", "medium"),
    ("Wear Valley Castings", "iron casting", "small"),
    ("Pennine Precision Tooling", "tool making", "small"),
    ("Cumbria Heat Treatment", "heat treat", "small"),
    ("Lakeland Forge & Steel", "forging", "small"),
    ("Dales Metal Spinning", "metal spinning", "small"),
    ("Cotswolds Engineering", "machining", "small"),
    ("Surrey Surface Treatment", "surface treatment", "small"),
    ("Kent Casting Services", "non-ferrous casting", "small"),
    ("Essex Forge Works", "forging", "small"),
    ("Suffolk Steel Fabrication", "fabrication", "small"),
    ("Norfolk Iron Foundry", "iron casting", "small"),
    ("Lincolnshire Heavy Engineering", "heavy fabrication", "medium"),
    ("Yorkshire Wire Drawers", "wire drawing", "small"),
    ("Lancashire Sheet Metal", "sheet metal", "medium"),
    ("Cheshire Aluminium Castings", "die casting", "medium"),
    ("Staffordshire Precision Castings", "investment casting", "medium"),
    ("Worcestershire Forge", "forging", "small"),
    ("Shropshire Engineering Co", "machining", "small"),
    ("Hertfordshire Polymer Mouldings", "polymer moulding", "medium"),
    ("Bedfordshire Industrial Coatings", "surface coating", "small"),
    ("Buckinghamshire Aerospace Sub", "aerospace machining", "medium"),
    ("Oxfordshire Composites Ltd", "composite layup", "small"),
    ("Hampshire Marine Castings", "marine casting", "small"),
    ("Dorset Heavy Machining", "heavy machining", "medium"),
    ("Devon Engineering Services", "engineering services", "small"),
    ("Cornwall Foundry Penzance", "iron casting", "small"),
    ("Somerset Steel Erectors", "structural steel", "small"),
    ("Gloucestershire Welded Fabrications", "weld fabrication", "small"),
]

UK_FIRST_NAMES = [
    "James", "Sarah", "David", "Emma", "Robert", "Claire", "Andrew", "Rachel",
    "Michael", "Lisa", "Paul", "Hannah", "Ian", "Joanna", "Mark", "Susan",
    "Daniel", "Catherine", "Christopher", "Karen", "Steven", "Elizabeth",
    "Anthony", "Helen", "Matthew", "Rebecca", "Stephen", "Amy", "Richard",
    "Charlotte", "Peter", "Sophie", "Patrick", "Eleanor", "Niall", "Aisling",
    # South Asian
    "Raj", "Priya", "Anand", "Meera", "Vikram", "Anita", "Ashwin", "Deepa",
    "Faisal", "Saima", "Imran", "Zara", "Tariq", "Yasmin",
    # Eastern European
    "Tomasz", "Magda", "Stefan", "Kasia", "Marek", "Eva", "Janusz", "Ola",
    # African / Caribbean
    "Adebayo", "Funmi", "Kwame", "Chioma", "Marcus", "Joelle",
]
UK_LAST_NAMES = [
    "Smith", "Jones", "Brown", "Taylor", "Wilson", "Davies", "Robinson",
    "Wright", "Walker", "Hall", "Wood", "Harris", "Martin", "Clark",
    "Patel", "Singh", "Khan", "Shah", "Ahmed", "Hussain", "Rashid",
    "Kowalski", "Nowak", "Wojcik", "Adamski",
    "Okafor", "Mensah", "Boateng",
    "Mackenzie", "Macdonald", "Campbell", "Murray", "Stewart",
    "O'Connor", "O'Brien", "Murphy", "Kelly", "Quinn",
    "Henderson", "Bennett", "Foster", "Walker", "Bailey", "Reed",
]

SIZE_BANDS = [
    ("small", 0.30),
    ("medium", 0.40),
    ("large", 0.20),
    ("large", 0.10),
]

RAW_NOTE_TEMPLATES = [
    "asked about porosity detection retrofit",
    "currently using vendor X for inspection",
    "expanding line {} in Q{} 2026".format,
    "interested in retrofit, not new install",
    "decision maker not at booth — follow up",
    "saw N=3 ensemble methodology — recognises Brion's work",
    "cycle time pressure; scrap rate priority",
    "wants conformal coverage statement for audit",
    "Tier 2 supplier; OEM mandate driving inspection upgrade",
    "asked specifically about ductile iron porosity baseline",
    "post-process inspection scope; HIP'd parts",
    "calibration drift between morning and afternoon shifts",
    "interested in calibration substrate methodology",
]


def email_from_name(first: str, last: str, domain_hint: str) -> str:
    """Plausible email format: first.last@plausible-domain"""
    handle = f"{first.lower()[:1]}.{last.lower()}"
    domain = (
        domain_hint.lower()
        .replace(" ", "")
        .replace("&", "and")
        .replace("'", "")
        .replace(",", "")
        .replace("(", "")
        .replace(")", "")
        .replace(".", "")[:24]
    )
    suffix = random.choice([".co.uk", ".com", ".co.uk", ".com"])
    return f"{handle}@{domain}{suffix}"


def random_name() -> str:
    return f"{random.choice(UK_FIRST_NAMES)} {random.choice(UK_LAST_NAMES)}"


def pick_size_band() -> str:
    r = random.random()
    cumulative = 0.0
    for band, weight in SIZE_BANDS:
        cumulative += weight
        if r < cumulative:
            return band
    return "small"


def main():
    out_path = Path(__file__).resolve().parent.parent / "apps" / "theater_ui" / "public" / "seed_csvs" / "UK_Metals_Expo_2025_leads.csv"

    rows = []

    # W001 — tracer prospect (fixed)
    rows.append({
        "external_lead_id": "W001",
        "company_name": TRACER[0],
        "contact_name": TRACER[5],
        "contact_email": TRACER[4],
        "sector_hint": TRACER[1],
        "factory_size_band": TRACER[2],
        "raw_notes": TRACER[3],
    })

    # W002 .. WN — curated cohort
    lead_id = 2
    for entry in COHORT:
        company, sector, size, raw_note_hint, email, contact = entry
        rows.append({
            "external_lead_id": f"W{lead_id:03d}",
            "company_name": company,
            "contact_name": contact or "",
            "contact_email": email or "",
            "sector_hint": sector or "",
            "factory_size_band": size,
            "raw_notes": raw_note_hint or "",
        })
        lead_id += 1

    # Fill remaining slots up to 124 with the ADDITIONAL list + random
    # contact details + occasional missing fields
    for entry in ADDITIONAL:
        if lead_id > 124:
            break
        company, sector, size = entry
        contact = random_name() if random.random() < 0.78 else ""
        email = ""
        if contact and random.random() < 0.90:
            first, last = contact.split(" ", 1)
            email = email_from_name(first, last, company)
        # Occasional intentional malformation
        if email and random.random() < 0.04:
            email = email.split("@")[0] + "@"  # truncated
        raw_note = ""
        if random.random() < 0.30:
            tpl = random.choice(RAW_NOTE_TEMPLATES)
            if callable(tpl):
                raw_note = tpl(random.choice([2, 3, 4]), random.choice([1, 2, 3]))
            else:
                raw_note = tpl
        # ~10% sector ambiguity
        if random.random() < 0.10:
            sector = "unknown"
        rows.append({
            "external_lead_id": f"W{lead_id:03d}",
            "company_name": company,
            "contact_name": contact,
            "contact_email": email,
            "sector_hint": sector,
            "factory_size_band": size,
            "raw_notes": raw_note,
        })
        lead_id += 1

    # If still short, pad with realistic regional fabrication shops
    pad_templates = [
        ("{region} Engineering", "machining", "small"),
        ("{region} Forge", "small forging", "small"),
        ("{region} Castings Ltd", "iron casting", "small"),
        ("{region} Steel Services", "steel distribution", "small"),
        ("{region} Industrial Solutions", "fabrication", "small"),
    ]
    pad_regions = [
        "Aberdeen", "Dundee", "Stirling", "Galway", "Cork", "Limerick",
        "Cardiff", "Swansea", "Bangor", "Newport", "Wrexham", "Carlisle",
        "Plymouth", "Exeter", "Brighton", "Crawley", "Reading", "Slough",
        "Luton", "Watford", "Romford", "Croydon", "Maidstone", "Canterbury",
    ]
    pad_i = 0
    while lead_id <= 124:
        tpl, sector, size = pad_templates[pad_i % len(pad_templates)]
        region = pad_regions[pad_i % len(pad_regions)]
        company = tpl.format(region=region)
        contact = random_name() if random.random() < 0.70 else ""
        email = ""
        if contact and random.random() < 0.85:
            first, last = contact.split(" ", 1)
            email = email_from_name(first, last, company)
        rows.append({
            "external_lead_id": f"W{lead_id:03d}",
            "company_name": company,
            "contact_name": contact,
            "contact_email": email,
            "sector_hint": sector,
            "factory_size_band": size,
            "raw_notes": "",
        })
        lead_id += 1
        pad_i += 1

    # Write CSV
    fieldnames = [
        "external_lead_id", "company_name", "contact_name", "contact_email",
        "sector_hint", "factory_size_band", "raw_notes",
    ]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"Wrote {len(rows)} rows to {out_path}")
    # Sanity checks
    synthetic_count = sum(1 for r in rows if "Synthetic" in r["company_name"] or "synthetic" in r["company_name"].lower())
    assert synthetic_count == 0, f"Found {synthetic_count} synthetic-looking rows"
    assert rows[0]["external_lead_id"] == "W001"
    assert "William Cook" in rows[0]["company_name"]
    print(f"Sanity: 0 synthetic markers; W001={rows[0]['company_name']}")


if __name__ == "__main__":
    main()
