from app.modules.events.domain.entities.event import Event
from app.modules.events.domain.repositories.event_repository_interface import (
    EventRepositoryInterface,
)


class GetEventByIdUseCase:
    def __init__(self, event_repository: EventRepositoryInterface) -> None:
        self.event_repository = event_repository

    async def execute(self, id: int) -> Event:
        event = await self.event_repository.find_one(obj=Event(id=id))

        if not event:
            raise ValueError("no such event")

        return event
