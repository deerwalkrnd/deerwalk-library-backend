from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infra.repositories.repository import Repository
from app.core.models.teacher_recommendation import TeacherRecommendationModel
from app.modules.teacher_recommendations.domain.entities.teacher_recommendation import TeacherRecommendation
from app.modules.teacher_recommendations.domain.repository.teacher_recommendation_repository_interface import (TeacherRecommendationRepositoryInterface)

class TeacherRecommendationRepository(Repository[TeacherRecommendationModel,TeacherRecommendation],TeacherRecommendationRepositoryInterface):
    def __init__(self, db:AsyncSession):
        super().__init__(db=db, model=TeacherRecommendationModel, entity=TeacherRecommendation)