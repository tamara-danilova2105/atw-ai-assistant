from datetime import datetime
from typing import Literal

from pydantic import Field

from app.modules.tour_catalog.schemas.common import MongoBaseModel, PriceSchema

TourDateStatus = Literal[
    "draft",
    "active",
    "sold_out",
    "canceled",
]


class TourDateSchema(MongoBaseModel):
    id: str = Field(alias="_id")

    tourId: str

    date_start: datetime
    date_finish: datetime

    days_count: int = Field(ge=0)

    price: PriceSchema

    spotsTotal: int = Field(ge=0)
    spots: int = Field(ge=0)

    status: TourDateStatus = "active"

    createdAt: datetime | None = None
    updatedAt: datetime | None = None
