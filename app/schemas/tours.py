from datetime import datetime

from pydantic import BaseModel, Field


class Price(BaseModel):
    amount: int
    currency: str


class TourDate(BaseModel):
    id: str = Field(alias="_id")
    date_start: datetime
    date_finish: datetime
    days_count: int
    price: Price
    spots: int
    spots_total: int = Field(alias="spotsTotal")
    status: str


class TourDetails(BaseModel):
    included: str | None = None
    not_included: str | None = Field(default=None, alias="notIncluded")


class TourLocations(BaseModel):
    place_start: str | None = None
    place_finish: str | None = None
    time_start: str | None = None
    time_finish: str | None = None


class TourHotels(BaseModel):
    description: str | None = None


class TourProgramDay(BaseModel):
    title: str
    details: str | None = None


class Tour(BaseModel):
    id: str = Field(alias="_id")
    types: list[str] = []
    title: str = Field(alias="tour")
    slug: str
    dates: list[TourDate] = []

    locations: TourLocations | None = None
    details: TourDetails | None = None
    direction: str | None = None
    regions: list[str] = []
    activity: str | None = None
    comfort: str | None = None
    description: str | None = None
    program: list[TourProgramDay] = []
    hotels: TourHotels | None = None

    must_know: list[str] = Field(default_factory=list, alias="mustKnow")
    is_published: bool = Field(default=True, alias="isPublished")
