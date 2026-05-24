from bson import ObjectId
from fastapi import HTTPException, status

from app.modules.tour_catalog.mappers import (
    map_schedule_item,
    map_tour_detail,
    map_tours_response,
    serialize_mongo_document,
)
from app.modules.tour_catalog.repository import TourCatalogRepository


class TourCatalogService:
    def __init__(self, repository: TourCatalogRepository):
        self.repository = repository

    def get_tours(
        self,
        filters: dict,
        sort: dict,
        page: int,
        limit: int | None,
    ):
        response = self.repository.find_tours(
            filters=filters,
            sort=sort,
            page=page,
            limit=limit,
        )

        return map_tours_response(response)

    def get_tour_list(
        self,
        for_booking: bool = False,
    ):
        if for_booking:
            future_tour_ids = self.repository.find_future_tour_ids()

            if not future_tour_ids:
                return []

            tours = self.repository.find_tour_short_list_by_ids(
                future_tour_ids,
            )

            return serialize_mongo_document(tours)

        tours = self.repository.find_tour_short_list()

        return serialize_mongo_document(tours)

    def get_tours_schedule(self):
        future_dates = self.repository.find_future_dates()

        if not future_dates:
            return {"items": []}

        tour_ids = list(
            {
                str(tour_date["tourId"])
                for tour_date in future_dates
                if tour_date.get("tourId") is not None
            }
        )

        tours = self.repository.find_published_tours_by_ids(tour_ids)

        tour_map = {str(tour["_id"]): tour for tour in tours}

        items = []

        for tour_date in future_dates:
            tour_id = str(tour_date.get("tourId"))
            tour = tour_map.get(tour_id)

            if not tour:
                continue

            items.append(
                map_schedule_item(
                    tour=tour,
                    tour_date=tour_date,
                )
            )

        items.sort(key=lambda item: item["dateStart"])

        return {"items": items}

    def get_tour(self, param: str):
        tour = self._find_tour(param)

        if not tour:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Тур не найден",
            )

        future_dates = self.repository.find_future_dates_for_tour(
            tour_id=str(tour["_id"]),
        )

        return map_tour_detail(
            tour=tour,
            dates=future_dates,
        )

    def _find_tour(self, param: str):
        if ObjectId.is_valid(param):
            return self.repository.find_tour_by_id(param)

        return self.repository.find_tour_by_slug(param)
