from abc import abstractmethod
from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.core.domain.repositories.repository_interface import RepositoryInterface
from app.modules.book_borrows.domain.entities.book_borrow import BookBorrow
from app.modules.book_borrows.domain.responses.book_borrow_response_dto import (
    BookBorrowResponseDTO,
)


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
