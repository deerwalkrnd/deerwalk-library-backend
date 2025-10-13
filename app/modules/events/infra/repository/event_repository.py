from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infra.repositories.repository import Repository
from app.core.models.event import EventModel
from app.modules.events.domain.entities.event import Event
from app.modules.events.domain.repository.event_repository_interface import \
    EventRepositoryInterface


class EventRepository(Repository[EventModel, Event], EventRepositoryInterface):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, EventModel, Event)
