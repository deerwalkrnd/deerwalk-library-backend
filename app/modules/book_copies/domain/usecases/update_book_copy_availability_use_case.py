from app.modules.books.domain.entities.book_copy import BookCopy
from app.modules.books.domain.repositories.book_copy_repository_interface import (
    BookCopyRepositoryInterface,
)


class UpdateBookCopyAvailabilityUseCase:
    def __init__(self, book_copy_repository: BookCopyRepositoryInterface) -> None:
        self.book_copy_repository = book_copy_repository

    async def execute(self, book_copy_id: int, is_available: bool) -> int:
        return await self.book_copy_repository.update(
            conditions=BookCopy(id=book_copy_id),
            obj=BookCopy(is_available=is_available),
        )
