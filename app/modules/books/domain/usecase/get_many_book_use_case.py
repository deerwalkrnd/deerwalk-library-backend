from app.modules.books.domain.entities.book import Book
from app.modules.books.domain.repository.book_repository_interface import (
    BookRepositoryInterface,
)
from typing import List


class GetManyBookUseCase:
    def __init__(self, book_repository: BookRepositoryInterface) -> None:
        self.book_repository = book_repository

    async def execute(
        self,
        page: int,
        limit: int,
    ) -> List[Book]:
        offset = (page - 1) * limit
        books = await self.book_repository.filter(
            offset=offset,
            limit=limit,
            descending=True,
            sort_by="created_at",
            filter=None,
            start_date=None,
            end_date=None,
            searchable_value=None,
            searchable_key=None,
        )
        return books
