from typing import List
from datetime import datetime
from app.modules.recommendations.domain.entities.recommendation import Recommendation
from app.modules.recommendations.domain.repositories.recommendation_repository_interface import (
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
        starts: datetime | None,
        ends: datetime | None,
        searchable_key: str | None,
        searchable_value: str | None,
    ) -> List[Recommendation]:
        offset = (page - 1) * limit
        recommendations = await self.recommendation_repository.filter(
            offset=offset,
            limit=limit,
            descending=True,
            sort_by="created_at",
            filter=None,
            start_date=starts,
            end_date=ends,
            searchable_value=searchable_value,
            searchable_key=searchable_key,
        )
        return recommendations
