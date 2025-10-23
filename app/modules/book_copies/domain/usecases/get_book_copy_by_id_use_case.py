from app.modules.books.domain.entities.book_copy import BookCopy
from app.modules.books.domain.repositories.book_copy_repository_interface import (
    BookCopyRepositoryInterface,
)


class GetBookCopyByIdUseCase:
    def __init__(self, book_copy_repository: BookCopyRepositoryInterface) -> None:
        self.book_copy_repository = book_copy_repository

    async def execute(self, book_copy_id: int) -> BookCopy | None:
        return await self.book_copy_repository.find_one(obj=BookCopy(id=book_copy_id))
