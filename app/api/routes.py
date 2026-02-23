import structlog
from fastapi import APIRouter

router = APIRouter()
log = structlog.get_logger()


@router.get("/health")
async def health():
    return {"status": "ok"}
