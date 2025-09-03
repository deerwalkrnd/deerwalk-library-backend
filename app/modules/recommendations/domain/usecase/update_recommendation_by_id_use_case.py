from app.modules.recommendations.domain.entities.recommendation import (
    Recommendation,
)
from app.modules.recommendations.domain.repository.recommendation_repository_interface import (
    RecommendationRepositoryInterface,
)


class UpdateRecommendationByIdUseCase:
    def __init__(self, recommendation_repository: RecommendationRepositoryInterface) -> None:
        self.recommendation_repository = recommendation_repository

    async def execute(self, conditions: Recommendation, new: Recommendation) -> None:
        await self.recommendation_repository.update(conditions=conditions, obj=new)
