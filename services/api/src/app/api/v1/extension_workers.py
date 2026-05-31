from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.db.database import async_get_db
from ...schemas.extension_worker import ExtensionWorkerRead

router = APIRouter(prefix="/extension-workers", tags=["extension-workers"])


@router.get("", response_model=list[ExtensionWorkerRead])
async def list_extension_workers(
    region: str | None = None,
    db: AsyncSession = Depends(async_get_db),
) -> list[ExtensionWorkerRead]:
    raise NotImplementedError
