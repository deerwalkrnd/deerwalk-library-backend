from app.modules.feedbacks.domain.entities.feedback import Feedback
from app.modules.feedbacks.domain.repository.feedback_repository_interface import \
    FeedbackRepositoryInterface


class UpdateFeedbackByIdUseCase:
    def __init__(self, feedback_repository: FeedbackRepositoryInterface):
        self.feedback_repository = feedback_repository

    async def execute(self, conditions: Feedback, new: Feedback) -> None:
        await self.feedback_repository.update(conditions=conditions, obj=new)
