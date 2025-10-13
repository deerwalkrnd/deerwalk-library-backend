from app.modules.events.domain.entities.event import Event
from app.modules.events.domain.repository.event_repository_interface import (
    EventRepositoryInterface,
)


class UpdateEventByIdUseCase:
    def __init__(self, event_repository: EventRepositoryInterface) -> None:
        self.event_repository = event_repository

    async def execute(self, id: int, new: Event) -> int:
        return await self.event_repository.update(
            conditions=Event(id=id),
            obj=new,
        )
