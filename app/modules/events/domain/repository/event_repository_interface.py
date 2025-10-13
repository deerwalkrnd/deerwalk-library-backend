from app.core.domain.repositories.repository_interface import \
    RepositoryInterface
from app.modules.events.domain.entities.event import Event


class EventRepositoryInterface(RepositoryInterface[Event]):
    pass
