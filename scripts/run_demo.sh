#!/bin/bash
set -e

echo "Seeding mock data..."
docker compose exec -T refinery_api python scripts/seed_mock_data.py

echo "Building calibration table..."
docker compose exec -T refinery_api python scripts/build_calibration_table.py

echo "Verifying knowledge graph..."
docker compose exec -T refinery_api python scripts/verify_knowledge_graph.py

echo "Demo ready to run."
