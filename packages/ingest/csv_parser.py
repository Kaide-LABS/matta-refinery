import csv
import io
import uuid
from datetime import datetime
from packages.schemas.lead_intake import LeadIntakeBatch, LeadIntakeRow

def parse_csv_to_batch(file_bytes: bytes, source_label: str, user) -> LeadIntakeBatch:
    content = file_bytes.decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))
    rows = []
    for row in reader:
        rows.append(LeadIntakeRow(
            external_lead_id=row.get("external_lead_id") or str(uuid.uuid4()),
            company_name=row.get("company_name") or "Unknown",
            contact_name=row.get("contact_name"),
            contact_email=row.get("contact_email"),
            sector_hint=row.get("sector_hint"),
            factory_size_band=row.get("factory_size_band") or "unknown",
            raw_notes=row.get("raw_notes"),
            website_url=row.get("website_url") or None,
        ))
    
    return LeadIntakeBatch(
        batch_id=str(uuid.uuid4()),
        source_label=source_label,
        source_surface="theater_csv",
        ingest_user=user.id,
        ingest_timestamp=datetime.utcnow(),
        rows=rows
    )
