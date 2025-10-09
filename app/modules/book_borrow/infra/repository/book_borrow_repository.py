from sqlalchemy.ext.asyncio import AsyncSession
from app.core.infra.repositories.repository import Repository
from app.core.models.book_borrow import BookBorrowModel
from app.modules.book_borrow.domain.entities.book_borrow import BookBorrow
from app.modules.book_borrow.domain.repository.book_borrow_repository_interface import (
    BookBorrowRepositoryInterface,
)


class BookBorrowRepository(
    Repository[BookBorrowModel, BookBorrow], BookBorrowRepositoryInterface
):
    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        super().__init__(db, BookBorrowModel, BookBorrow)
