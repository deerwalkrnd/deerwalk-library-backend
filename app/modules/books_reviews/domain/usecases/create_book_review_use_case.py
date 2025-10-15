from app.modules.books_reviews.domain.entities.book_review import BookReview
from app.modules.books_reviews.domain.repositories.book_review_repository_interface import (
    BookReviewRepositoryInterface,
)


class CreateBookReviewUseCase:
    def __init__(self, book_review_repository: BookReviewRepositoryInterface) -> None:
        self.book_review_repository = book_review_repository

    async def execute(
        self, book_id: int, user_id: str, review_text: str, is_spam: bool
    ) -> BookReview | None:
        already = await self.book_review_repository.find_one(
            obj=BookReview(
                book_id=book_id,
                user_id=user_id,
                review_text=review_text,
                is_spam=is_spam,
            )
        )
        if already:
            raise ValueError("book review already exists")
        return await self.book_review_repository.create(
            obj=BookReview(
                book_id=book_id,
                user_id=user_id,
                review_text=review_text,
                is_spam=is_spam,
            )
        )
