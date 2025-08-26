from fastapi import Depends, logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies.database import get_db
from app.core.domain.entities.response.paginated_response import PaginatedResponseMany
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.modules.teacher_recommendations.domain.entities.teacher_recommendation import TeacherRecommendation
from app.modules.teacher_recommendations.domain.request.teacher_recommendation_list_params import TeacherRecommendationListParams
from app.modules.teacher_recommendations.infra.teacher_recommendations_repository import TeacherRecommendationRepository
from app.modules.teacher_recommendations.domain.usecase.get_many_teacher_recommendation_use_case import (GetManyTeacherRecommendationUseCase)


class TeacherRecommendationController:
    def __init__(self) -> None:
        pass

    async def list_teacher_recommendations(self, params: TeacherRecommendationListParams = Depends(),db:AsyncSession=Depends(get_db)) -> PaginatedResponseMany[TeacherRecommendation] | None:
        teacher_recommendation_repository = TeacherRecommendationRepository(db=db)

        try:
            get_many_teacher_recommendation_use_case  =GetManyTeacherRecommendationUseCase(teacher_recommendation_repository= teacher_recommendation_repository)

            teacher_recommendations = await get_many_teacher_recommendation_use_case.execute(
                page=params.page,
                limit=params.limit,
                searchable_value=params.searchable_value,
                searchable_field=params.searchable_field,
                starts=params.starts,
                ends=params.ends,
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
        

    async def create_teacher_recommendation(self):
        pass

    async def update_teacher_recommendation(self):
        pass

    async def delete_teacher_recommendation(self):
        pass
    