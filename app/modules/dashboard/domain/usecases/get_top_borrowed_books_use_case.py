from typing import List
from app.modules.books.domain.entities.book import Book
from app.modules.books.domain.repositories.book_repository_interface import (
    BookRepositoryInterface,
)


class GetTopBorrowedBooksUseCase:
    def __init__(self, book_repository: BookRepositoryInterface) -> None:
        self.book_repository = book_repository

    async def execute(self, limit: int) -> List[Book]:
        return await self.book_repository.get_top_books_borrowed(limit=limit)
