from datetime import datetime

from pydantic import BaseModel


class UpdateEventRequest(BaseModel):
    name: str | None = None
    event_date: datetime | None = None
    image_url: str | None = None
    description: str | None = None
    venue: str | None = None
