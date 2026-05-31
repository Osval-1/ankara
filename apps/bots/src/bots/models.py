from enum import Enum

from pydantic import BaseModel


class Crop(str, Enum):
    cassava = "cassava"
    maize = "maize"
    plantain = "plantain"
    tomato = "tomato"
    cocoa = "cocoa"


class Channel(str, Enum):
    whatsapp = "whatsapp"
    telegram = "telegram"


class Language(str, Enum):
    fr = "fr"
    en = "en"


class NormalizedMessage(BaseModel):
    """Platform-agnostic inbound message, produced by each adapter."""
    channel_id: str          # hashed phone / chat ID
    channel: Channel
    language: Language
    text: str | None = None
    image_bytes: bytes | None = None
    crop: Crop | None = None


class ConversationState(str, Enum):
    greeting = "greeting"
    awaiting_crop = "awaiting_crop"
    awaiting_photo = "awaiting_photo"
    awaiting_consent = "awaiting_consent"
    idle = "idle"
