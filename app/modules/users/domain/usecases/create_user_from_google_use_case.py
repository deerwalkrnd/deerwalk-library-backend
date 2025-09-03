from app.core.domain.entities.user import User, UserWithPassword
from app.core.domain.repositories.user_repository_interface import (
    UserRepositoryInterface,
)


class CreateUserFromGoogleUseCase:
    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self.user_repository = user_repository

    async def execute(self, user: User) -> User:
        u = await self.user_repository.create(obj=UserWithPassword.model_validate(user))

        if not u:
            raise ValueError

        return User.model_validate(u)
