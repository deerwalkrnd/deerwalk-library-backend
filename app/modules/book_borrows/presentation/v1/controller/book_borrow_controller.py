from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.database import get_db
from app.core.domain.entities.response.paginated_response import PaginatedResponseMany
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.core.models.book_borrow import FineStatus
from app.modules.book_borrows.domain.entities.book_borrow import BookBorrow
from app.modules.book_borrows.domain.requests.book_borrow_request import (
    BookBorrowRequest,
)
from app.modules.book_borrows.domain.requests.book_renew_request import BookRenewRequest
from app.modules.book_borrows.domain.requests.book_return_request import (
    BookReturnRequest,
)
from app.modules.book_borrows.domain.requests.get_many_book_borrow_request import (
    GetManyBookBorrowRequest,
)
from app.modules.book_borrows.domain.responses.book_borrow_response_dto import (
    BookBorrowResponseDTO,
)
from app.modules.book_borrows.infra.repositories.book_borrow_repository import (
    BookBorrowRepository,
)
from app.modules.book_borrows.infra.usecases.borrow_book_use_case import (
    BorrowBookUseCase,
)
from app.modules.book_borrows.infra.usecases.get_book_borrow_by_id_usecase import (
    GetBookBorrowByIdUseCase,
)
from app.modules.book_borrows.infra.usecases.get_book_borrow_by_user_id_and_book_copy_id_use_case import (
    GetBookBorrowByUserIdAndBookCopyIdUseCase,
)
from app.modules.book_borrows.infra.usecases.get_many_borrow_books_with_user_and_book_use_case import (
    GetManyBorrowBooksWithUserAndBookUseCase,
)
from app.modules.book_borrows.infra.usecases.renew_book_use_case import RenewBookUseCase
from app.modules.book_borrows.infra.usecases.return_book_use_case import (
    ReturnBookUseCase,
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

        book_borrow = await get_book_borrow_by_id_use_case.execute(
            book_borrow_id=id, returned=False
        )

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
        except ValueError:
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
    ) -> PaginatedResponseMany[BookBorrowResponseDTO]:
        book_borrow_repository = BookBorrowRepository(db=db)

        get_many_borrow_books_with_user_and_book_use_case = (
            GetManyBorrowBooksWithUserAndBookUseCase(
                book_borrow_repository=book_borrow_repository
            )
        )

        data = await get_many_borrow_books_with_user_and_book_use_case.execute(
            page=params.page,
            end_date=params.ends,
            limit=params.limit,
            searchable_key=params.searchable_field,
            searchable_value=params.searchable_value,
            sort_by=params.sort_by,
            start_date=params.starts,
            user_id=None,
        )

        return PaginatedResponseMany(
            page=params.page, total=len(data), next=params.page + 1, items=data
        )

    async def renew_book(
        self,
        id: int,
        book_renew_request: BookRenewRequest,
        db: AsyncSession = Depends(get_db),
    ) -> None:
        book_borrow_repository = BookBorrowRepository(db=db)

        get_book_borrow_by_id_use_case = GetBookBorrowByIdUseCase(
            book_borrow_repository=book_borrow_repository
        )

        book_borrow = await get_book_borrow_by_id_use_case.execute(
            book_borrow_id=id, returned=False
        )

        if not book_borrow or book_borrow.times_renewed == book_borrow.times_renewable:
            raise LibraryException(
                status_code=403,
                code=ErrorCode.INSUFFICIENT_PERMISSION,
                msg="You can now longer renew this book and it must be re-issued.",
            )

        renew_book_use_case = RenewBookUseCase(
            book_borrow_repository=book_borrow_repository
        )

        if book_borrow.times_renewed == None:
            raise ValueError("unreachable")

        await renew_book_use_case.execute(
            new_due_date=book_renew_request.new_due_date,
            fine_collected=book_renew_request.fine_collected,
            id=id,
            prev_fine=book_borrow.fine_accumulated
            if book_borrow.fine_accumulated
            else 0,
            prev_renewed=book_borrow.times_renewed + 1,
        )

    async def return_book(
        self,
        id: int,
        return_book_request: BookReturnRequest,
        db: AsyncSession = Depends(get_db),
    ) -> None:
        book_borrow_repository = BookBorrowRepository(db=db)
        get_book_borrow_by_id_use_case = GetBookBorrowByIdUseCase(
            book_borrow_repository=book_borrow_repository
        )
        book_borrow = await get_book_borrow_by_id_use_case.execute(
            book_borrow_id=id, returned=False
        )

        if not book_borrow:
            raise LibraryException(
                status_code=404,
                code=ErrorCode.NOT_FOUND,
                msg="this book has not been borrowed by this individual",
            )

        return_book_use_case = ReturnBookUseCase(
            book_borrow_repository=book_borrow_repository
        )

        await return_book_use_case.execute(
            book_borrow_id=id,
            fine_paid=return_book_request.fine_paid,
            returned_date=return_book_request.returned_date,
            fine_prev=book_borrow.fine_accumulated
            if book_borrow.fine_accumulated
            else 0,
            remark=return_book_request.remark,
        )
