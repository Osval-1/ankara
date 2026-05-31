from fastapi import APIRouter

from .health import router as health_router
from .login import router as login_router
from .logout import router as logout_router
from .users import router as users_router

router = APIRouter(prefix="/v1")
router.include_router(health_router)
router.include_router(login_router)
router.include_router(logout_router)
router.include_router(users_router)
# Crop Doctor domain routers added here as they are built:
# from .diagnosis import router as diagnosis_router
# from .interactions import router as interactions_router
# from .advice_templates import router as advice_templates_router
