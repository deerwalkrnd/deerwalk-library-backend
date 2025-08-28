from fastapi import Depends, logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies.database import get_db
from app.core.domain.entities.response.paginated_response import PaginatedResponseMany
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.modules.teacher_recommendations.domain.entities.teacher_recommendation import (
    TeacherRecommendation,
)
from app.modules.teacher_recommendations.domain.request.teacher_recommendation_create_request import (
    CreateTeacherRecommendationRequest,
)
from app.modules.teacher_recommendations.domain.request.teacher_recommendation_list_params import (
    TeacherRecommendationListParams,
)
from app.modules.teacher_recommendations.domain.request.teacher_recommendation_update_request import (
    TeacherRecommendationUpdateRequest,
)
from app.modules.teacher_recommendations.domain.usecase.create_teacher_recommendation_use_case import (
    CreateTeacherRecommendationUseCase,
)
from app.modules.teacher_recommendations.domain.usecase.get_teacher_recommendation_by_id_use_case import (
    GetTeacherRecommendationByIdUseCase,
)
from app.modules.teacher_recommendations.domain.usecase.update_teacher_recommendation_by_id_use_case import (
    UpdateTeacherRecommendationByIdUseCase,
)
from app.modules.teacher_recommendations.infra.teacher_recommendations_repository import (
    TeacherRecommendationRepository,
)
from app.modules.teacher_recommendations.domain.usecase.get_many_teacher_recommendation_use_case import (
    GetManyTeacherRecommendationUseCase,
)

from app.modules.teacher_recommendations.domain.usecase.delete_teacher_recommendation_by_id_use_case import (
    DeleteTeacherRecommendationByIdUseCase,
)


class TeacherRecommendationController:
    def __init__(self) -> None:
        pass

    async def list_teacher_recommendations(
        self,
        params: TeacherRecommendationListParams = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginatedResponseMany[TeacherRecommendation] | None:
        teacher_recommendation_repository = TeacherRecommendationRepository(db=db)

        try:
            get_many_teacher_recommendation_use_case = (
                GetManyTeacherRecommendationUseCase(
                    teacher_recommendation_repository=teacher_recommendation_repository
                )
            )

            teacher_recommendations = (
                await get_many_teacher_recommendation_use_case.execute(
                    page=params.page,
                    limit=params.limit,
                )
            )
            return PaginatedResponseMany(
                page=params.page,
                total=len(teacher_recommendations),
                next=params.page + 1,
                items=teacher_recommendations,
            )

        except Exception as e:
            logger.logger.error(e)
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="could not fetch teacher recommendations",
            )

    async def create_teacher_recommendation(
        self,
        create_teacher_recommendation_request: CreateTeacherRecommendationRequest,
        db: AsyncSession = Depends(get_db),
    ) -> TeacherRecommendation | None:
        teacher_recommendations_repository = TeacherRecommendationRepository(db=db)
        try:
            create_teacher_recommendation_use_case = CreateTeacherRecommendationUseCase(
                teacher_recommendation_repository=teacher_recommendations_repository
            )

            teacher_recommendation = await create_teacher_recommendation_use_case.execute(
                name=create_teacher_recommendation_request.name,
                designation=create_teacher_recommendation_request.designation,
                note=create_teacher_recommendation_request.note,
                book_title=create_teacher_recommendation_request.book_title,
                cover_image_url=create_teacher_recommendation_request.cover_image_url,
            )
            return teacher_recommendation

        except Exception as e:
            logger.logger.error(e)
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="could not create teacher recommendation",
            )

    async def update_teacher_recommendation(
        self,
        id: int,
        teacher_recommendation_update_request: TeacherRecommendationUpdateRequest,
        db: AsyncSession = Depends(get_db),
    ) -> None:
        teacher_recommendation_repository = TeacherRecommendationRepository(db=db)

        try:
            get_teacher_recommendation_by_id_use_case = (
                GetTeacherRecommendationByIdUseCase(
                    teacher_recommendation_repository=teacher_recommendation_repository
                )
            )

            teacher_recommendation = (
                await get_teacher_recommendation_by_id_use_case.execute(id=id)
            )

            if not teacher_recommendation:
                raise LibraryException(
                    status_code=404,
                    code=ErrorCode.NOT_FOUND,
                    msg="teacher recommendation not found",
                )

            update_teacher_recommendation_by_id_use_case = (
                UpdateTeacherRecommendationByIdUseCase(
                    teacher_repository=teacher_recommendation_repository
                )
            )

            await update_teacher_recommendation_by_id_use_case.execute(
                conditions=TeacherRecommendation(id=id),
                new=TeacherRecommendation(
                    **teacher_recommendation_update_request.model_dump(
                        exclude_unset=True
                    )
                ),
            )

            return None

        except Exception as e:
            logger.logger.error(e)
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="could not update teacher recommendation",
            )

    async def delete_teacher_recommendation(
        self, id: int, db: AsyncSession = Depends(get_db)
    ) -> None:
        teacher_recommendation_repository = TeacherRecommendationRepository(db=db)
        try:
            get_teacher_recommendation_by_id_use_case = (
                GetTeacherRecommendationByIdUseCase(
                    teacher_recommendation_repository=teacher_recommendation_repository
                )
            )
            teacher_recommendation = (
                await get_teacher_recommendation_by_id_use_case.execute(id=id)
            )
            if not teacher_recommendation:
                raise LibraryException(
                    status_code=404,
                    code=ErrorCode.NOT_FOUND,
                    msg="teacher recommendation you're deleting does not exist",
                )
            delete_teacher_recommendation_by_id_use_case = (
                DeleteTeacherRecommendationByIdUseCase(
                    teacher_recommendation_repository=teacher_recommendation_repository
                )
            )

            return await delete_teacher_recommendation_by_id_use_case.execute(id=id)

        except Exception as e:
            logger.logger.error(e)
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="could not delete teacher recommendation",
            )
