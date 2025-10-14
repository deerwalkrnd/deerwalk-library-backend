from abc import abstractmethod

from app.core.domain.repositories.repository_interface import RepositoryInterface
from app.modules.books_reviews.domain.entities.book_review import BookReview


class BookReviewRepositoryInterface(RepositoryInterface[BookReview]):
    @abstractmethod
    async def count_book_reviews(self, book_id: int) -> int:
        raise NotImplementedError
