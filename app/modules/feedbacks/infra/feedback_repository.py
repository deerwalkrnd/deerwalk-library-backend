from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infra.repositories.repository import Repository
from app.core.models.feedback import FeedbackModel
from app.modules.feedbacks.domain.entities.feedback import Feedback
from app.modules.feedbacks.domain.repository.feedback_repository_interface import \
    FeedbackRepositoryInterface


class FeedbackRepository(
    Repository[FeedbackModel, Feedback], FeedbackRepositoryInterface
):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db=db, model=FeedbackModel, entity=Feedback)
