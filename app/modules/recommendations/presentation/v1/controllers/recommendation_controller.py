from fastapi import Depends, logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.database import get_db
from app.core.domain.entities.response.paginated_response import PaginatedResponseMany
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.modules.recommendations.domain.entities.recommendation import Recommendation
from app.modules.recommendations.domain.request.recommendation_create_request import (
    CreateRecommendationRequest,
)
from app.modules.recommendations.domain.request.recommendation_list_params import (
    RecommendationListParams,
)
from app.modules.recommendations.domain.request.recommendation_update_request import (
    RecommendationUpdateRequest,
)
from app.modules.recommendations.domain.usecase.create_recommendation_use_case import (
    CreateRecommendationUseCase,
)
from app.modules.recommendations.domain.usecase.delete_recommendation_by_id_use_case import (
    DeleteRecommendationByIdUseCase,
)
from app.modules.recommendations.domain.usecase.get_many_recommendation_use_case import (
    GetManyRecommendationUseCase,
)
from app.modules.recommendations.domain.usecase.get_recommendation_by_id_use_case import (
    GetRecommendationByIdUseCase,
)
from app.modules.recommendations.domain.usecase.update_recommendation_by_id_use_case import (
    UpdateRecommendationByIdUseCase,
)
from app.modules.recommendations.infra.repositories.recommendation_repository import (
    RecommendationRepository,
)


class RecommendationController:
    def __init__(self) -> None:
        pass

    async def list_recommendations(
        self,
        params: RecommendationListParams = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginatedResponseMany[Recommendation] | None:
        recommendation_repository = RecommendationRepository(db=db)

        if (params.searchable_field and not params.searchable_value) or (
            params.searchable_value and not params.searchable_field
        ):
            raise LibraryException(
                code=ErrorCode.INVALID_FIELDS,
                status_code=400,
                msg="searchable params need both value and key",
            )

        try:
            get_many_recommendation_use_case = GetManyRecommendationUseCase(
                recommendation_repository=recommendation_repository
            )

            recommendations = await get_many_recommendation_use_case.execute(
                page=params.page,
                limit=params.limit,
                starts=params.starts,
                ends=params.ends,
                searchable_key=params.searchable_field,
                searchable_value=params.searchable_value,
            )


            return PaginatedResponseMany(
                page=params.page,
                total=len(recommendations),
                next=params.page + 1,
                items=recommendations,
            )

        except Exception as e:
            logger.logger.error(e)
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="could not fetch recommendations",
            )

    async def create_recommendation(
        self,
        create_recommendation_request: CreateRecommendationRequest,
        db: AsyncSession = Depends(get_db),
    ) -> Recommendation | None:
        recommendations_repository = RecommendationRepository(db=db)
        try:
            create_recommendation_use_case = CreateRecommendationUseCase(
                recommendation_repository=recommendations_repository
            )

            recommendation = await create_recommendation_use_case.execute(
                name=create_recommendation_request.name,
                designation=create_recommendation_request.designation,
                note=create_recommendation_request.note,
                book_title=create_recommendation_request.book_title,
                cover_image_url=create_recommendation_request.cover_image_url,
            )
            return recommendation

        except Exception as e:
            logger.logger.error(e)
            if isinstance(e, LibraryException):
                raise e
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="could not create recommendation",
            )

    async def update_recommendation(
        self,
        id: int,
        recommendation_update_request: RecommendationUpdateRequest,
        db: AsyncSession = Depends(get_db),
    ) -> None:
        recommendation_repository = RecommendationRepository(db=db)

        try:
            get_recommendation_by_id_use_case = GetRecommendationByIdUseCase(
                recommendation_repository=recommendation_repository
            )

            recommendation = await get_recommendation_by_id_use_case.execute(id=id)

            if not recommendation:
                raise LibraryException(
                    status_code=404,
                    code=ErrorCode.NOT_FOUND,
                    msg="recommendation not found",
                )

            update_recommendation_by_id_use_case = UpdateRecommendationByIdUseCase(
                recommendation_repository=recommendation_repository
            )

            await update_recommendation_by_id_use_case.execute(
                conditions=Recommendation(id=id),
                new=Recommendation(
                    **recommendation_update_request.model_dump(exclude_unset=True)
                ),
            )

            return None

        except Exception as e:
            logger.logger.error(e)
            if isinstance(e, LibraryException):
                raise e
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="could not update recommendation",
            )

    async def delete_recommendation(
        self, id: int, db: AsyncSession = Depends(get_db)
    ) -> None:
        recommendation_repository = RecommendationRepository(db=db)
        try:
            get_recommendation_by_id_use_case = GetRecommendationByIdUseCase(
                recommendation_repository=recommendation_repository
            )
            recommendation = await get_recommendation_by_id_use_case.execute(id=id)
            if not recommendation:
                raise LibraryException(
                    status_code=404,
                    code=ErrorCode.NOT_FOUND,
                    msg="recommendation you're deleting does not exist",
                )
            delete_recommendation_by_id_use_case = DeleteRecommendationByIdUseCase(
                recommendation_repository=recommendation_repository
            )

            return await delete_recommendation_by_id_use_case.execute(id=id)

        except Exception as e:
            logger.logger.error(e)
            if isinstance(e, LibraryException):
                raise e
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="could not delete recommendation",
            )
