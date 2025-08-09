from venv import logger
from fastapi import Depends
from app.core.dependencies.database import get_db
from app.core.dependencies.middleware.get_current_user import get_current_user
from app.core.domain.entities.response.paginated_response import PaginatedResponseMany
from app.core.domain.entities.user import User
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.modules.feedbacks.domain.entities.feedback import Feedback
from app.modules.feedbacks.domain.request.feedback_create_request import (
    FeedbackCreateRequest,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.feedbacks.domain.request.feedback_list_params import FeedbackListParams
from app.modules.feedbacks.domain.request.feedback_update_request import (
    FeedbackUpdateRequest,
)
from app.modules.feedbacks.domain.usecase.create_feedback_use_case import (
    CreateFeedbackUseCase,
)
from app.modules.feedbacks.domain.usecase.get_feedback_by_id_use_case import (
    GetFeedbackByIdUseCase,
)
from app.modules.feedbacks.domain.usecase.get_many_feedback_use_case import (
    GetManyFeedbackUseCase,
)
from app.modules.feedbacks.domain.usecase.update_feedback_by_id_use_case import (
    UpdateFeedbackByIdUseCase,
)
from app.modules.feedbacks.infra.feedback_repository import FeedbackRepository


class FeedbackController:
    def __init__(self) -> None:
        pass

    async def create_feedback(
        self,
        feedback_create_request: FeedbackCreateRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ) -> Feedback | None:
        feedback_repository = FeedbackRepository(db=db)

        if not user.uuid:
            raise LibraryException(
                code=ErrorCode.INSUFFICIENT_PERMISSION,
                status_code=403,
                msg="could not get your user id",
            )

        try:
            create_feedback_use_case = CreateFeedbackUseCase(
                feedback_repository=feedback_repository
            )

            new_feedback = await create_feedback_use_case.execute(
                subject=feedback_create_request.subject,
                feedback=feedback_create_request.feedback,
                user_id=user.uuid,
            )

            return new_feedback
        except ValueError as e:
            logger.error(e)
            raise LibraryException(
                status_code=409,
                code=ErrorCode.DUPLICATE_ENTRY,
                msg="feedback already exists",
            )

    async def list_feedbacks(
        self, params: FeedbackListParams = Depends(), db: AsyncSession = Depends(get_db)
    ) -> PaginatedResponseMany[Feedback]:
        feedback_repository = FeedbackRepository(db=db)

        try:
            get_many_feedback_use_case = GetManyFeedbackUseCase(
                feedback_repository=feedback_repository
            )

            feedbacks = await get_many_feedback_use_case.execute(
                page=params.page,
                limit=params.limit,
                searchable_field=params.searchable_field,
                searchable_value=params.searchable_value,
                starts=params.starts,
                ends=params.ends,
                is_ack=params.is_ack,
            )

            return PaginatedResponseMany(
                page=params.page,
                total=len(feedbacks),
                next=params.page + 1,
                items=feedbacks,
            )

        except Exception as e:
            logger.error(e)
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="could not fetch quotes",
            )

    async def update_feedbacks(
        self,
        id: int,
        feedback_update_request: FeedbackUpdateRequest,
        db: AsyncSession = Depends(get_db),
    ) -> None:
        feedback_repository = FeedbackRepository(db=db)
        get_feedback_by_id_use_case = GetFeedbackByIdUseCase(
            feedback_repository=feedback_repository
        )

        feedback = await get_feedback_by_id_use_case.execute(id=id)

        if not feedback:
            raise LibraryException(
                status_code=404,
                code=ErrorCode.NOT_FOUND,
                msg="quote you're deleting does not exist",
            )

        update_feedback_by_id_use_case = UpdateFeedbackByIdUseCase(
            feedback_repository=feedback_repository
        )

        await update_feedback_by_id_use_case.execute(
            conditions=Feedback(id=id),
            new=Feedback(**feedback_update_request.model_dump(exclude_unset=True)),
        )

        return None
