from datetime import datetime
from typing import List

from app.modules.books.domain.entities.book import Book
from app.modules.books.domain.repositories.book_repository_interface import (
    BookRepositoryInterface,
)


class GetManyBookUseCase:
    def __init__(self, book_repository: BookRepositoryInterface) -> None:
        self.book_repository = book_repository

    async def execute(
        self,
        page: int,
        limit: int,
        searchable_value: str | None,
        searchable_field: str | None,
        starts: datetime | None,
        ends: datetime | None,
    ) -> List[Book]:
        offset = (page - 1) * limit
        books = await self.book_repository.filter(
            offset=offset,
            limit=limit,
            descending=True,
            sort_by="created_at",
            filter=None,
            start_date=starts,
            end_date=ends,
            searchable_value=searchable_value,
            searchable_key=searchable_field,
        )
        return books
