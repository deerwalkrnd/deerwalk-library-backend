from app.modules.book_borrow.domain.entities.book_borrow import BookBorrow
from app.modules.book_borrow.domain.repository.book_borrow_repository_interface import (
    BookBorrowRepositoryInterface,
)


class GetBookBorrowByIdUseCase:
    def __init__(self, book_borrow_repository: BookBorrowRepositoryInterface) -> None:
        self.book_borrow_repository = book_borrow_repository

    async def execute(self, book_borrow_id: int) -> BookBorrow | None:
        return await self.book_borrow_repository.find_one(
            obj=BookBorrow(id=book_borrow_id)
        )
