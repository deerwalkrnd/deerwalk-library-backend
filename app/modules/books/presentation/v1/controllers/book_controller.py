from typing import List, Literal

from fastapi import Depends, File, Query, Response, UploadFile, logger
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import run_in_threadpool

from app.core.dependencies.database import get_db
from app.core.dependencies.middleware.get_current_librarian import get_current_librarian
from app.core.domain.entities.user import User
from app.core.domain.entities.response.paginated_response import PaginatedResponseMany
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.modules.books.domain.entities.book import Book
from app.modules.books.domain.requests.book_create_request import CreateBookRequest
from app.modules.books.domain.requests.book_request_list_params import BookListParams
from app.modules.books.domain.requests.book_update_request import BookUpdateRequest
from app.modules.books.domain.responses.book_bulk_upload_response import (
    BookBulkUploadRespose,
)
from app.modules.books.domain.usecases.associate_book_with_genre_use_case import (
    AssociateBookWithGenreUseCase,
)
from app.modules.books.domain.usecases.create_book_copy_use_case import (
    CreateBookCopyUseCase,
)
from app.modules.books.domain.usecases.create_book_use_case import CreateBookUseCase
from app.modules.books.domain.usecases.delete_book_by_id_use_case import (
    DeleteBookByIdUseCase,
)
from app.modules.books.domain.usecases.get_book_by_id_use_case import GetBookByIdUseCase
from app.modules.books.domain.usecases.get_book_genre_by_book_id_use_case import (
    GetBookGenreByBookIdUseCase,
)
from app.modules.books.domain.usecases.get_books_based_on_conditions_use_case import (
    GetBooksBasedOnConditionsUseCase,
)
from app.modules.books.domain.usecases.get_many_book_use_case import GetManyBookUseCase
from app.modules.books.domain.usecases.update_book_by_id_use_case import (
    UpdateBookByIdUseCase,
)
from app.modules.books.infra.repositories.book_copy_repository import BookCopyRepository
from app.modules.books.infra.repositories.book_repository import BookRepository
from app.modules.books.infra.repositories.books_genre_repository import (
    BooksGenreRepository,
)
from app.modules.books.utils.book_import.parse_book_import_file import (
    parse_book_import_file,
)
from app.modules.books.utils.book_import.template_builder import (
    build_csv_template,
    build_xlsx_template,
)
from app.modules.genres.domain.entities.genre import Genre
from app.modules.books.infra.services.book_bulk_upload_service import (
    BookBulkUploadService,
)

from app.modules.genres.infra.genre_repository import GenreRepository


MAX_IMPORT_FILE_BYTES = 20 * 1024 * 1024


