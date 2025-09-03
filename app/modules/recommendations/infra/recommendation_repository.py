from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infra.repositories.repository import Repository
from app.core.models.recommendation import RecommendationModel
from app.modules.recommendations.domain.entities.recommendation import (
    Recommendation,
)
from app.modules.recommendations.domain.repository.recommendation_repository_interface import (
    RecommendationRepositoryInterface,
)


class RecommendationRepository(
    Repository[RecommendationModel, Recommendation],
    RecommendationRepositoryInterface,
):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, model=RecommendationModel, entity=Recommendation)
