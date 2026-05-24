from datetime import datetime
from typing import Literal

from pydantic import Field

from app.modules.tour_catalog.schemas.common import ImageSchema, MongoBaseModel

TourType = Literal[
    "Трекинг",
    "Ретрит / оздоровительный",
    "Экскурсионный",
    "Детский",
    "Фототур",
]

Direction = Literal["Россия", "Заграница"]

ActivityLevel = Literal[
    "Для всех",
    "Низкий",
    "Средний",
    "Высокий",
    "Очень высокий",
]

ComfortLevel = Literal[
    "Высокий",
    "Уникальное жилье",
    "Средний",
]


class DiscountSchema(MongoBaseModel):
    enabled: bool = False
    endDate: datetime
    percentage: int = Field(ge=0, le=100)


class LocationSchema(MongoBaseModel):
    place_start: str = ""
    place_finish: str = ""
    time_start: str = ""
    time_finish: str = ""


class DetailsSchema(MongoBaseModel):
    included: str = ""
    notIncluded: str = ""


class HotelsSchema(MongoBaseModel):
    description: str = ""
    images: list[ImageSchema] = Field(default_factory=list)


class DayProgramSchema(MongoBaseModel):
    title: str = ""
    details: str = ""
    images: list[ImageSchema] = Field(default_factory=list)


class MapMarkerSchema(MongoBaseModel):
    id: str
    coordinates: list[float] = Field(min_length=2, max_length=2)


class FAQSchema(MongoBaseModel):
    question: str
    answer: str


class TourSchema(MongoBaseModel):
    id: str = Field(alias="_id")

    types: list[TourType]
    tour: str = ""
    slug: str

    locations: LocationSchema = Field(default_factory=LocationSchema)
    details: DetailsSchema = Field(default_factory=DetailsSchema)

    cover: ImageSchema | None = None
    gallery: list[ImageSchema] = Field(default_factory=list)

    direction: Direction
    regions: list[str] = Field(default_factory=list)

    discount: DiscountSchema | None = None

    activity: ActivityLevel
    comfort: ComfortLevel

    description: str = ""

    program: list[DayProgramSchema] = Field(default_factory=list)

    hotels: HotelsSchema = Field(default_factory=HotelsSchema)

    mapMarker: list[MapMarkerSchema] = Field(default_factory=list)
    mustKnow: list[FAQSchema] = Field(default_factory=list)

    isPublished: bool = True

    createdAt: datetime | None = None
    updatedAt: datetime | None = None
