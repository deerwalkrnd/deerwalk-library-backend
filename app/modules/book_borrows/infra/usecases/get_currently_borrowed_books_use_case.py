from datetime import datetime
from app.modules.book_borrows.domain.entities.book_borrow import BookBorrow
from app.modules.book_borrows.domain.repositories.book_borrow_repository_interface import BookBorrowRepositoryInterface


class GetCurrentlyBorrowedBooksUseCase:
    def __init__(self, book_borrow_repository: BookBorrowRepositoryInterface) -> None:
        self.book_borrow_repository = book_borrow_repository

    async def execute(
        self,
        page: int,
        limit: int,
        start_date: datetime | None,
        end_date: datetime | None,
        searchable_key: str | None,
        searchable_value: str | None,
        sort_by: str,
        user_id: str | None,
    ):
        offset = (page - 1) * limit
        filter = BookBorrow(user_id=user_id, returned=False)

        if user_id:
            filter.user_id = user_id

        return await self.book_borrow_repository.get_borrow_with_user_and_book(
            filter=filter,
            descending=True,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            offset=offset,
            searchable_key=searchable_key,
            searchable_value=searchable_value,
            sort_by=sort_by,
        )