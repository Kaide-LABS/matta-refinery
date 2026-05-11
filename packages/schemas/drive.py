from datetime import datetime
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

class DossierDocManifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    drive_folder_id: str
    drive_doc_id: str
    share_link: str
    last_verified_at: datetime
    knowledge_graph_version: str
