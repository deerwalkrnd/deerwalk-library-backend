from app.modules.books.domain.entities.book import Book
from app.modules.books.domain.repository.book_repository_interface import \
    BookRepositoryInterface


class DeleteBookByIdUseCase:
    def __init__(self, book_repository: BookRepositoryInterface) -> None:
        self.book_repository = book_repository

    async def execute(self, id: int) -> None:
        await self.book_repository.delete(conditions=Book(id=id))
