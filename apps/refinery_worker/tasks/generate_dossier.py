from ..app import app
from sqlalchemy import create_engine, text
from apps.refinery_api.config import settings
import hashlib
from datetime import datetime
from pathlib import Path

from packages.knowledge_graph.loader import load_graph
from packages.uncertainty.conformal import CalibrationTable


@app.task(
    name="refinery.generate_dossier",
    bind=True,
    acks_late=True,
    reject_on_worker_lost=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    max_retries=3,
)
def generate_dossier(self, prospect_id: str, dossier_id: str):
    engine = create_engine(settings.postgres_url.replace('+asyncpg', ''))

    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT batch_id, signal_hash FROM lead_prospects WHERE id = :pid"),
            {"pid": prospect_id},
        ).first()
    if row is None:
        raise ValueError(f"prospect_id {prospect_id} not found in lead_prospects")
    batch_id, lp_signal_hash = row[0], row[1]

    kg_version = load_graph().version

    calib_path = Path("packages/uncertainty/calibration_table.json")
    calib = CalibrationTable.model_validate_json(calib_path.read_text(encoding="utf-8"))
    calibration_version = calib.calibration_version

    if lp_signal_hash:
        signal_hash = lp_signal_hash
    else:
        signal_hash_raw = f"{prospect_id}|{batch_id}|{kg_version}"
        signal_hash = hashlib.sha256(signal_hash_raw.encode("utf-8")).hexdigest()[:16]

    with engine.begin() as conn:
        conn.execute(
            text(
                """
                INSERT INTO dossier_artifacts (
                    id, dossier_id, prospect_id, batch_id,
                    signal_hash, knowledge_graph_version, calibration_version,
                    state, generated_at
                ) VALUES (
                    :did, :did, :pid, :bid,
                    :sh, :kgv, :cv,
                    'generating', :now
                )
                ON CONFLICT (id) DO UPDATE
                  SET state = 'generating', generated_at = :now
                """
            ),
            {
                "did": dossier_id,
                "pid": prospect_id,
                "bid": batch_id,
                "sh": signal_hash,
                "kgv": kg_version,
                "cv": calibration_version,
                "now": datetime.utcnow(),
            },
        )

    app.send_task("refinery.dossier_section_taxonomy", args=[prospect_id, dossier_id])
