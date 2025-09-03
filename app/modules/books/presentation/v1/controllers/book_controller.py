from fastapi import Depends, logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies.database import get_db
from app.core.domain.entities.response.paginated_response import PaginatedResponseMany
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.modules.books.domain.entities.book import Book
from app.modules.books.domain.request.book_create_request import CreateBookRequest
from app.modules.books.domain.request.book_request_list_params import BookListParams
from app.modules.books.domain.request.book_update_request import BookUpdateRequest
from app.modules.books.domain.usecase.delete_book_by_id_use_case import (
    DeleteBookByIdUseCase,
)
from app.modules.books.domain.usecase.get_book_by_id_use_case import GetBookByIdUseCase
from app.modules.books.domain.usecase.update_book_by_id_use_case import (
    UpdateBookByIdUseCase,
)
from app.modules.books.infra.book_repository import BookRepository
from app.modules.books.domain.usecase.get_many_book_use_case import GetManyBookUseCase


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
            )

            return PaginatedResponseMany(
                page=params.page, total=len(books), next=params.page + 1, items=books
            )

        except Exception as e:
            logger.logger.error(e)
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="could not create Book",
            )

    async def create_book(
        self, create_book_request: CreateBookRequest, db: AsyncSession = Depends(get_db)
    ) -> Book | None:
        # book_repository = BookRepository(db=db)
        try:
            pass

        except Exception as e:
            logger.logger.error(e)
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="could not create Book",
            )

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
