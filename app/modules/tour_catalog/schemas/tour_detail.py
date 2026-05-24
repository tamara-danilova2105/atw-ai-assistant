from app.modules.tour_catalog.schemas.tour import TourSchema
from pydantic import Field

from app.modules.tour_catalog.schemas.tour_date import TourDateSchema


class TourDetailSchema(TourSchema):
    dates: list[TourDateSchema] = Field(default_factory=list)
