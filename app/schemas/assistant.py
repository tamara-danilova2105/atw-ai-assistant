from pydantic import BaseModel, Field


# объект запроса, который API извлекает из сообщения пользователя
class SearchFilters(BaseModel):
    region: str | None = None
    direction: str | None = None
    month: int | None = None
    max_price: int | None = None
    days_count: int | None = None
    activity: str | None = None
    comfort: str | None = None


# если пользователь уже находится на странице тура, можно передавать selected_tour_id
class ConsultationRequest(BaseModel):
    message: str
    selected_tour_id: str | None = None
    conversation_id: str | None = None


class MatchedTour(BaseModel):
    id: str
    title: str
    slug: str
    reason: str | None = None


class ConsultationResponse(BaseModel):
    # текстовый ответ AI в чате
    answer: str
    # AI извлекает структурированные параметры поиска из текста пользователя.
    extracted_filters: SearchFilters | None = None
    # cписок туров, которые AI считает подходящими.
    matched_tours: list[MatchedTour] = Field(default_factory=list)
    # подсказки для продолжения диалога.
    suggested_questions: list[str] = Field(default_factory=list)
    # понял ли AI запрос достаточно хорошо.
    needs_clarification: bool = False
