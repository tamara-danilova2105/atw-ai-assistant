from datetime import UTC, datetime

from bson import ObjectId

from app.db.mongo import db
from app.modules.tour_catalog.pipeline import build_tours_pipeline


class TourCatalogRepository:
    def __init__(self):
        self.tours = db["tours"]
        self.tour_dates = db["tourdates"]

    def find_tours(
        self,
        filters: dict,
        sort: dict,
        page: int,
        limit: int | None,
    ):
        pipeline = build_tours_pipeline(
            filters=filters,
            sort=sort,
            page=page,
            limit=limit,
        )

        result = list(self.tours.aggregate(pipeline))

        if not limit:
            return {
                "tours": result,
                "allTours": len(result),
                "currentPage": None,
                "totalPages": None,
            }

        facet = (
            result[0]
            if result
            else {
                "tours": [],
                "total": [],
            }
        )

        total = facet.get("total", [{}])[0].get("count", 0) if facet.get("total") else 0

        return {
            "tours": facet.get("tours", []),
            "allTours": total,
            "currentPage": page,
            "totalPages": (total + limit - 1) // limit if limit else None,
        }

    def find_tour_by_id(self, tour_id: str):
        if not ObjectId.is_valid(tour_id):
            return None

        return self.tours.find_one(
            {
                "_id": ObjectId(tour_id),
                "isPublished": True,
            }
        )

    def find_tour_by_slug(self, slug: str):
        return self.tours.find_one(
            {
                "slug": slug,
                "isPublished": True,
            }
        )

    def find_tour_short_list(self):
        cursor = self.tours.find(
            {
                "isPublished": True,
            },
            {
                "_id": 1,
                "tour": 1,
            },
        ).sort("tour", 1)

        return list(cursor)

    def find_tour_short_list_by_ids(
        self,
        tour_ids: list[str],
    ):
        object_ids = self._to_object_ids(tour_ids)

        if not object_ids:
            return []

        cursor = self.tours.find(
            {
                "_id": {"$in": object_ids},
                "isPublished": True,
            },
            {
                "_id": 1,
                "tour": 1,
            },
        ).sort("tour", 1)

        return list(cursor)

    def find_future_dates(self):
        cursor = self.tour_dates.find(
            {
                "date_start": {
                    "$gte": datetime.now(UTC),
                },
                "status": {
                    "$ne": "canceled",
                },
            },
            {
                "tourId": 1,
                "date_start": 1,
                "date_finish": 1,
                "spots": 1,
            },
        ).sort("date_start", 1)

        return list(cursor)

    def find_future_dates_for_tour(
        self,
        tour_id: str,
    ):
        if not ObjectId.is_valid(tour_id):
            return []

        cursor = self.tour_dates.find(
            {
                "tourId": ObjectId(tour_id),
                "date_start": {
                    "$gte": datetime.now(UTC),
                },
                "status": {
                    "$ne": "canceled",
                },
            }
        ).sort("date_start", 1)

        return list(cursor)

    def find_future_tour_ids(self):
        dates = self.find_future_dates()

        return list({str(date["tourId"]) for date in dates if date.get("tourId") is not None})

    def find_published_tours_by_ids(
        self,
        tour_ids: list[str],
    ):
        object_ids = self._to_object_ids(tour_ids)

        if not object_ids:
            return []

        cursor = self.tours.find(
            {
                "_id": {"$in": object_ids},
                "isPublished": True,
            },
            {
                "slug": 1,
                "tour": 1,
                "regions": 1,
            },
        )

        return list(cursor)

    def _to_object_ids(
        self,
        ids: list[str],
    ):
        return [ObjectId(item) for item in ids if ObjectId.is_valid(item)]
