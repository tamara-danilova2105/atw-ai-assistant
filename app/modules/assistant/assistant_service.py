from app.modules.assistant.filter_extractor import FilterExtractor
from app.modules.assistant.schemas import (
    CatalogToursResponse,
    ConsultationRequest,
    ConsultationResponse,
    MatchedTour,
)
from app.modules.assistant.tour_search_adapter import AssistantTourSearchAdapter


class AssistantService:
    def __init__(
        self,
        filter_extractor: FilterExtractor,
        tour_search_adapter: AssistantTourSearchAdapter,
    ):
        self.filter_extractor = filter_extractor
        self.tour_search_adapter = tour_search_adapter

    def consult(self, request: ConsultationRequest) -> ConsultationResponse:
        filters = self.filter_extractor.extract(request.message)
        tours_response = self.tour_search_adapter.search(filters)

        matched_tours = self._map_matched_tours(tours_response)

        return ConsultationResponse(
            answer="Я нашла подходящие туры по вашему запросу.",
            extracted_filters=filters,
            matched_tours=matched_tours,
            suggested_questions=[
                "Что входит в стоимость?",
                "Какие есть даты?",
                "Какое размещение?",
            ],
            needs_clarification=False,
        )

    def _map_matched_tours(
        self,
        tours_response: CatalogToursResponse,
    ) -> list[MatchedTour]:
        return [
            MatchedTour(
                id=item.id or item._id or "",
                title=item.title or item.tour or "Без названия",
                slug=item.slug or "",
                reason="Подходит по указанным фильтрам.",
            )
            for item in tours_response.tours
        ]
