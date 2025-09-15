from app.modules.books.domain.entities.book import Book
from app.modules.books.domain.repository.book_repository_interface import (
    BookRepositoryInterface,
)
from typing import List
from datetime import datetime


class GetManyBookUseCase:
    def __init__(self, book_repository: BookRepositoryInterface) -> None:
        self.book_repository = book_repository

    async def execute(
        self,
        page: int,
        limit: int,
        sort_by: str,
        is_descending: bool,
        searchable_field: str | None,
        searchable_value: str | None,
        start_date: datetime | None,
        end_date: datetime | None,
    ) -> List[Book]:
        offset = (page - 1) * limit
        books = await self.book_repository.filter(
            offset=offset,
            limit=limit,
            descending=is_descending,
            sort_by=sort_by,
            filter=None,
            start_date=start_date,
            end_date=end_date,
            searchable_value=searchable_value,
            searchable_key=searchable_field,
        )
        return books
