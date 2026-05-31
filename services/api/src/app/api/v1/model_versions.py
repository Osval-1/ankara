from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.db.database import async_get_db
from ...schemas.model_version import ModelVersionRead

router = APIRouter(prefix="/model-versions", tags=["model-versions"])


@router.get("", response_model=list[ModelVersionRead])
async def list_model_versions(
    db: AsyncSession = Depends(async_get_db),
) -> list[ModelVersionRead]:
    raise NotImplementedError
