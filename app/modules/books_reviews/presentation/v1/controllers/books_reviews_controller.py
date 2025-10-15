from fastapi import Depends, logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.database import get_db
from app.core.dependencies.middleware.get_current_user import get_current_user
from app.core.domain.entities.response.paginated_response import PaginatedResponseMany
from app.core.domain.entities.user import User, UserRole
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.modules.books_reviews.domain.entities.book_review import BookReview
from app.modules.books_reviews.domain.request.book_review_create_request import (
    BookReviewCreateRequest,
)
from app.modules.books_reviews.domain.request.book_review_list_params import (
    BookReviewListParams,
)
from app.modules.books_reviews.domain.request.book_review_spam_request import (
    BookReviewSpamRequest,
)
from app.modules.books_reviews.domain.usecase.create_book_review_use_case import (
    CreateBookReviewUseCase,
)
from app.modules.books_reviews.domain.usecase.get_many_book_reviews_by_id_use_case import (
    GetManyBookReviewsByIdUseCase,
)
from app.modules.books_reviews.domain.usecase.update_book_review_spam_by_id_use_case import (
    UpdateBookReviewSpamByIdUseCase,
)
from app.modules.books_reviews.infra.book_review_repository import BookReviewRepository


class BooksReviewsController:
    def __init__(self):
        pass

    async def create_book_review(
        self,
        book_review_request: BookReviewCreateRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ) -> BookReview | None:
        # create book review
        book_review_repository = BookReviewRepository(db=db)

        if not user.uuid:
            raise LibraryException(
                code=ErrorCode.INSUFFICIENT_PERMISSION,
                status_code=403,
                msg="could not get your user id",
            )

        try:
            create_book_review_use_case = CreateBookReviewUseCase(
                book_review_repository=book_review_repository
            )

            new_book_review = await create_book_review_use_case.execute(
                book_id=book_review_request.book_id,
                user_id=user.uuid,
                review_text=book_review_request.review_text,
                is_spam=book_review_request.is_spam,
            )
            return new_book_review

        except Exception as e:
            logger.logger.error(e)
            raise LibraryException(
                code=ErrorCode.DUPLICATE_ENTRY,
                status_code=500,
                msg=str(e),
            )

    async def get_book_reviews_by_book_id(
        self,
        params: BookReviewListParams = Depends(),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ) -> PaginatedResponseMany[BookReview] | None:
        book_review_repository = BookReviewRepository(db=db)

        if user.role and user.role.value == "STUDENT":
            params.is_spam = False

        try:
            get_many_book_reviews_by_id_use_case = GetManyBookReviewsByIdUseCase(
                book_review_repository
            )
            book_reviews = await get_many_book_reviews_by_id_use_case.execute(
                page=params.page,
                limit=params.limit,
                descending=params.is_descending,
                sort_by=params.sort_by,
                is_spam=params.is_spam,
                book_id=params.book_id,
            )
            return PaginatedResponseMany(
                page=params.page,
                total=len(book_reviews),
                next=params.page + 1,
                items=book_reviews,
            )

        except Exception as e:
            logger.logger.error(e)
            raise LibraryException(
                code=ErrorCode.UNKOWN_ERROR,
                status_code=500,
                msg=str(e),
            )

    async def mark_spam(
        self,
        id: int,
        book_review_spam_request: BookReviewSpamRequest,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
    ) -> BookReview | None:
        if user.role != UserRole.LIBRARIAN:
            raise LibraryException(
                code=ErrorCode.INSUFFICIENT_PERMISSION,
                status_code=403,
                msg="only librarian can mark review as spam",
            )

        book_review_repository = BookReviewRepository(db=db)

        try:
            update_book_review_spam_by_id_use_case = UpdateBookReviewSpamByIdUseCase(
                book_review_repository=book_review_repository
            )
            await update_book_review_spam_by_id_use_case.execute(
                conditions=BookReview(book_id=id),
                new=BookReview(is_spam=book_review_spam_request.is_spam),
            )
            return None

        except Exception as e:
            logger.logger.error(e)
            raise LibraryException(
                code=ErrorCode.UNKOWN_ERROR,
                status_code=500,
                msg=str(e),
            )

    async def count_book_reviews(
        self, book_id: int, db: AsyncSession = Depends(get_db)
    ) -> int | None:
        book_review_repository = BookReviewRepository(db=db)
        try:
            count = await book_review_repository.count_book_reviews(book_id=book_id)
            return count
        except Exception as e:
            logger.logger.error(e)
            raise LibraryException(
                code=ErrorCode.UNKOWN_ERROR,
                status_code=500,
                msg=str(e),
            )
