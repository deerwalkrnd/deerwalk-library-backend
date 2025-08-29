from app.modules.teacher_recommendations.domain.entities.teacher_recommendation import (
    TeacherRecommendation,
)
from app.modules.teacher_recommendations.domain.repository.teacher_recommendation_repository_interface import (
    TeacherRecommendationRepositoryInterface,
)


class DeleteTeacherRecommendationByIdUseCase:
    def __init__(
        self,
        teacher_recommendation_repository: TeacherRecommendationRepositoryInterface,
    ) -> None:
        self.teacher_recommendation_repository = teacher_recommendation_repository

    async def execute(self, id: int) -> None:
        await self.teacher_recommendation_repository.hard_delete(
            conditions=TeacherRecommendation(id=id)
        )
