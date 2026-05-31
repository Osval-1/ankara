from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.db.database import async_get_db
from ...models.enums import Channel, Language, Crop
from ...schemas.diagnosis import DiagnosisReply, DiagnosisRequest

router = APIRouter(prefix="/diagnosis", tags=["diagnosis"])


@router.post("", response_model=DiagnosisReply)
async def diagnose(
    crop: Crop = Form(...),
    channel: Channel = Form(...),
    language: Language = Form(Language.fr),
    user_id: str | None = Form(None),
    image: UploadFile = File(...),
    db: AsyncSession = Depends(async_get_db),
) -> DiagnosisReply:
    raise NotImplementedError
