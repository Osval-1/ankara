from datetime import datetime

from pydantic import BaseModel

from ..models.enums import Channel, ConfidenceLevel, Crop, CropClass


class InteractionCreate(BaseModel):
    channel: Channel
    crop: Crop
    predicted_class: CropClass
    confidence_raw: float
    confidence_level: ConfidenceLevel
    advice_template_version: int | None = None
    image_ref: str | None = None
    farmer_id: int | None = None
    region: str | None = None
    escalated: bool = False
    model_version_id: int | None = None


class InteractionRead(InteractionCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
