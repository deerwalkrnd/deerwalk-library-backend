from app.modules.recommendations.domain.entities.recommendation import Recommendation
from app.modules.recommendations.domain.repository.recommendation_repository_interface import (
    RecommendationRepositoryInterface,
)


class GetRecommendationByIdUseCase:
    def __init__(
        self,
        recommendation_repository: RecommendationRepositoryInterface,
    ) -> None:
        self.recommendation_repository = recommendation_repository

    async def execute(self, id: int) -> Recommendation | None:
        return await self.recommendation_repository.find_one(obj=Recommendation(id=id))
