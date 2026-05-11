import os
from pathlib import Path

dirs = [
    "infra",
    "apps/refinery_api/routers",
    "apps/refinery_worker/tasks",
    "apps/theater_ui/pages",
    "apps/theater_ui/components",
    "apps/theater_ui/hooks",
    "apps/mocks/mock_slack",
    "apps/mocks/mock_crm",
    "apps/mocks/mock_drive",
    "apps/mocks/mock_matta_dashboard",
    "packages/schemas",
    "packages/adc",
    "packages/scoring",
    "packages/enrichment",
    "packages/knowledge_graph",
    "packages/uncertainty",
    "packages/outbox",
    "packages/adapters/slack",
    "packages/adapters/crm",
    "packages/adapters/drive",
    "packages/prompts",
    "scripts",
    "migrations/versions",
    "tests/unit",
    "tests/integration"
]

for d in dirs:
    Path(d).mkdir(parents=True, exist_ok=True)
    
print("Directories created successfully.")
