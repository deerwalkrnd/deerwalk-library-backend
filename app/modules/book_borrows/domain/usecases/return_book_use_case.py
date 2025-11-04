from datetime import datetime
from typing import Optional

from app.core.models.book_borrow import FineStatus
from app.modules.book_borrows.domain.entities.book_borrow import BookBorrow
from app.modules.book_borrows.domain.repositories.book_borrow_repository_interface import (
    BookBorrowRepositoryInterface,
)
from app.core.dependencies.get_settings import get_settings

class ReturnBookUseCase:
    def __init__(self, book_borrow_repository: BookBorrowRepositoryInterface) -> None:
        self.book_borrow_repository = book_borrow_repository

    async def execute(
        self,
        book_borrow_id: int,
        fine_paid: bool,
        fine_prev: int,
        returned_date: datetime,
        remark: Optional[str],
        due_date: datetime,
    ) -> int:
        settings = get_settings()
        per_day_rate = settings.default_fine_amount

        overdue_days = max((returned_date - due_date).days, 0)
        fine_accumulated = fine_prev + (per_day_rate * overdue_days)

        return await self.book_borrow_repository.update(
            conditions=BookBorrow(id=book_borrow_id, returned=False),
            obj=BookBorrow(
                fine_accumulated=fine_accumulated,
                returned_date=returned_date,
                returned=True,
                fine_status=FineStatus.PAID
                if fine_paid else FineStatus.UNPAID,
                remark=remark,
            ),
        )
