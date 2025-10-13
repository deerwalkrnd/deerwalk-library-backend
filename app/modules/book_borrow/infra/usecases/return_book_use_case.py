from app.core.models.book_borrow import FineStatus
from app.modules.book_borrow.domain.entities.book_borrow import BookBorrow
from app.modules.book_borrow.domain.repository.book_borrow_repository_interface import (
    BookBorrowRepositoryInterface,
)
from datetime import datetime


class ReturnBookUseCase:
    def __init__(self, book_borrow_repository: BookBorrowRepositoryInterface) -> None:
        self.book_borrow_repository = book_borrow_repository

    async def execute(
        self,
        book_borrow_id: int,
        fine_paid: int,
        fine_prev: int,
        returned_date: datetime,
    ) -> int:
        return await self.book_borrow_repository.update(
            conditions=BookBorrow(id=book_borrow_id, returned=False),
            obj=BookBorrow(
                fine_accumulated=fine_paid + fine_prev,
                returned_date=returned_date,
                returned=True,
                fine_status=FineStatus.PAID,
            ),
        )
