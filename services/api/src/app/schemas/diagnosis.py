from pydantic import BaseModel

from ..models.enums import Channel, ConfidenceLevel, Crop, CropClass, Language


class DiagnosisRequest(BaseModel):
    crop: Crop
    image_ref: str
    user_id: str | None = None
    channel: Channel
    language: Language = Language.fr


class DiagnosisReply(BaseModel):
    crop: Crop
    predicted_class: CropClass
    confidence: ConfidenceLevel
    label: str
    opening: str
    steps: list[str]
    consult_message: str
    escalate: bool
    advice_template_version: int | None = None
