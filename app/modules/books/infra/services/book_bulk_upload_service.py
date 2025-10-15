from sqlite3 import IntegrityError
from typing import List

from fastapi import logger
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
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

from app.modules.books.domain.request.book_create_request import CreateBookRequest
from app.modules.books.domain.response.book_bulk_upload_response import BookBulkUploadRespose
from app.modules.books.domain.response.book_bulk_upload_skip_response import BookBulkUploadSkipResponse
from app.modules.books.domain.services.book_bulk_upload_service_interface import (
    BookBulkUploadServiceInterface,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.books.domain.usecase.associate_book_with_genre_use_case import (
    AssociateBookWithGenreUseCase,
)
from app.modules.books.domain.usecase.create_book_copy_use_case import (
    CreateBookCopyUseCase,
)
from app.modules.books.domain.usecase.create_book_use_case import CreateBookUseCase
from app.modules.books.domain.usecase.get_books_based_on_conditions_use_case import (
    GetBooksBasedOnConditionsUseCase,
)
from app.modules.genres.domain.repository.genre_repository_interface import (
    GenreRepositoryInterface,
)
from app.modules.genres.domain.usecase.get_genre_by_id_use_case import (
    GetGenreByIdUseCase,
)


class BookBulkUploadService(BookBulkUploadServiceInterface):
    def __init__(
        self,
        book_repository: BookRepositoryInterface,
        books_genre_repository: BooksGenreRepositoryInterface,
        book_copy_repository: BookCopyRepositoryInterface,
        genre_repository: GenreRepositoryInterface,
        db: AsyncSession,
    ):
        self.book_repository = book_repository
        self.books_genre_repository = books_genre_repository
        self.book_copy_repository = book_copy_repository
        self.genre_repository = genre_repository
        self.db = db

    async def bulk_upload(
        self, create_book_requests: List[CreateBookRequest]
    ) -> BookBulkUploadRespose:
        inserted = 0
        skipped: List[BookBulkUploadSkipResponse] = []

        for req in create_book_requests:
            try:
                created_book = await self.create_book(req)
                await self.db.commit()
                if created_book:
                    inserted += 1
                else:
                    skipped.append(
                        BookBulkUploadSkipResponse(
                            book_title=req.title, reason="Book creation returned None"
                        )
                    )

            except LibraryException as e:
                await self.db.rollback()
                logger.logger.error(f"Skipping book '{req.title}' due to error: {e}")
                skipped.append(
                    BookBulkUploadSkipResponse(
                        book_title=req.title, reason=f"error: {e}"
                    )
                )
            except IntegrityError as e:
                await self.db.rollback()
                logger.logger.error(
                    f"Skipping book '{req.title}' due to integrity error: {e}"
                )
                skipped.append(
                    BookBulkUploadSkipResponse(
                        book_title=req.title,
                        reason=f"Database integrity constraint violation: {e}",
                    )
                )
            except Exception as e:
                await self.db.rollback()
                logger.logger.error(
                    f"Skipping book '{req.title}' due to unexpected error: {e}"
                )
                skipped.append(
                    BookBulkUploadSkipResponse(
                        book_title=req.title, reason=f"Unexpected error: {e}"
                    )
                )

        return BookBulkUploadRespose(inserted=inserted, skipped=skipped)

    async def create_book(self, create_book_request: CreateBookRequest) -> Book | None:
        if not create_book_request.genres or len(create_book_request.genres) < 1:
            raise LibraryException(
                status_code=400,
                code=ErrorCode.INVALID_FIELDS,
                msg="All Book Creation Requests must have atleast one genre",
            )

        get_genre_by_id_use_case = GetGenreByIdUseCase(
            genre_repository=self.genre_repository
        )

        for genre_id in create_book_request.genres:
            genre = await get_genre_by_id_use_case.execute(id=genre_id)
            if not genre:
                raise LibraryException(
                    status_code=404,
                    code=ErrorCode.NOT_FOUND,
                    msg=f"Genre with id {genre_id} does not exist",
                )

        get_books_based_on_conditions_use_case = GetBooksBasedOnConditionsUseCase(
            book_repository=self.book_repository
        )

        book = await get_books_based_on_conditions_use_case.execute(
            conditions=Book(
                isbn=create_book_request.isbn,
                publication=create_book_request.publication,
            )
        )

        if book:
            raise LibraryException(
                status_code=409,
                code=ErrorCode.DUPLICATE_ENTRY,
                msg=f"Book with ISBN '{create_book_request.isbn}' and publication '{create_book_request.publication}' already exists",
            )

        create_book_use_case = CreateBookUseCase(book_repository=self.book_repository)

        created_book: Book | None = await create_book_use_case.execute(
            publication=create_book_request.publication,
            author=create_book_request.author,
            category=create_book_request.category,
            cover_image_url=create_book_request.cover_image_url,
            grade=create_book_request.grade,
            isbn=create_book_request.isbn,
            title=create_book_request.title,
        )

        if not created_book:
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="Failed to create book",
            )

        if not created_book.id:
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="Could not insert book into the database",
            )

        if create_book_request.copies and len(create_book_request.copies) >= 1:
            for book_copy in create_book_request.copies:
                create_book_copy_use_case = CreateBookCopyUseCase(
                    book_copy_repository=self.book_copy_repository
                )

                if not book_copy.unique_identifier:
                    raise LibraryException(
                        status_code=400,
                        code=ErrorCode.INVALID_FIELDS,
                        msg="All book copies need a unique_identifier",
                    )

                await create_book_copy_use_case.execute(
                    book_id=created_book.id,
                    unique_identifier=book_copy.unique_identifier,
                    condition=book_copy.condition,
                )

        for genre_id in create_book_request.genres:
            associate_book_with_genre_use_case = AssociateBookWithGenreUseCase(
                books_genre_repository=self.books_genre_repository
            )
            await associate_book_with_genre_use_case.execute(
                genre_id=genre_id, book_id=created_book.id
            )

        return created_book