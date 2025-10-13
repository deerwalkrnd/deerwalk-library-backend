from app.core.domain.repositories.repository_interface import \
    RepositoryInterface
from app.modules.recommendations.domain.entities.recommendation import \
    Recommendation


class RecommendationRepositoryInterface(RepositoryInterface[Recommendation]):
    pass
