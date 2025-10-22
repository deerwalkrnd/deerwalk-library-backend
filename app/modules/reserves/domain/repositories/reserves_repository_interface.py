from app.core.domain.repositories.repository_interface import RepositoryInterface
from app.modules.reserves.domain.entities.reserve import Reserve


class ReservesRepositoryInterface(RepositoryInterface[Reserve]):
    pass
