from pydantic import Field

from app.modules.tour_catalog.schemas.common import (
    DiscountSchema,
    ImageSchema,
    MongoBaseModel,
)
from app.modules.tour_catalog.schemas.tour_date import TourDateSchema


class ToursItemSchema(MongoBaseModel):
    id: str = Field(alias="_id")
    tour: str
    slug: str
    cover: ImageSchema | None = None
    discount: DiscountSchema | None = None
    regions: list[str] = Field(default_factory=list)
    isPublished: bool
    dates: list[TourDateSchema] = Field(default_factory=list)


class ScheduleItemSchema(MongoBaseModel):
    tourId: str
    slug: str
    tour: str
    dateStart: str
    dateEnd: str
    spots: int | None = None
    regions: list[str] = Field(default_factory=list)


class ListItemSchema(MongoBaseModel):
    id: str = Field(alias="_id")
    tour: str
