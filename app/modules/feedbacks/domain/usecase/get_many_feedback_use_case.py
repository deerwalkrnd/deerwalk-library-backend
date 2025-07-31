from typing import List
from datetime import datetime

from app.modules.feedbacks.domain.entities.feedback import Feedback
from app.modules.feedbacks.domain.repository.feedback_repository_interface import (
    FeedbackRepositoryInterface,
)


class GetManyFeedbackUseCase:
    def __init__(self, feedback_repository: FeedbackRepositoryInterface) -> None:
        self.feedback_repository = feedback_repository

    async def execute(
        self,
        page: int,
        limit: int,
        searchable_field: str | None,
        searchable_value: str | None,
        starts: datetime | None,
        ends: datetime | None,
        is_ack: bool,
    ) -> List[Feedback]:
        offset = (page - 1) * limit
        feedbacks = await self.feedback_repository.filter(
            offset=offset,
            limit=limit,
            descending=True,
            sort_by="created_at",
            end_date=ends,
            start_date=starts,
            searchable_key=searchable_field,
            searchable_value=searchable_value,
            filter=Feedback(is_acknowledged=is_ack),
        )
        return feedbacks
