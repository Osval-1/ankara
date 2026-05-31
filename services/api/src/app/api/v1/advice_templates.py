from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.db.database import async_get_db
from ...schemas.advice_template import AdviceTemplateRead, AdviceTemplateUpdate

router = APIRouter(prefix="/advice-templates", tags=["advice-templates"])


@router.get("", response_model=list[AdviceTemplateRead])
async def list_advice_templates(
    db: AsyncSession = Depends(async_get_db),
) -> list[AdviceTemplateRead]:
    raise NotImplementedError


@router.put("/{template_id}", response_model=AdviceTemplateRead)
async def update_advice_template(
    template_id: int,
    payload: AdviceTemplateUpdate,
    db: AsyncSession = Depends(async_get_db),
) -> AdviceTemplateRead:
    raise NotImplementedError
