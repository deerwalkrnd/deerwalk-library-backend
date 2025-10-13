from app.modules.recommendations.domain.entities.recommendation import \
    Recommendation
from app.modules.recommendations.domain.repository.recommendation_repository_interface import \
    RecommendationRepositoryInterface


class CreateRecommendationUseCase:
    def __init__(
        self,
        recommendation_repository: RecommendationRepositoryInterface,
    ) -> None:
        self.recommendation_repository = recommendation_repository

    async def execute(
        self,
        name: str,
        designation: str,
        note: str,
        book_title: str,
        cover_image_url: str | None = None,
    ) -> Recommendation | None:
        already = await self.recommendation_repository.find_one(
            obj=Recommendation(
                name=name,
                designation=designation,
                note=note,
                book_title=book_title,
                cover_image_url=cover_image_url,
            )
        )
        if already:
            raise ValueError("recommendation already exists.")
        return await self.recommendation_repository.create(
            obj=Recommendation(
                name=name,
                designation=designation,
                note=note,
                book_title=book_title,
                cover_image_url=cover_image_url,
            )
        )
