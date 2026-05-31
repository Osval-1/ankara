from sqlalchemy.ext.asyncio import AsyncSession

from ..models.enums import Channel, ConfidenceLevel, Language
from ..schemas.diagnosis import DiagnosisReply, DiagnosisRequest
from .confidence_calibrator import ConfidenceCalibrator
from .ml_client import MLClient
from .r2_client import R2Client


class DiagnosisService:
    """
    Orchestrates the full diagnosis flow:
    1. Upload image to R2
    2. Call ML inference
    3. Calibrate confidence
    4. Load advice template from DB
    5. Log interaction
    6. Return reply
    """

    def __init__(self, db: AsyncSession, r2: R2Client, ml: MLClient) -> None:
        self.db = db
        self.r2 = r2
        self.ml = ml
        self.calibrator = ConfidenceCalibrator()

    async def diagnose(self, request: DiagnosisRequest, image_bytes: bytes) -> DiagnosisReply:
        raise NotImplementedError
