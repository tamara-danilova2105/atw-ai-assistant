from fastapi import APIRouter

from app.modules.tour_catalog.router import router as tour_catalog_router

router = APIRouter()

router.include_router(tour_catalog_router)
