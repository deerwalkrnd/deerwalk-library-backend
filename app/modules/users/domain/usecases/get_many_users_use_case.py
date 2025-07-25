from typing import List
from datetime import datetime
from app.core.domain.entities.user import User
from app.core.infra.repositories.user_repository import UserRepository


class GetManyUsersUseCase:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def execute(
        self,
        page: int,
        limit: int,
        searchable_field: str | None,
        searchable_value: str | None,
        starts: datetime | None,
        ends: datetime | None,
    ) -> List[User]:
        offset = (page - 1) * limit

        items = await self.user_repository.filter(
            limit=limit,
            offset=offset,
            descending=True,
            sort_by="created_at",
            filter=None,
            start_date=starts,
            end_date=ends,
            searchable_key="name",
            searchable_value=searchable_value,
        )

        return [User.model_validate(item) for item in items]
