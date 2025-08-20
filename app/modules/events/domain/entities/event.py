from pydantic import BaseModel, ConfigDict
from datetime import datetime


class Event(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int | None = None
    name: str | None = None
    event_date: datetime | None = None
    image_url: str | None = None
    description: str | None = None
