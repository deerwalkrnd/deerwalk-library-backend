from typing import List

from app.modules.recommendations.domain.entities.recommendation import Recommendation
from app.modules.recommendations.domain.repository.recommendation_repository_interface import (
    RecommendationRepositoryInterface,
)


class GetManyRecommendationUseCase:
    def __init__(
        self,
        recommendation_repository: RecommendationRepositoryInterface,
    ) -> None:
        self.recommendation_repository = recommendation_repository

    async def execute(
        self,
        page: int,
        limit: int,
    ) -> List[Recommendation]:
        offset = (page - 1) * limit
        recommendations = await self.recommendation_repository.filter(
            offset=offset,
            limit=limit,
            descending=True,
            sort_by="created_at",
            filter=None,
            start_date=None,
            end_date=None,
            searchable_value=None,
            searchable_key=None,
        )
        return recommendations
