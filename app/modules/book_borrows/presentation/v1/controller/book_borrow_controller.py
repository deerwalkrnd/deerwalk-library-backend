from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.database import get_db
from app.core.dependencies.middleware.get_current_user import get_current_user
from app.core.domain.entities.response.paginated_response import PaginatedResponseMany
from app.core.domain.entities.user import User
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
from app.modules.book_borrows.domain.requests.borrowed_history_params import (
    BorrowedHistoryParams,
)
from app.modules.book_borrows.domain.requests.get_many_book_borrow_request import (
    GetManyBookBorrowRequest,
)
from app.modules.book_borrows.domain.responses.book_borrow_response_dto import (
    BookBorrowResponseDTO,
)
from app.modules.book_borrows.domain.usecases.get_borrowed_history_use_case import (
    GetBorrowedHistoryUseCase,
)
from app.modules.book_borrows.domain.utils.validate_get_borrows_request import (
    validate_get_borrows_request,
)
from app.modules.book_borrows.infra.repositories.book_borrow_repository import (
    BookBorrowRepository,
)
from app.modules.book_borrows.domain.usecases.borrow_book_use_case import (
    BorrowBookUseCase,
)
from app.modules.book_borrows.domain.usecases.get_book_borrow_by_id_usecase import (
    GetBookBorrowByIdUseCase,
)
from app.modules.book_borrows.domain.usecases.get_book_borrow_by_user_id_and_book_copy_id_use_case import (
    GetBookBorrowByUserIdAndBookCopyIdUseCase,
)
from app.modules.book_borrows.domain.usecases.get_currently_borrowed_books_use_case import (
    GetCurrentlyBorrowedBooksUseCase,
)
from app.modules.book_borrows.domain.usecases.get_many_borrow_books_with_user_and_book_use_case import (
    GetManyBorrowBooksWithUserAndBookUseCase,
)
from app.modules.book_borrows.domain.usecases.renew_book_use_case import (
    RenewBookUseCase,
)
from app.modules.book_borrows.domain.usecases.return_book_use_case import (
    ReturnBookUseCase,
)
from app.modules.book_copies.domain.usecases.update_book_copy_availability_use_case import (
    UpdateBookCopyAvailabilityUseCase,
)
from app.modules.books.infra.repositories.book_copy_repository import BookCopyRepository
from app.modules.book_borrows.domain.usecases.get_book_recommendations_use_case import (
    GetBookRecommendationsUseCase,
)
from app.modules.book_borrows.domain.requests.book_recommendation_params import (
    BookRecommendationParams,
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
        book_copy_repository = BookCopyRepository(db=db)

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
            update_book_copy_availability_use_case = UpdateBookCopyAvailabilityUseCase(
                book_copy_repository=book_copy_repository
            )

            await update_book_copy_availability_use_case.execute(
                book_copy_id=book_copy_id, is_available=False
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
        validate_get_borrows_request(request=params)

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
            times_renewed=book_borrow.times_renewed,
        )

    async def return_book(
        self,
        id: int,
        return_book_request: BookReturnRequest,
        db: AsyncSession = Depends(get_db),
    ) -> None:
        book_borrow_repository = BookBorrowRepository(db=db)
        book_copy_repository = BookCopyRepository(db=db)

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
            fine_rate=book_borrow.fine_rate,
            due_date=book_borrow.due_date,
            returned_date=return_book_request.returned_date,
            fine_prev=book_borrow.fine_accumulated
            if book_borrow.fine_accumulated
            else 0,
            remark=return_book_request.remark,
        )

        update_book_copy_availability_use_case = UpdateBookCopyAvailabilityUseCase(
            book_copy_repository=book_copy_repository
        )
        if not book_borrow.book_copy_id:
            raise ValueError("unreachable")

        await update_book_copy_availability_use_case.execute(
            book_copy_id=book_borrow.book_copy_id, is_available=True
        )

    async def get_currently_borrowed_books(
        self,
        db: AsyncSession = Depends(get_db),
        params: GetManyBookBorrowRequest = Depends(),
        user: User = Depends(get_current_user),
    ) -> PaginatedResponseMany[BookBorrowResponseDTO]:
        try:
            book_borrow_repository = BookBorrowRepository(db=db)

            get_currently_borrowed_books_use_case = GetCurrentlyBorrowedBooksUseCase(
                book_borrow_repository=book_borrow_repository
            )

            if not user:
                raise LibraryException(
                    status_code=404,
                    code=ErrorCode.NOT_FOUND,
                    msg="user with retrieved user id does not exist",
                )

            currently_reading_books = (
                await get_currently_borrowed_books_use_case.execute(
                    page=params.page,
                    end_date=params.ends,
                    limit=params.limit,
                    searchable_key=params.searchable_field,
                    searchable_value=params.searchable_value,
                    sort_by=params.sort_by,
                    start_date=params.starts,
                    user_id=user.uuid,
                )
            )

            return PaginatedResponseMany(
                page=params.page,
                total=len(currently_reading_books),
                next=params.page + 1,
                items=currently_reading_books,
            )

        except Exception as e:
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg=f"Something bad happened error: {e}",
            )

    async def borrowed_history(
        self,
        params: BorrowedHistoryParams = Depends(),
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
    ) -> PaginatedResponseMany[BookBorrow]:
        books_borrow_repository = BookBorrowRepository(db=db)

        get_borrowed_history_use_case = GetBorrowedHistoryUseCase(
            book_borrow_repository=books_borrow_repository
        )

        if not user.uuid:
            raise ValueError("unreachable")

        borrowed = await get_borrowed_history_use_case.execute(
            ends=params.ends,
            limit=params.limit,
            page=params.page,
            searchable_key=params.searchable_field,
            searchable_value=params.searchable_value,
            starts=params.starts,
            user_id=user.uuid,
        )

        return PaginatedResponseMany(
            items=borrowed,
            next=params.page + 1,
            page=params.page,
            total=len(borrowed),
        )

    async def get_book_recommendations(
        self,
        params: BookRecommendationParams = Depends(),
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
    ):
        if not user.uuid:
            raise ValueError("unreachable")

        try:
            book_borrow_repository = BookBorrowRepository(db=db)

            get__book_recommendations_use_case = GetBookRecommendationsUseCase(
                book_borrow_repository=book_borrow_repository
            )

            recommended_book = await get__book_recommendations_use_case.execute(
                limit=params.limit or 5, user_id=user.uuid
            )

            return recommended_book
        except Exception as e:
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg=f"Something bad happend error: {e}",
            )
