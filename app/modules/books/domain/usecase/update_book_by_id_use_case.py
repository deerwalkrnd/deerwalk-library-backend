from app.modules.books.domain.entities.book import Book
from app.modules.books.domain.repository.book_repository_interface import (
    BookRepositoryInterface,
)


class UpdateBookByIdUseCase:
    def __init__(self, book_repository: BookRepositoryInterface) -> None:
        self.book_repository = book_repository

    async def execute(self, conditions: Book, new: Book) -> None:
        await self.book_repository.update(conditions=conditions, obj=new)
