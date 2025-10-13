from app.modules.books.domain.entities.book import Book
from app.modules.books.domain.repository.book_repository_interface import \
    BookRepositoryInterface


class GetBookByIdUseCase:
    def __init__(self, book_repository: BookRepositoryInterface) -> None:
        self.book_repository = book_repository

    async def execute(self, id: int) -> Book | None:
        return await self.book_repository.find_one(obj=Book(id=id))
