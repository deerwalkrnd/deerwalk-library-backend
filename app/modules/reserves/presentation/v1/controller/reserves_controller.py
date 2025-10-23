from typing import Any
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies.database import get_db
from app.core.dependencies.middleware.get_current_user import get_current_user
from app.core.domain.entities.user import User
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.core.models.reserve import BookReserveEnum
from app.modules.book_copies.domain.usecases.get_book_copy_by_id_use_case import (
    GetBookCopyByIdUseCase,
)
from app.modules.book_copies.domain.usecases.update_book_copy_availability_use_case import (
    UpdateBookCopyAvailabilityUseCase,
)
from app.modules.books.infra.repositories.book_copy_repository import BookCopyRepository
from app.modules.reserves.domain.entities.reserve import Reserve
from app.modules.reserves.domain.requests.reserve_book_request import ReserveBookRequest
from app.modules.reserves.domain.usecases.get_reserve_by_book_copy_id_and_user_id_use_case import (
    GetReserveByBookCopyIdandUserIdUseCase,
)
from app.modules.reserves.domain.usecases.get_reserve_by_id_use_case import (
    GetReserveByIdUseCase,
)
from app.modules.reserves.domain.usecases.remove_reserve_use_case import (
    RemoveReserveUseCase,
)
from app.modules.reserves.domain.usecases.reserve_book_use_case import (
    ReserveBookUseCase,
)
from app.modules.reserves.infra.repositories.reserves_repository import (
    ReservesRepository,
)


class ReservesController:
    def __init__(self) -> None:
        pass

    async def reserve_book(
        self,
        reserve_book_request: ReserveBookRequest,
        db: AsyncSession,
        user: User = Depends(get_current_user),
    ) -> Reserve | None:
        reserves_repository = ReservesRepository(db=db)
        book_copy_repository = BookCopyRepository(db=db)

        get_book_copy_by_id_use_case = GetBookCopyByIdUseCase(
            book_copy_repository=book_copy_repository
        )

        # the logic for checking already borrowed book-id isnt sound here. need to be fixed

        book_copy = await get_book_copy_by_id_use_case.execute(
            book_copy_id=reserve_book_request.book_copy_id,
        )

        if not book_copy:
            raise LibraryException(
                status_code=404,
                code=ErrorCode.NOT_FOUND,
                msg="book copy does not exist",
            )

        if not book_copy.is_available:
            raise LibraryException(
                status_code=409,
                code=ErrorCode.DUPLICATE_ENTRY,
                msg="book copy is not available",
            )

        get_reserve_by_book_copy_id_and_user_id_use_case = (
            GetReserveByBookCopyIdandUserIdUseCase(
                reserves_repository=reserves_repository
            )
        )

        if not user.uuid:
            raise ValueError("unreachable")

        already_reserved = (
            await get_reserve_by_book_copy_id_and_user_id_use_case.execute(
                user_id=user.uuid, book_copy_id=reserve_book_request.book_copy_id
            )
        )

        if already_reserved and already_reserved.state == BookReserveEnum.BORROWED:
            raise LibraryException(
                status_code=409,
                code=ErrorCode.DUPLICATE_ENTRY,
                msg="this specific book already reserved by this user",
            )

        reserve_book_use_case = ReserveBookUseCase(
            reserves_repository=reserves_repository
        )
        r = await reserve_book_use_case.execute(
            book_copy_id=reserve_book_request.book_copy_id,
            user_id=user.uuid,
        )

        update_book_copy_availability_use_case = UpdateBookCopyAvailabilityUseCase(
            book_copy_repository=book_copy_repository
        )

        await update_book_copy_availability_use_case.execute(
            book_copy_id=reserve_book_request.book_copy_id, is_available=False
        )

        return r

    async def remove_reserve(
        self,
        reserve_id: int,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
    ) -> None:
        reserves_repository = ReservesRepository(db=db)
        book_copy_repository = BookCopyRepository(db=db)

        get_reserve_by_id_use_case = GetReserveByIdUseCase(
            reserve_repository=reserves_repository
        )

        reserve = await get_reserve_by_id_use_case.execute(reserve_id=reserve_id)

        if not reserve:
            raise LibraryException(
                status_code=404, code=ErrorCode.NOT_FOUND, msg="reserve was not found"
            )

        if reserve.user_id != user.uuid:
            raise LibraryException(
                status_code=403,
                code=ErrorCode.INSUFFICIENT_PERMISSION,
                msg="you are not allowed to remove this reserve",
            )

        remove_reserve_use_case = RemoveReserveUseCase(
            reserve_repository=reserves_repository
        )

        update_book_copy_availability_use_case = UpdateBookCopyAvailabilityUseCase(
            book_copy_repository=book_copy_repository
        )

        if not reserve.book_copy_id:
            raise ValueError("unreachable")

        await update_book_copy_availability_use_case.execute(
            book_copy_id=reserve.book_copy_id, is_available=False
        )

        await remove_reserve_use_case.execute(reserve_id=reserve_id)

    async def is_book_reserved(self, book_id: int) -> Any:
        raise NotImplementedError

    async def get_borrow_requests(self, params: Any) -> Any:
        raise NotImplementedError
