from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class MongoBaseModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class ImageSchema(MongoBaseModel):
    id: str = Field(alias="_id")
    src: str


Currency = Literal["₽", "$", "€"]


class PriceSchema(MongoBaseModel):
    amount: float
    discount: float | None = None
    currency: Currency


class DiscountSchema(MongoBaseModel):
    enabled: bool = False
    endDate: datetime
    percentage: int = Field(ge=0, le=100)
