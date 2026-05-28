from app.modules.assistant.assistant_service import AssistantService
from app.modules.assistant.filter_extractor import FilterExtractor
from app.modules.assistant.tour_search_adapter import AssistantTourSearchAdapter
from app.modules.tour_catalog.repository import TourCatalogRepository
from app.modules.tour_catalog.service import TourCatalogService


def get_assistant_service() -> AssistantService:
    tour_catalog_repository = TourCatalogRepository()

    tour_catalog_service = TourCatalogService(
        repository=tour_catalog_repository,
    )

    tour_search_adapter = AssistantTourSearchAdapter(
        tour_catalog_service=tour_catalog_service,
    )

    filter_extractor = FilterExtractor()

    return AssistantService(
        filter_extractor=filter_extractor,
        tour_search_adapter=tour_search_adapter,
    )
