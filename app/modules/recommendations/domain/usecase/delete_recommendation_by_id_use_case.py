from app.modules.recommendations.domain.entities.recommendation import \
    Recommendation
from app.modules.recommendations.domain.repository.recommendation_repository_interface import \
    RecommendationRepositoryInterface


class DeleteRecommendationByIdUseCase:
    def __init__(
        self,
        recommendation_repository: RecommendationRepositoryInterface,
    ) -> None:
        self.recommendation_repository = recommendation_repository

    async def execute(self, id: int) -> None:
        await self.recommendation_repository.hard_delete(
            conditions=Recommendation(id=id)
        )
