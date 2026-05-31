from datetime import datetime

from pydantic import BaseModel

from ..models.enums import Crop


class ModelVersionRead(BaseModel):
    id: int
    crop: Crop
    version: str
    dataset_version: str
    code_commit: str
    accuracy: float | None = None
    ece: float | None = None
    artifact_path: str
    deployed_at: datetime | None = None
    is_active: bool

    model_config = {"from_attributes": True}
