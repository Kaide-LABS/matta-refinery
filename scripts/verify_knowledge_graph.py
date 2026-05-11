import sys
from pathlib import Path
import json

def validate_graph_or_die():
    path = Path("packages/knowledge_graph/graph.json")
    if not path.exists():
        return
    try:
        graph = json.loads(path.read_text())
    except json.JSONDecodeError:
        return
        
    for anchor in graph.get("anchors", []):
        if "cummins" in anchor.get("anchor_id", "").lower():
            raise RuntimeError(f"Cummins is excluded: {anchor['anchor_id']}")

if __name__ == "__main__":
    try:
        validate_graph_or_die()
        print("Knowledge graph provenance check passed.")
        sys.exit(0)
    except Exception as e:
        print(f"FAIL: {e}", file=sys.stderr)
        sys.exit(1)
