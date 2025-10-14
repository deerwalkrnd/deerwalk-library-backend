from app.modules.events.domain.entities.event import Event
from app.modules.events.domain.repositories.event_repository_interface import (
    EventRepositoryInterface,
)


class GetLatestEventUseCase:
    def __init__(self, event_repository: EventRepositoryInterface) -> None:
        self.event_repository = event_repository

    async def execute(self) -> Event | None:
        events = await self.event_repository.find_many(
            limit=1, descending=True, offset=0, sort_by="created_at", filter=None
        )

        if len(events) == 0:
            return None

        return events[0]
