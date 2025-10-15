from datetime import datetime

from app.core.models.book_borrow import FineStatus
from app.modules.book_borrows.domain.entities.book_borrow import BookBorrow
from app.modules.book_borrows.domain.repositories.book_borrow_repository_interface import (
    BookBorrowRepositoryInterface,
)


class BorrowBookUseCase:
    def __init__(self, book_borrow_repository: BookBorrowRepositoryInterface) -> None:
        self.book_borrow_repository = book_borrow_repository

    async def execute(
        self,
        user_id: str,
        book_copy_id: int,
        fine_accumulated: int,
        times_renewable: int,
        times_renewed: int,
        due_date: datetime,
        fine_status: FineStatus,
    ) -> BookBorrow | None:
        try:
            created = await self.book_borrow_repository.create(
                obj=BookBorrow(
                    book_copy_id=book_copy_id,
                    due_date=due_date,
                    fine_accumulated=fine_accumulated,
                    times_renewable=times_renewable,
                    times_renewed=times_renewed,
                    user_id=user_id,
                    fine_status=fine_status,
                )
            )
            return created
        except Exception as e:
            raise ValueError(str(e))
