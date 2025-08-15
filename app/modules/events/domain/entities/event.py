from pydantic import BaseModel
from datetime import datetime


class Event(BaseModel):
    id: int | None = None
    name: str | None = None
    event_date: datetime | None = None
    image_url: str | None = None
    description: str | None = None
