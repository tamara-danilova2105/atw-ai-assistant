from typing import Annotated

from fastapi import APIRouter, Depends

from app.modules.assistant.assistant_service import AssistantService
from app.modules.assistant.dependencies import get_assistant_service
from app.modules.assistant.schemas import ConsultationRequest, ConsultationResponse

router = APIRouter(prefix="/assistant", tags=["assistant"])


@router.post("/chat", response_model=ConsultationResponse)
def chat(
    request: ConsultationRequest,
    assistant_service: Annotated[
        AssistantService,
        Depends(get_assistant_service),
    ],
) -> ConsultationResponse:
    return assistant_service.consult(request)
