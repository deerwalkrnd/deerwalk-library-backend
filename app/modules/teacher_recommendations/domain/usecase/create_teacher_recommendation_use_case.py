from app.modules.teacher_recommendations.domain.entities.teacher_recommendation import (
    TeacherRecommendation,
)
from app.modules.teacher_recommendations.domain.repository.teacher_recommendation_repository_interface import (
    TeacherRecommendationRepositoryInterface,
)


class CreateTeacherRecommendationUseCase:
    def __init__(
        self,
        teacher_recommendation_repository: TeacherRecommendationRepositoryInterface,
    ) -> None:
        self.teacher_recommendation_repository = teacher_recommendation_repository

    async def execute(
        self,
        name: str,
        designation: str,
        note: str,
        book_title: str,
        cover_image_url: str | None = None,
    ) -> TeacherRecommendation | None:
        already = await self.teacher_recommendation_repository.find_one(
            obj=TeacherRecommendation(
                name=name,
                designation=designation,
                note=note,
                book_title=book_title,
                cover_image_url=cover_image_url,
            )
        )
        if already:
            raise ValueError("teacher recommendation already exists.")
        return await self.teacher_recommendation_repository.create(
            obj=TeacherRecommendation(
                name=name,
                designation=designation,
                note=note,
                book_title=book_title,
                cover_image_url=cover_image_url,
            )
        )
