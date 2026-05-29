from app.modules.assistant.filter_extractor import FilterExtractor
from app.modules.assistant.schemas import (
    CatalogToursResponse,
    ConsultationRequest,
    ConsultationResponse,
    MatchedTour,
)
from app.modules.assistant.tour_context_builder import TourContextBuilder
from app.modules.assistant.tour_search_adapter import AssistantTourSearchAdapter


class AssistantService:
    def __init__(
        self,
        filter_extractor: FilterExtractor,
        tour_search_adapter: AssistantTourSearchAdapter,
        tour_context_builder: TourContextBuilder,
    ):
        self.filter_extractor = filter_extractor
        self.tour_search_adapter = tour_search_adapter
        self.tour_context_builder = tour_context_builder

    def consult(
        self,
        request: ConsultationRequest,
    ) -> ConsultationResponse:
        if request.selected_tour_id:
            return self._answer_about_selected_tour(request)

        return self._search_tours(request)

    def _search_tours(
        self,
        request: ConsultationRequest,
    ) -> ConsultationResponse:
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
        )

    def _answer_about_selected_tour(
        self,
        request: ConsultationRequest,
    ) -> ConsultationResponse:
        if not request.selected_tour_id:
            return ConsultationResponse(
                answer="Какой тур вас интересует?",
                extracted_filters=None,
                matched_tours=[],
                suggested_questions=[],
                needs_clarification=True,
            )

        tour = self.tour_search_adapter.get_tour_by_id(request.selected_tour_id)

        if not tour:
            return ConsultationResponse(
                answer="Не удалось найти выбранный тур.",
                extracted_filters=None,
                matched_tours=[],
                suggested_questions=[],
                needs_clarification=True,
            )

        tour_context = self.tour_context_builder.build(
            tour=tour,
            user_message=request.message,
        )

        return ConsultationResponse(
            answer=tour_context,
            extracted_filters=None,
            matched_tours=[],
            suggested_questions=[
                "Что входит в стоимость?",
                "Что не входит в стоимость?",
                "Какое размещение?",
                "Какие есть даты?",
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
