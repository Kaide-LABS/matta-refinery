import sys
from pathlib import Path
import os
import json

def seed_mock_data():
    # Make sure packages directory exists
    Path("apps/mocks").mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from apps.mocks.lead_csv_generator import generate_leads_csv
    generate_leads_csv(Path("mocks/UK_Metals_Expo_2025_leads.csv"))

    holdout = []
    for i in range(30):
        holdout.append({
            "event_id": f"calib_{i:03d}",
            "vertical": "metal_casting",
            "process_taxonomy_summary": "ductile iron pour into molds; ladle pour at ~1450C",
            "true_defect_class": "porosity" if i < 4 else "dimensional_drift",
            "raw_context": "Operator notes increased porosity defects on Pour A line after ladle refurb."
        })
    Path("mocks/calibration_holdout.json").parent.mkdir(parents=True, exist_ok=True)
    Path("mocks/calibration_holdout.json").write_text(json.dumps(holdout, indent=2))
    Path("mocks/mock_slack/seed_workspace.json").parent.mkdir(parents=True, exist_ok=True)
    Path("mocks/mock_slack/seed_workspace.json").write_text(json.dumps({"team_id": "T_MOCK"}))
    Path("mocks/mock_crm/seed_contacts.json").parent.mkdir(parents=True, exist_ok=True)
    Path("mocks/mock_crm/seed_contacts.json").write_text(json.dumps([{"id": "W001", "name": "William Cook Sheffield"}]))
    Path("mocks/mock_drive/seed_folders.json").parent.mkdir(parents=True, exist_ok=True)
    Path("mocks/mock_drive/seed_folders.json").write_text(json.dumps([{"id": "folder_1", "name": "Matta Leads"}]))

if __name__ == "__main__":
    seed_mock_data()
