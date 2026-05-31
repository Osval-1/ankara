from ..models.enums import Crop


class MLPrediction:
    crop_class: str
    raw_confidence: float

    def __init__(self, crop_class: str, raw_confidence: float) -> None:
        self.crop_class = crop_class
        self.raw_confidence = raw_confidence


class MLClient:
    """REST client to TF Serving. gRPC upgrade deferred to post-MVP."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    async def predict(self, crop: Crop, image_bytes: bytes) -> MLPrediction:
        raise NotImplementedError
