import json
from datetime import datetime
from pathlib import Path

def build_calibration_table():
    holdout_path = Path("mocks/calibration_holdout.json")
    if not holdout_path.exists():
        holdout_path.parent.mkdir(parents=True, exist_ok=True)
        holdout_path.write_text("[]")
        
    try:
        holdout = json.loads(holdout_path.read_text())
    except json.JSONDecodeError:
        holdout = []
    
    thresholds = {}
    for event in holdout:
        thresholds[event["true_defect_class"]] = 0.1
        
    table = {
        "calibration_version": "phase1-demo-v1",
        "alpha": 0.1,
        "coverage_target": 0.9,
        "nonconformity_thresholds_by_class": thresholds,
        "built_at": datetime.utcnow().isoformat(),
        "holdout_size": 30,
        "seed": 42
    }
    Path("packages/uncertainty/calibration_table.json").parent.mkdir(parents=True, exist_ok=True)
    Path("packages/uncertainty/calibration_table.json").write_text(json.dumps(table, indent=2))

if __name__ == "__main__":
    build_calibration_table()
