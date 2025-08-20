from datetime import datetime

from app.modules.events.domain.entities.event import Event
from app.modules.events.domain.repository.event_repository_interface import (
    EventRepositoryInterface,
)


class CreateEventUseCase:
    def __init__(self, event_repository: EventRepositoryInterface) -> None:
        self.event_repository = event_repository

    async def execute(
        self, name: str, description: str, image_url: str, event_date: datetime
    ) -> Event | None:
        event = Event(
            name=name,
            description=description,
            image_url=image_url,
            event_date=event_date,
        )

        e = await self.event_repository.create(event)

        return e
