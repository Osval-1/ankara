from fastapi import APIRouter

from .advice_templates import router as advice_templates_router
from .diagnosis import router as diagnosis_router
from .extension_workers import router as extension_workers_router
from .health import router as health_router
from .interactions import router as interactions_router
from .login import router as login_router
from .logout import router as logout_router
from .model_versions import router as model_versions_router
from .users import router as users_router
from .webhooks import router as webhooks_router

router = APIRouter(prefix="/v1")
router.include_router(health_router)
router.include_router(login_router)
router.include_router(logout_router)
router.include_router(users_router)
router.include_router(diagnosis_router)
router.include_router(interactions_router)
router.include_router(advice_templates_router)
router.include_router(extension_workers_router)
router.include_router(model_versions_router)
router.include_router(webhooks_router)
