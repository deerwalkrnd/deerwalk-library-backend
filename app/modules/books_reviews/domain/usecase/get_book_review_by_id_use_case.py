from app.modules.books_reviews.domain.entities.book_review import BookReview
from app.modules.books_reviews.domain.repository.book_review_repository_interface import \
    BookReviewRepositoryInterface


class GetBookReviewByIdUseCase:
    def __init__(self, book_review_repository: BookReviewRepositoryInterface):
        self.book_review_repository = book_review_repository

    async def execute(self, id: int):
        return await self.book_review_repository.find_one(obj=BookReview(id=id))
