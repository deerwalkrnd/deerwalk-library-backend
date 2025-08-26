from datetime import datetime
from typing import List

from app.modules.teacher_recommendations.domain.entities.teacher_recommendation import TeacherRecommendation
from app.modules.teacher_recommendations.domain.repository.teacher_recommendation_repository_interface import (
    TeacherRecommendationRepositoryInterface,
)
class GetManyTeacherRecommendationUseCase:
    def __init__(self, teacher_recommendation_repository:TeacherRecommendationRepositoryInterface) -> None:
        self.teacher_recommendation_repository = teacher_recommendation_repository

    async def execute(
        self,
        page:int,
        limit:int,
        searchable_field:str | None,
        searchable_value:str | None,
        starts:datetime | None,
        ends:datetime | None,
    ) -> List[TeacherRecommendation]:
        offset=(page - 1) * limit
        teacher_recommendations = await self.teacher_recommendation_repository.filter(
            offset=offset,
            limit=limit,
            descending=True,
            sort_by="created_at",
            end_date=ends,
            start_date=starts,
            searchable_key=searchable_field,
            searchable_value=searchable_value,
            filter=None,
        )
        return teacher_recommendations