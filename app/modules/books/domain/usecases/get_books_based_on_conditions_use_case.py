from app.modules.books.domain.entities.book import Book
from app.modules.books.domain.repositories.book_repository_interface import (
    BookRepositoryInterface,
)


class GetBooksBasedOnConditionsUseCase:
    def __init__(self, book_repository: BookRepositoryInterface) -> None:
        self.book_repository = book_repository

    async def execute(self, conditions: Book) -> Book | None:
        return await self.book_repository.find_one(obj=conditions)
