from typing import List
from app.modules.books_reviews.domain.entities.book_review import BookReview
from app.modules.books_reviews.domain.repository.book_review_repository_interface import (
    BookReviewRepositoryInterface,
)


class GetManyBookReviewsByIdUseCase:
    def __init__(self, book_review_repository: BookReviewRepositoryInterface) -> None:
        self.book_review_repository = book_review_repository

    async def execute(self, book_id: int) -> List[BookReview]:
        book_reviews = await self.book_review_repository.filter(
            offset=0,
            limit=100,
            descending=True,
            sort_by="created_at",
            filter=BookReview(book_id=book_id),
            start_date=None,
            end_date=None,
            searchable_value=None,
            searchable_key=None,
        )
        return book_reviews
