from abc import abstractmethod
from typing import Optional
from app.core.domain.repositories.repository_interface import RepositoryInterface
from app.modules.reserves.domain.entities.reserve import Reserve


class ReservesRepositoryInterface(RepositoryInterface[Reserve]):
    @abstractmethod
    async def get_reserves_by_book(
        self, user_id: str, book_id: int
    ) -> Optional[Reserve]:
        raise NotImplementedError
