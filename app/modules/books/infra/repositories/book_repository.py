from sqlalchemy import and_, distinct, func, select
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

    async def get_total_books_count(self) -> int:
        query = (
            select(func.count(distinct(self.model.id)))
            .select_from(self.model)
            .where(and_(self.model.deleted == False))
        )

        result = await self.db.execute(query)
        count = result.scalar()
        if not count:
            count = 0
        return count
