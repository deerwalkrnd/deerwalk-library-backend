from typing import List
from app.modules.book_borrows.domain.entities.book_borrow import BookBorrow
from app.modules.book_borrows.domain.repositories.book_borrow_repository_interface import (
    BookBorrowRepositoryInterface,
)


class GetTopOverduesUseCase:
    def __init__(self, book_borrow_repository: BookBorrowRepositoryInterface) -> None:
        self.book_borrow_repository = book_borrow_repository

    async def execute(self, limit: int) -> List[BookBorrow]:
        return await self.book_borrow_repository.filter(
            limit=limit,
            offset=0,
            filter=BookBorrow(
                returned=False,
            ),
            sort_by="created_at",
            descending=False,
            start_date=None,
            end_date=None,
            searchable_key=None,
            searchable_value=None,
        )
