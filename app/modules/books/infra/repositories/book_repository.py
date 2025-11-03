from typing import List
from sqlalchemy import and_, distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infra.repositories.repository import Repository
from app.core.models.book import BookModel
from app.core.models.book_borrow import BookBorrowModel
from app.core.models.book_copy import BookCopyModel
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

    async def get_top_books_borrowed(self, limit: int) -> List[Book]:
        query = (
            select(self.model)
            .join(BookCopyModel, BookCopyModel.book_id == BookModel.id)
            .join(BookBorrowModel, BookBorrowModel.book_copy_id == BookCopyModel.id)
            .where(BookModel.deleted == False)
            .group_by(BookModel.id)
            .order_by(func.count(BookBorrowModel.id).desc())
            .limit(limit)
        )

        result = await self.db.execute(query)

        top_books = result.scalars().unique().all()

        return [self.entity.model_validate(book) for book in top_books]
