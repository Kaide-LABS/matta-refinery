import csv
from pathlib import Path

def generate_leads_csv(output_path: Path):
    data = [
        ["external_lead_id", "company_name", "contact_name", "contact_email", "sector_hint", "factory_size_band", "raw_notes"],
        ["W001", "William Cook Sheffield", "(generated)", "(generated)@wcook-sheffield.example", "ductile iron casting", "medium", "booth-conversation:porosity-spike-on-pour-A"],
        ["T002", "Tata Steel UK", "(generated)", "(generated)@tatasteel.example", "steel", "large", ""],
        ["E003", "Ernest Wright", "(generated)", "(generated)@ernestwright.example", "blade-grinding", "small", ""],
        ["C004", "Centriblast", "(generated)", "(generated)@centriblast.example", "abrasive blasting", "medium", ""],
        ["S005", "Safran Seats GB", "(generated)", "(generated)@safran.example", "aerospace seat assembly", "large", ""]
    ]
    # Add synthetic rows
    for i in range(6, 125):
        data.append([f"S{i:03d}", f"Synthetic Company {i}", "(generated)", f"contact{i}@example.com", "unknown", "medium", ""])
        
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(data)

if __name__ == "__main__":
    generate_leads_csv(Path("mocks/UK_Metals_Expo_2025_leads.csv"))
