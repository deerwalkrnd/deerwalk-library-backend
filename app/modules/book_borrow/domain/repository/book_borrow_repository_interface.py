from abc import abstractmethod
from typing import List
from app.core.domain.repositories.repository_interface import RepositoryInterface
from app.modules.book_borrow.domain.entities.book_borrow import BookBorrow
from pydantic import BaseModel
from datetime import datetime

from app.modules.book_borrow.domain.response.book_borrow_response_dto import (
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
