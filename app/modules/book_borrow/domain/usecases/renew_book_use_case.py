from datetime import datetime

from app.modules.book_borrows.domain.entities.book_borrow import BookBorrow
from app.modules.book_borrows.domain.repositories.book_borrow_repository_interface import (
    BookBorrowRepositoryInterface,
)


class RenewBookUseCase:
    def __init__(self, book_borrow_repository: BookBorrowRepositoryInterface) -> None:
        self.book_borrow_repository = book_borrow_repository

    async def execute(
        self,
        id: int,
        new_due_date: datetime,
        fine_collected: int,
        prev_renewed: int,
        prev_fine: int = 0,
    ) -> int:
        return await self.book_borrow_repository.update(
            conditions=BookBorrow(id=id),
            obj=BookBorrow(
                due_date=new_due_date,
                fine_accumulated=prev_fine + fine_collected,
                times_renewed=prev_renewed + 1,
            ),
        )
