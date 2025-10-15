from typing import List

from app.modules.books_reviews.domain.entities.book_review import BookReview
from app.modules.books_reviews.domain.repository.book_review_repository_interface import (
    BookReviewRepositoryInterface,
)


class GetManyBookReviewsByIdUseCase:
    def __init__(self, book_review_repository: BookReviewRepositoryInterface) -> None:
        self.book_review_repository = book_review_repository

    async def execute(
        self,
        page: int,
        limit: int,
        sort_by: str,
        descending: bool,
        is_spam: bool,
        book_id: int,
    ) -> List[BookReview]:
        offset = (page - 1) * limit
        book_reviews = await self.book_review_repository.filter(
            offset=offset,
            limit=limit,
            descending=descending,
            sort_by=sort_by,
            filter=BookReview(book_id=book_id, is_spam=is_spam),
            start_date=None,
            end_date=None,
            searchable_value=None,
            searchable_key=None,
        )
        return book_reviews
