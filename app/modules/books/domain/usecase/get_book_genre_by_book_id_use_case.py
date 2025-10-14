from typing import List

from app.modules.books.domain.repository.books_genre_repository_interface import (
    BooksGenreRepositoryInterface,
)
from app.modules.genres.domain.entities.genre import Genre


class GetBookGenreByBookIdUseCase:
    def __init__(self, book_genre_repository: BooksGenreRepositoryInterface) -> None:
        self.book_genre_repository = book_genre_repository

    async def execute(self, book_id: int) -> List[Genre]:
        return await self.book_genre_repository.get_genres_by_book_id(book_id=book_id)
