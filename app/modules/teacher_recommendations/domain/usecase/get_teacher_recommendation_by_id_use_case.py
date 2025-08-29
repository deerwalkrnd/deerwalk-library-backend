from app.modules.teacher_recommendations.domain.repository.teacher_recommendation_repository_interface import (
    TeacherRecommendationRepositoryInterface,
)

from app.modules.teacher_recommendations.domain.entities.teacher_recommendation import (
    TeacherRecommendation,
)


class GetTeacherRecommendationByIdUseCase:
    def __init__(
        self,
        teacher_recommendation_repository: TeacherRecommendationRepositoryInterface,
    ) -> None:
        self.teacher_recommendation_repository = teacher_recommendation_repository

    async def execute(self, id: int) -> TeacherRecommendation | None:
        return await self.teacher_recommendation_repository.find_one(
            obj=TeacherRecommendation(id=id)
        )
