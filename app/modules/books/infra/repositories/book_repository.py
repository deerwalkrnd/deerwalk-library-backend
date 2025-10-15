from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infra.repositories.repository import Repository
from app.core.models.book import BookModel
from app.modules.books.domain.entities.book import Book
from app.modules.books.domain.repositories.book_repository_interface import (
    BookRepositoryInterface,
)


class BookRepository(Repository[BookModel, Book], BookRepositoryInterface):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db=db, model=BookModel, entity=Book)
