from typing import List
from app.core.domain.entities.user import User
from app.core.domain.repositories.user_repository_interface import (
    UserRepositoryInterface,
)


class GetAllStudentsUseCase:
    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self.user_repository = user_repository

    async def execute(self) -> List[User]:
        return await self.user_repository.get_all_students()
