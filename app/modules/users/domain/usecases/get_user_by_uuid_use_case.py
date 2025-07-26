from app.core.domain.entities.user import User, UserWithPassword
from app.core.domain.repositories.user_repository_interface import (
    UserRepositoryInterface,
)


class GetUserByUUIDUseCase:
    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self.user_repository = user_repository

    async def execute(self, uuid: str) -> User:
        user = await self.user_repository.find_one(obj=UserWithPassword(uuid=uuid))
        if not user:
            raise ValueError("user not found")
        return User.model_validate(user)
