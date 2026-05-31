from datetime import datetime

from pydantic import BaseModel

from ..models.enums import Crop, CropClass, Language


class AdviceTemplateRead(BaseModel):
    id: int
    crop: Crop
    crop_class: CropClass
    language: Language
    version: int
    label: str
    opening: str
    steps: list[str]
    consult_message: str
    reviewed_by: str | None = None
    reviewed_at: datetime | None = None
    is_active: bool

    model_config = {"from_attributes": True}


class AdviceTemplateUpdate(BaseModel):
    label: str | None = None
    opening: str | None = None
    steps: list[str] | None = None
    consult_message: str | None = None
    reviewed_by: str | None = None
    is_active: bool | None = None
