from abc import abstractmethod
from typing import Set

from app.core.domain.repositories.repository_interface import RepositoryInterface
from app.modules.books.domain.entities.book_copy import BookCopy


class BookCopyRepositoryInterface(RepositoryInterface[BookCopy]):
    @abstractmethod
    async def get_all_unique_identifiers(self) -> Set[str]:
        raise NotImplementedError