class BookController:
    def __init__(self) -> None:
        pass

    async def list_books(
        self,
        params: BookListParams = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginatedResponseMany[Book] | None:
        book_repository = BookRepository(db=db)

        try:
            get_many_book_use_case = GetManyBookUseCase(book_repository=book_repository)

            books = await get_many_book_use_case.execute(
                page=params.page,
                limit=params.limit,
                searchable_value=params.searchable_value,
                searchable_field=params.searchable_field,
                starts=params.starts,
                ends=params.ends,
            )

            total = await get_many_book_use_case.count(
                searchable_value=params.searchable_value,
                searchable_field=params.searchable_field,
                starts=params.starts,
                ends=params.ends,
            )

            return PaginatedResponseMany.build(
                page=params.page, limit=params.limit, total=total, items=books
            )

        except Exception as e:
            logger.logger.error(e)
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="could not list Books",
            )

    async def create_book(
        self, create_book_request: CreateBookRequest, db: AsyncSession = Depends(get_db)
    ) -> Book | None:
        book_repository = BookRepository(db=db)

        # non academic books have genre, academic books have grade

        if not create_book_request.genres or len(create_book_request.genres) < 1:
            raise LibraryException(
                status_code=400,
                code=ErrorCode.INVALID_FIELDS,
                msg="All Book Creation Requests must have atleast one genre",
            )

        get_books_based_on_conditions_use_case = GetBooksBasedOnConditionsUseCase(
            book_repository=book_repository
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
                msg="book with same publication and isbn already exists",
            )

        create_book_use_case = CreateBookUseCase(book_repository=book_repository)

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
                msg="failed to create book",
            )

        if not created_book.id:
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="could not insert book into the db",
            )

        book_copy_repository = BookCopyRepository(db=db)

        if create_book_request.copies and len(create_book_request.copies) >= 1:
            for book_copy in create_book_request.copies:
                create_book_copy_use_case = CreateBookCopyUseCase(
                    book_copy_repository=book_copy_repository
                )

                if not book_copy.unique_identifier:
                    raise LibraryException(
                        status_code=400,
                        code=ErrorCode.INVALID_FIELDS,
                        msg="all book copies need a unique_identifier",
                    )

                await create_book_copy_use_case.execute(
                    book_id=created_book.id,
                    unique_identifier=book_copy.unique_identifier,
                    condition=book_copy.condition,
                )

        books_genre_repository = BooksGenreRepository(db=db)

        for genre_id in create_book_request.genres:
            associate_book_with_genre_use_case = AssociateBookWithGenreUseCase(
                books_genre_repository=books_genre_repository
            )
            await associate_book_with_genre_use_case.execute(
                genre_id=genre_id, book_id=created_book.id
            )

        return created_book

    async def update_book(
        self,
        id: int,
        book_update_request: BookUpdateRequest,
        db: AsyncSession = Depends(get_db),
    ) -> Book | None:
        book_repository = BookRepository(db=db)
        try:
            get_book_by_id_use_case = GetBookByIdUseCase(
                book_repository=book_repository
            )
            book = await get_book_by_id_use_case.execute(id=id)
            if not book:
                raise LibraryException(
                    status_code=404,
                    code=ErrorCode.NOT_FOUND,
                    msg="Book not found",
                )

            update_book_by_id_use_case = UpdateBookByIdUseCase(
                book_repository=book_repository
            )

            await update_book_by_id_use_case.execute(
                conditions=Book(id=id),
                new=Book(
                    **book_update_request.model_dump(exclude_unset=True),
                ),
            )

            return None

        except Exception as e:
            logger.logger.error(e)
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="could not update Book",
            )

    async def delete_book(self, id: int, db: AsyncSession = Depends(get_db)) -> None:
        book_repository = BookRepository(db=db)
        try:
            get_book_by_id_use_case = GetBookByIdUseCase(
                book_repository=book_repository
            )
            book = await get_book_by_id_use_case.execute(id=id)
            if not book:
                raise LibraryException(
                    status_code=404,
                    code=ErrorCode.NOT_FOUND,
                    msg="Book not found",
                )

            delete_book_by_id_use_case = DeleteBookByIdUseCase(
                book_repository=book_repository
            )
            return await delete_book_by_id_use_case.execute(id=id)

        except Exception as e:
            logger.logger.error(e)
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="could not delete Book",
            )

    async def get_genres_by_book_id(
        self, id: int, db: AsyncSession = Depends(get_db)
    ) -> List[Genre]:
        books_genre_repository = BooksGenreRepository(db=db)

        get_book_genre_use_case = GetBookGenreByBookIdUseCase(
            book_genre_repository=books_genre_repository
        )

        genres = await get_book_genre_use_case.execute(book_id=id)

        return genres

    async def get_book_by_book_id(self, id: int, db: AsyncSession = Depends(get_db)):
        try:
            book_repository = BookRepository(db=db)
            get_book_by_id_use_case = GetBookByIdUseCase(
                book_repository=book_repository
            )

            book = await get_book_by_id_use_case.execute(id=id)

            return book
        except Exception as e:
            logger.logger.error(e)
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="server could not retrieve book by id.",
            )

    async def bulk_upload_books(
        self,
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db),
        _: User = Depends(get_current_librarian),
    ) -> BookBulkUploadRespose:
        content = await file.read(MAX_IMPORT_FILE_BYTES + 1)
        if len(content) > MAX_IMPORT_FILE_BYTES:
            raise LibraryException(
                status_code=413,
                code=ErrorCode.INVALID_FIELDS,
                msg=f"File is too large (limit {MAX_IMPORT_FILE_BYTES // (1024 * 1024)} MB).",
            )

        # Parsing a full register takes a few seconds of CPU; keep it off
        # the event loop so other requests are not stalled meanwhile.
        parsed = await run_in_threadpool(
            parse_book_import_file, file.filename or "", content
        )

        book_bulk_upload_service = BookBulkUploadService(
            book_repository=BookRepository(db=db),
            books_genre_repository=BooksGenreRepository(db=db),
            book_copy_repository=BookCopyRepository(db=db),
            genre_repository=GenreRepository(db=db),
            db=db,
        )
        result = await book_bulk_upload_service.bulk_upload(
            create_book_requests=parsed.books
        )

        return BookBulkUploadRespose(
            format=parsed.format,
            inserted=result.books_created,
            books_updated=result.books_updated,
            copies_added=result.copies_added,
            duplicates_ignored=parsed.duplicates_ignored + result.duplicates_ignored,
            skipped=parsed.skipped + result.skipped,
        )

    async def download_import_template(
        self,
        format: Literal["xlsx", "csv"] = Query(default="xlsx"),
        db: AsyncSession = Depends(get_db),
        _: User = Depends(get_current_librarian),
    ) -> Response:
        if format == "csv":
            return Response(
                content=build_csv_template(),
                media_type="text/csv; charset=utf-8",
                headers={
                    "Content-Disposition": 'attachment; filename="book_import_template.csv"'
                },
            )

        genres = await GenreRepository(db=db).find_many(
            limit=10_000, offset=0, sort_by="title", descending=False
        )
        return Response(
            content=build_xlsx_template(g.title for g in genres if g.title),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": 'attachment; filename="book_import_template.xlsx"'
            },
        )
