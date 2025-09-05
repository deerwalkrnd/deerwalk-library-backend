from typing import Optional
from app.modules.books.domain.entities.book_copy import BookCopy
from app.modules.books.domain.repository.book_copy_repository_interface import (
    BookCopyRepositoryInterface,
)


class CreateBookCopyUseCase:
    def __init__(self, book_copy_repository: BookCopyRepositoryInterface) -> None:
        self.book_copy_repository = book_copy_repository

    async def execute(
        self, book_id: int, unique_identifier: str, condition: Optional[str]
    ) -> BookCopy | None:
        book_copy = await self.book_copy_repository.create(
            obj=BookCopy(
                book_id=book_id,
                unique_identifier=unique_identifier,
                condition=condition,
            )
        )
        return book_copy
