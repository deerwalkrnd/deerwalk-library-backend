from sqlalchemy.ext.asyncio import AsyncSession
from app.core.infra.repositories.repository import Repository
from app.core.models.book_copy import BookCopyModel
from app.modules.books.domain.entities.book_copy import BookCopy
from app.modules.books.domain.repository.book_copy_repository_interface import (
    BookCopyRepositoryInterface,
)


class BookCopyRepository(
    Repository[BookCopyModel, BookCopy], BookCopyRepositoryInterface
):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, BookCopyModel, BookCopy)
