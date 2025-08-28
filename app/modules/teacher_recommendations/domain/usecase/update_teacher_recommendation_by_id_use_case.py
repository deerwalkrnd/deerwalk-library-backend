from app.modules.teacher_recommendations.domain.entities.teacher_recommendation import (
    TeacherRecommendation,
)
from app.modules.teacher_recommendations.domain.repository.teacher_recommendation_repository_interface import (
    TeacherRecommendationRepositoryInterface,
)


class UpdateTeacherRecommendationByIdUseCase:
    def __init__(
        self, teacher_repository: TeacherRecommendationRepositoryInterface
    ) -> None:
        self.teacher_repository = teacher_repository

    async def execute(
        self, conditions: TeacherRecommendation, new: TeacherRecommendation
    ) -> None:
        await self.teacher_repository.update(conditions=conditions, obj=new)
