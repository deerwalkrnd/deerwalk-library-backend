from fastapi import Depends

from app.core.dependencies.middleware.get_current_librarian import get_current_librarian
from app.core.domain.entities.user import User
from app.modules.events.domain.entities.event import Event
from app.modules.events.domain.request.create_event_request import CreateEventRequest


class EventsController:
    def __init__(self) -> None:
        pass

    async def create_event(
        self,
        create_event_request: CreateEventRequest,
        librarian: User = Depends(get_current_librarian),
    ) -> Event:
        raise NotImplementedError
