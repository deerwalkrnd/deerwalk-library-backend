from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infra.repositories.repository import Repository
from app.core.models.book_review import BookReviewModel
from app.modules.books_reviews.domain.entities.book_review import BookReview
from app.modules.books_reviews.domain.repository.book_review_repository_interface import (
    BookReviewRepositoryInterface,
)


class BookReviewRepository(
    Repository[BookReviewModel, BookReview], BookReviewRepositoryInterface
):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db=db, model=BookReviewModel, entity=BookReview)

    async def count_book_reviews(self, book_id: int) -> int:
        query = (
            select(func.count())
            .select_from(BookReviewModel)
            .where(BookReviewModel.book_id == book_id)
        )
        result = await self.db.execute(query)
        return result.scalar_one()
