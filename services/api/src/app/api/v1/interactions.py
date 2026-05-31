from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.db.database import async_get_db
from ...schemas.interaction import InteractionRead

router = APIRouter(prefix="/interactions", tags=["interactions"])


@router.get("", response_model=list[InteractionRead])
async def list_interactions(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(async_get_db),
) -> list[InteractionRead]:
    raise NotImplementedError
