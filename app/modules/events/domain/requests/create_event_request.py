from datetime import datetime

from pydantic import BaseModel


class CreateEventRequest(BaseModel):
    name: str
    event_date: datetime
    image_url: str
    description: str
    venue: str
