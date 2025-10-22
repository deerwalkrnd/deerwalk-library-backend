from fastapi import Depends, logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.database import get_db
from app.core.dependencies.middleware.get_current_user import get_current_user
from app.core.domain.entities.response.paginated_response import PaginatedResponseMany
from app.core.domain.entities.user import User
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.modules.bookmarks.domain.entities.bookmark import Bookmark
from app.modules.bookmarks.domain.requests.bookamark_list_params import (
    BookmarkListParams,
)
from app.modules.bookmarks.domain.requests.bookmark_check_request import (
    BookmarkCheckRequest,
)
from app.modules.bookmarks.domain.requests.bookmark_create_request import (
    BookmarkCreateRequest,
)
from app.modules.bookmarks.domain.usecases.add_bookmark_use_case import (
    AddBookmarkUseCase,
)
from app.modules.bookmarks.domain.usecases.check_bookmark_by_book_id_use_case import (
    CheckBookmarkByBookIdUseCase,
)
from app.modules.bookmarks.domain.usecases.get_bookmark_by_user_id_use_case import (
    GetBookmarkByUserIdUseCase,
)
from app.modules.bookmarks.domain.usecases.remove_bookmark_by_id_use_case import (
    RemoveBookmarkByIdUseCase,
)
from app.modules.bookmarks.infra.repositories.bookmark_repository import (
    BookmarkRepository,
)


class BookmarkController:
    def __init__(self) -> None:
        pass

    async def add_bookmark(
        self,
        bookmark_create_request: BookmarkCreateRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):
        if not user.uuid:
            raise LibraryException(
                code=ErrorCode.NOT_FOUND,
                status_code=404,
                msg="cannot find user id",
            )

        try:
            bookmark_repository = BookmarkRepository(db=db)
            add_bookmark_use_case = AddBookmarkUseCase(
                bookmark_repository=bookmark_repository
            )

            bookmark = await add_bookmark_use_case.execute(
                user_id=user.uuid, book_id=bookmark_create_request.book_id
            )

            return bookmark
        except ValueError as e:
            logger.logger.error(e)
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="bookmark could not be added.",
            )

    async def remove_bookmark(
        self,
        id: int,
        db: AsyncSession = Depends(get_db),
    ):
        try:
            bookmark_repository = BookmarkRepository(db=db)
            remove_bookmark_use_case = RemoveBookmarkByIdUseCase(
                bookmark_repository=bookmark_repository
            )

            await remove_bookmark_use_case.execute(id=id)

        except ValueError as e:
            logger.logger.error(e)
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="bookmark could not be removed.",
            )

    async def get_bookmark(
        self,
        params: BookmarkListParams = Depends(),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ) -> PaginatedResponseMany[Bookmark]:
        try:
            bookmark_repository = BookmarkRepository(db=db)
            get_bookmark_by_user_id_use_case = GetBookmarkByUserIdUseCase(
                bookmark_repository=bookmark_repository
            )
            bookmarks = await get_bookmark_by_user_id_use_case.execute(
                page=params.page,
                limit=params.limit,
                searchable_field=params.searchable_field,
                searchable_value=params.searchable_value,
                starts=params.starts,
                ends=params.ends,
                user_id=user.uuid,
            )

            return PaginatedResponseMany(
                page=params.page,
                total=len(bookmarks),
                next=params.page + 1,
                items=bookmarks,
            )
        except Exception as e:
            logger.logger.error(e)
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="could not fetch bookmarks",
            )

    async def check_bookmark(
        self,
        bookmark_check_request: BookmarkCheckRequest,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
    ):
        try:
            bookmark_repository = BookmarkRepository(db=db)

            check_bookmark_by_book_id_use_case = CheckBookmarkByBookIdUseCase(
                bookmark_repository=bookmark_repository
            )

            if user.uuid:
                status = await check_bookmark_by_book_id_use_case.execute(
                    book_id=bookmark_check_request.book_id, user_id=user.uuid
                )
            else:
                raise LibraryException(
                    status_code=500,
                    code=ErrorCode.UNKOWN_ERROR,
                    msg="unable to fetch current user",
                )

            return status
        except Exception as e:
            logger.logger.error(e)
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="failed to check status of current book",
            )
