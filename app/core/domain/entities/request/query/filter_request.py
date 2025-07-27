from pydantic import BaseModel, Field
from datetime import datetime


class FilterParams(BaseModel):
    searchable_value: str | None = Field(default=None, min_length=1, max_length=200)
    searchable_field: str | None = Field(default=None, min_length=1, max_length=200)
    starts: datetime | None = None
    ends: datetime | None = None
