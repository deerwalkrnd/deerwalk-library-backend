from app.modules.feedbacks.domain.entities.feedback import Feedback
from app.modules.feedbacks.domain.repositories.feedback_repository_interface import (
    FeedbackRepositoryInterface,
)


class GetFeedbackByIdUseCase:
    def __init__(self, feedback_repository: FeedbackRepositoryInterface):
        self.feedback_repository = feedback_repository

    async def execute(self, id: int) -> Feedback | None:
        return await self.feedback_repository.find_one(obj=Feedback(id=id))
