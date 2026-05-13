#!/bin/bash
set -e

echo "Seeding mock data..."
python scripts/seed_mock_data.py

echo "Building calibration table..."
python scripts/build_calibration_table.py

echo "Verifying knowledge graph..."
python scripts/verify_knowledge_graph.py

echo "Demo ready to run."
