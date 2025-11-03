from abc import abstractmethod
from typing import List
from app.core.domain.repositories.repository_interface import RepositoryInterface
from app.modules.books.domain.entities.book import Book


class BookRepositoryInterface(RepositoryInterface[Book]):
    @abstractmethod
    async def get_total_books_count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_top_books_borrowed(self, limit: int) -> List[Book]:
        raise NotImplementedError
