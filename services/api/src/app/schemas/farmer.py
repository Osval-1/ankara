from datetime import datetime

from pydantic import BaseModel

from ..models.enums import Channel, Language


class FarmerCreate(BaseModel):
    channel_id: str
    channel: Channel
    region: str | None = None
    language: Language = Language.fr
    retain_photos: bool = False


class FarmerRead(FarmerCreate):
    id: int
    created_at: datetime
    consent_given_at: datetime | None = None

    model_config = {"from_attributes": True}
