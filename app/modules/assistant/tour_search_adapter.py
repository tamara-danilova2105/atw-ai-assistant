from calendar import monthrange
from datetime import date

from app.modules.assistant.schemas import (
    CatalogDateRange,
    CatalogFilters,
    CatalogToursResponse,
    SearchFilters,
)
from app.modules.tour_catalog.service import TourCatalogService


class AssistantTourSearchAdapter:
    def __init__(self, tour_catalog_service: TourCatalogService):
        self.tour_catalog_service = tour_catalog_service

    def search(self, filters: SearchFilters) -> CatalogToursResponse:
        catalog_filters = self.to_catalog_filters(filters)

        response = self.tour_catalog_service.get_tours(
            filters=catalog_filters.model_dump(exclude_none=True),
            sort={},
            page=1,
            limit=5,
        )

        parsed_response = CatalogToursResponse.model_validate(response)

        return parsed_response

    def to_catalog_filters(
        self,
        filters: SearchFilters,
    ) -> CatalogFilters:
        catalog_filters = CatalogFilters()

        if filters.region:
            catalog_filters.region = [filters.region]

        if filters.max_price:
            catalog_filters.price = [0, filters.max_price]

        if filters.days_count:
            catalog_filters.duration = [
                filters.days_count,
                filters.days_count,
            ]

        if filters.month:
            catalog_filters.dates = self._month_to_date_range(
                month=filters.month,
                year=filters.year,
            )

        return catalog_filters

    def _month_to_date_range(
        self,
        month: int,
        year: int | None = None,
    ) -> CatalogDateRange:
        target_year = year or date.today().year
        _, last_day = monthrange(target_year, month)

        return CatalogDateRange(
            startDate=date(target_year, month, 1).isoformat(),
            endDate=date(target_year, month, last_day).isoformat(),
        )
