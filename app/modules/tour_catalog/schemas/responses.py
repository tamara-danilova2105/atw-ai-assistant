from pydantic import Field

from app.modules.tour_catalog.schemas.common import MongoBaseModel
from app.modules.tour_catalog.schemas.tours import (
    ScheduleItemSchema,
    ToursItemSchema,
)


class ToursResponse(MongoBaseModel):
    tours: list[ToursItemSchema] = Field(default_factory=list)
    allTours: int
    currentPage: int | None = None
    totalPages: int | None = None


class ToursScheduleResponse(MongoBaseModel):
    items: list[ScheduleItemSchema] = Field(default_factory=list)
