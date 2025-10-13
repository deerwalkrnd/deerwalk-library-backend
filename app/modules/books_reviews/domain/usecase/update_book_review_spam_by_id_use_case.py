from app.modules.books_reviews.domain.entities.book_review import BookReview
from app.modules.books_reviews.domain.repository.book_review_repository_interface import \
    BookReviewRepositoryInterface


class UpdateBookReviewSpamByIdUseCase:
    def __init__(self, book_review_repository: BookReviewRepositoryInterface) -> None:
        self.book_review_repository = book_review_repository

    async def execute(self, conditions: BookReview, new: BookReview) -> None:
        await self.book_review_repository.update(conditions=conditions, obj=new)
