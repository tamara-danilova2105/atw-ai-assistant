import json

from fastapi import APIRouter, Query

from app.modules.tour_catalog.repository import TourCatalogRepository
from app.modules.tour_catalog.service import TourCatalogService

router = APIRouter(
    prefix="/tours",
    tags=["Tours"],
)

repository = TourCatalogRepository()
service = TourCatalogService(repository)


@router.get("/")
def get_tours(
    filter: str | None = Query(default=None),
    sort: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int | None = Query(default=None, ge=1),
):
    parsed_filters = json.loads(filter) if filter else {}
    parsed_sort = json.loads(sort) if sort else {}

    return service.get_tours(
        filters=parsed_filters,
        sort=parsed_sort,
        page=page,
        limit=limit,
    )


@router.get("/list")
def get_tour_list(
    forBooking: bool = False,
):
    return service.get_tour_list(
        for_booking=forBooking,
    )


@router.get("/schedule")
def get_tours_schedule():
    return service.get_tours_schedule()


@router.get("/{param}")
def get_tour(param: str):
    return service.get_tour(param)
