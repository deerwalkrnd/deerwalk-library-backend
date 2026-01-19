from typing import List
from app.modules.books.domain.entities.book import Book
from app.modules.books.domain.repositories.book_copy_repository_interface import (
    BookCopyRepositoryInterface,
)
from app.modules.books.domain.repositories.book_repository_interface import (
    BookRepositoryInterface,
)
from app.modules.books.domain.repositories.books_genre_repository_interface import (
    BooksGenreRepositoryInterface,
)
from app.modules.books.domain.requests.bulk_book_create_request import (
    BulkCreateBookRequest,
)
from app.modules.books.domain.responses.book_bulk_upload_response import (
    BookBulkUploadRespose,
)
from app.modules.genres.domain.repositories.genre_repository_interface import (
    GenreRepositoryInterface,
)
from sqlalchemy.ext.asyncio import AsyncSession


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
        self, create_book_requests: List[BulkCreateBookRequest]
    ) -> BookBulkUploadRespose:
        raise NotImplementedError

    async def create_book(
        self, create_book_request: BulkCreateBookRequest
    ) -> Book | None:
        raise NotImplementedError
