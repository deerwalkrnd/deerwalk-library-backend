from app.modules.events.domain.entities.event import Event
from app.modules.events.domain.repository.event_repository_interface import (
    EventRepositoryInterface,
)


class DeleteEventByIdUseCase:
    def __init__(self, event_repository: EventRepositoryInterface) -> None:
        self.event_repository = event_repository

    async def execute(self, id: int) -> None:
        await self.event_repository.delete(conditions=Event(id=id))
