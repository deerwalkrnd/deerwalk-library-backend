from fastapi import Depends, logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.database import get_db
from app.core.domain.entities.response.paginated_response import PaginatedResponseMany
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.modules.book_copies.domain.requests.book_copy_list_params import (
    BookCopyListParams,
)
from app.modules.books.domain.usecases.get_many_book_copy_by_book_id_use_case import (
    GetManyBookCopyByBookIdUseCase,
)
from app.modules.books.infra.repositories.book_copy_repository import BookCopyRepository


class BookCopyController:
    async def get_available_book_copies(
        self, params: BookCopyListParams = Depends(), db: AsyncSession = Depends(get_db)
    ):
        try:
            book_copy_repository = BookCopyRepository(db=db)

            get_many_book_copy_use_case = GetManyBookCopyByBookIdUseCase(
                book_copy_repository=book_copy_repository
            )

            book_copies = await get_many_book_copy_use_case.execute(
                page=params.page,
                limit=params.limit,
                searchable_field=params.searchable_field,
                searchable_value=params.searchable_value,
                ends=params.ends,
                starts=params.starts,
                book_id=params.book_id,
            )

            if book_copies:
                return PaginatedResponseMany(
                    page=params.page,
                    total=len(book_copies),
                    next=params.page + 1,
                    items=book_copies,
                )

        except Exception as e:
            logger.logger.error(e)
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="could not fetch book_copies",
            )
