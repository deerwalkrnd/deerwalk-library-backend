from app.modules.feedbacks.domain.entities.feedback import Feedback
from app.modules.feedbacks.domain.repository.feedback_repository_interface import \
    FeedbackRepositoryInterface


class CreateFeedbackUseCase:
    def __init__(self, feedback_repository: FeedbackRepositoryInterface) -> None:
        self.feedback_repository = feedback_repository

    async def execute(
        self, subject: str, feedback: str, user_id: str
    ) -> Feedback | None:
        already = await self.feedback_repository.find_one(
            obj=Feedback(subject=subject, feedback=feedback, user_id=user_id)
        )

        if already:
            raise ValueError("feedback already exists")

        return await self.feedback_repository.create(
            obj=Feedback(user_id=user_id, subject=subject, feedback=feedback)
        )
