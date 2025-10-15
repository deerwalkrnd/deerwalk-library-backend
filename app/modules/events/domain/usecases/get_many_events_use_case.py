from datetime import datetime
from typing import List

from app.modules.events.domain.entities.event import Event
from app.modules.events.domain.repositories.event_repository_interface import (
    EventRepositoryInterface,
)


class GetManyEventsUseCase:
    def __init__(self, event_repository: EventRepositoryInterface) -> None:
        self.event_repository = event_repository

    async def execute(
        self, page: int, limit: int, starts: datetime, ends: datetime
    ) -> List[Event]:
        offset = (page - 1) * limit

        events = await self.event_repository.filter(
            descending=True,
            sort_by="created_at",
            offset=offset,
            start_date=starts,
            end_date=ends,
            limit=limit,
            searchable_key=None,
            searchable_value=None,
            filter=None,
        )
        return events
