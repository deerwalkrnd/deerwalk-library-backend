from app.modules.book_borrows.domain.repositories.book_borrow_repository_interface import (
    BookBorrowRepositoryInterface,
)


class GetBookRecommendationsUseCase:
    def __init__(self, book_borrow_repository: BookBorrowRepositoryInterface):
        self.book_borrow_repository = book_borrow_repository

    async def execute(self, limit: int, user_id: str):
        return await self.book_borrow_repository.get_book_recommendations(
            limit=limit, user_id=user_id
        )
