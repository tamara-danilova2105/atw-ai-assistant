from fastapi import APIRouter
import structlog

router = APIRouter()
log = structlog.get_logger()

@router.get("/health")
async def health():
    return {"status": "ok"}
