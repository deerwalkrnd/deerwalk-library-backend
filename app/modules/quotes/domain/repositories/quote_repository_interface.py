from abc import ABC, abstractmethod

from app.core.domain.repositories.repository_interface import RepositoryInterface
from app.modules.quotes.domain.entities.quote import Quote


class QuoteRepositoryInterface(RepositoryInterface[Quote], ABC):
    @abstractmethod
    async def get_random_quote(self) -> Quote | None:
        raise NotImplementedError
