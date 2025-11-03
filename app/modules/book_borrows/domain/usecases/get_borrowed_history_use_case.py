from datetime import datetime
from app.modules.book_borrows.domain.entities.book_borrow import BookBorrow
from app.modules.book_borrows.domain.repositories.book_borrow_repository_interface import (
    BookBorrowRepositoryInterface,
)


class GetBorrowedHistoryUseCase:
    def __init__(self, book_borrow_repository: BookBorrowRepositoryInterface) -> None:
        self.book_borrow_repository = book_borrow_repository

    async def execute(
        self,
        user_id: str,
        limit: int,
        page: int,
        starts: datetime | None,
        ends: datetime | None,
        searchable_key: str | None,
        searchable_value: str | None,
    ):
        offset = (page - 1) * limit
        return await self.book_borrow_repository.filter(
            filter=BookBorrow(
                user_id=user_id,
                returned=True,
            ),
            descending=True,
            start_date=starts,
            end_date=ends,
            limit=limit,
            offset=offset,
            searchable_key=searchable_key,
            searchable_value=searchable_value,
            sort_by="created_at",
        )
