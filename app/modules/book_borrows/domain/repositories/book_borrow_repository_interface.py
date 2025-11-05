from abc import abstractmethod
from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.core.domain.repositories.repository_interface import RepositoryInterface
from app.modules.book_borrows.domain.entities.book_borrow import BookBorrow
from app.modules.book_borrows.domain.responses.book_borrow_response_dto import (
    BookBorrowResponseDTO,
)
from app.modules.books.domain.entities.book import Book


class BookBorrowRepositoryInterface(RepositoryInterface[BookBorrow]):
    @abstractmethod
    async def get_borrow_with_user_and_book(
        self,
        filter: BaseModel | None,
        limit: int,
        offset: int,
        sort_by: str,
        descending: bool,
        start_date: datetime | None,
        end_date: datetime | None,
        searchable_key: str | None,
        searchable_value: str | None,
    ) -> List[BookBorrowResponseDTO]:
        raise NotImplementedError

    @abstractmethod
    async def student_dashboard(self, student_id: str) -> dict[str, int | str]:
        raise NotImplementedError

    @abstractmethod
    async def librarian_dashboard(self) -> dict[str, int]:
        raise NotImplementedError

    @abstractmethod
    async def get_book_recommendations(self, limit: int, user_id: str) -> List[Book]:
        raise NotImplementedError

    @abstractmethod
    async def get_top_overdues(self, limit: int) -> List[BookBorrow]:
        raise NotImplementedError
