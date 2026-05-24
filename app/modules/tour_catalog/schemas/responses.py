from app.modules.tour_catalog.schemas.tour import TourSchema
from pydantic import Field

from app.modules.tour_catalog.schemas.common import MongoBaseModel


class ToursResponse(MongoBaseModel):
    tours: list[TourSchema] = Field(default_factory=list)
    allTours: int
    currentPage: int | None = None
    totalPages: int | None = None


class TourListItemSchema(MongoBaseModel):
    id: str
    tour: str


class ScheduleItemSchema(MongoBaseModel):
    tourId: str
    slug: str
    tour: str
    dateStart: str
    dateEnd: str
    spots: int | None = None
    regions: list[str] = Field(default_factory=list)


class ToursScheduleResponse(MongoBaseModel):
    items: list[ScheduleItemSchema] = Field(default_factory=list)
