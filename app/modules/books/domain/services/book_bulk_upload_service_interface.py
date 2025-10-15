from typing import List
from app.modules.books.domain.entities.book import Book
from app.modules.books.domain.repository.book_copy_repository_interface import (
    BookCopyRepositoryInterface,
)
from app.modules.books.domain.repository.book_repository_interface import (
    BookRepositoryInterface,
)
from app.modules.books.domain.repository.books_genre_repository_interface import (
    BooksGenreRepositoryInterface,
)
from app.modules.books.domain.repository.response.book_bulk_upload_response import (
    BookBulkUploadResponse,
)
from app.modules.books.domain.request.book_create_request import CreateBookRequest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.genres.domain.repository.genre_repository_interface import (
    GenreRepositoryInterface,
)


class BookBulkUploadServiceInterface:
    def __init__(
        self,
        book_repository: BookRepositoryInterface,
        books_genre_repository: BooksGenreRepositoryInterface,
        book_copy_repository: BookCopyRepositoryInterface,
        genre_repository: GenreRepositoryInterface,
        db: AsyncSession,
    ):
        raise NotImplementedError

    async def bulk_upload(
        self, create_book_requests: List[CreateBookRequest]
    ) -> BookBulkUploadResponse:
        raise NotImplementedError

    async def create_book(self, create_book_request: CreateBookRequest) -> Book | None:
        raise NotImplementedError
