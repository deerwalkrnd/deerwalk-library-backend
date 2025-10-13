from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.dependencies.database import get_db
from app.core.domain.entities.response.paginated_response import PaginatedResponseMany
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.core.models.book_borrow import FineStatus
from app.modules.book_borrow.domain.entities.book_borrow import BookBorrow
from app.modules.book_borrow.domain.request.book_borrow_request import BookBorrowRequest
from app.modules.book_borrow.domain.request.get_many_book_borrow_request import (
    GetManyBookBorrowRequest,
)
from app.modules.book_borrow.infra.repository.book_borrow_repository import (
    BookBorrowRepository,
)
from app.modules.book_borrow.infra.usecases.borrow_book_use_case import (
    BorrowBookUseCase,
)
from app.modules.book_borrow.infra.usecases.get_book_borrow_by_id_usecase import (
    GetBookBorrowByIdUseCase,
)
from app.modules.book_borrow.infra.usecases.get_book_borrow_by_user_id_and_book_copy_id_use_case import (
    GetBookBorrowByUserIdAndBookCopyIdUseCase,
)


class BookBorrowController:
    def __init__(self) -> None:
        pass

    # TODO(aashutosh): test this
    async def get_one_borrow(
        self, id: int, db: AsyncSession = Depends(get_db)
    ) -> BookBorrow:
        book_borrow_repository = BookBorrowRepository(db=db)

        get_book_borrow_by_id_use_case = GetBookBorrowByIdUseCase(
            book_borrow_repository=book_borrow_repository
        )

        book_borrow = await get_book_borrow_by_id_use_case.execute(book_borrow_id=id)

        if not book_borrow:
            raise LibraryException(
                status_code=404,
                code=ErrorCode.NOT_FOUND,
                msg="Borrow record with such id does not exist",
            )

        return book_borrow

    # TODO(aashutosh): test this and also unique constraint
    async def borrow_book(
        self,
        book_copy_id: int,
        book_borrow_request: BookBorrowRequest,
        db: AsyncSession = Depends(get_db),
    ) -> BookBorrow | None:
        book_borrow_repository = BookBorrowRepository(db=db)

        get_book_borrow_by_user_id_and_book_copy_id_use_case = (
            GetBookBorrowByUserIdAndBookCopyIdUseCase(
                book_borrow_repository=book_borrow_repository
            )
        )

        already = await get_book_borrow_by_user_id_and_book_copy_id_use_case.execute(
            book_copy_id=book_copy_id,
            user_id=book_borrow_request.user_uuid,
        )

        if already:
            raise LibraryException(
                status_code=409,
                code=ErrorCode.DUPLICATE_ENTRY,
                msg="this book is already borrowed by this individual",
            )

        fine_status = FineStatus.DISABLED

        if book_borrow_request.fine_enabled:
            fine_status = FineStatus.UNPAID

        try:
            borrow_book_use_case = BorrowBookUseCase(
                book_borrow_repository=book_borrow_repository
            )

            borrow = await borrow_book_use_case.execute(
                book_copy_id=book_copy_id,
                due_date=book_borrow_request.due_date,
                fine_accumulated=0,
                times_renewable=book_borrow_request.times_renewable,
                times_renewed=0,
                user_id=book_borrow_request.user_uuid,
                fine_status=fine_status,
            )
            return borrow
        except ValueError as e:
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="Something Bad Happened",
            )

    # TODO(aashutosh): Join users table and book table with a new DTO for response
    async def get_many_borrow_books(
        self,
        db: AsyncSession = Depends(get_db),
        params: GetManyBookBorrowRequest = Depends(),
    ) -> PaginatedResponseMany[BookBorrow]:
        book_borrow_repository = BookBorrowRepository(db=db)

        raise NotImplementedError

    async def renew_book(self, book_renew_request: Any) -> None:
        raise NotImplementedError

    async def return_book(self, return_book_request: Any) -> None:
        raise NotImplementedError
