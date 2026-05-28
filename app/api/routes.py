from fastapi import APIRouter

from app.modules.assistant.router import router as assistant_router
from app.modules.tour_catalog.router import router as tour_catalog_router

router = APIRouter()

router.include_router(tour_catalog_router)
router.include_router(assistant_router)
