from datetime import datetime
from typing import List
from app.modules.books.domain.entities.book_copy import BookCopy
from app.modules.books.domain.repositories.book_copy_repository_interface import (
    BookCopyRepositoryInterface,
)


class GetManyBookCopyByBookIdUseCase:
    def __init__(self, book_copy_repository: BookCopyRepositoryInterface):
        self.book_copy_repository = book_copy_repository

    async def execute(
        self,
        page: int,
        limit: int,
        searchable_field: str | None,
        searchable_value: str | None,
        starts: datetime | None,
        ends: datetime | None,
        book_id: int,
    ) -> List[BookCopy] | None:
        offset = (page - 1) * limit
        book_copies = await self.book_copy_repository.filter(
            offset=offset,
            limit=limit,
            descending=True,
            sort_by="created_at",
            end_date=ends,
            start_date=starts,
            searchable_key=searchable_field,
            searchable_value=searchable_value,
            filter=BookCopy(book_id=book_id, is_available=True),
        )
        return book_copies
