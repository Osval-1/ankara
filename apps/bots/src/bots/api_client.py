import httpx

from .config import settings
from .models import Crop, Language


class DiagnosisReply:
    predicted_class: str
    confidence: str
    label: str
    opening: str
    steps: list[str]
    consult_message: str
    escalate: bool

    def __init__(self, data: dict) -> None:
        self.predicted_class = data["predicted_class"]
        self.confidence = data["confidence"]
        self.label = data["label"]
        self.opening = data["opening"]
        self.steps = data["steps"]
        self.consult_message = data["consult_message"]
        self.escalate = data["escalate"]


class APIClient:
    """Thin async client wrapping the FastAPI backend."""

    def __init__(self) -> None:
        self._client = httpx.AsyncClient(base_url=settings.API_BASE_URL, timeout=30)

    async def diagnose(
        self,
        crop: Crop,
        image_bytes: bytes,
        channel: str,
        language: Language,
        user_id: str | None = None,
    ) -> DiagnosisReply:
        response = await self._client.post(
            "/diagnosis",
            data={"crop": crop.value, "channel": channel, "language": language.value, "user_id": user_id},
            files={"image": ("photo.jpg", image_bytes, "image/jpeg")},
        )
        response.raise_for_status()
        return DiagnosisReply(response.json())

    async def aclose(self) -> None:
        await self._client.aclose()
