from app.core.domain.entities.user import User, UserWithPassword
from app.core.domain.repositories.user_repository_interface import (
    UserRepositoryInterface,
)
from app.modules.users.domain.request.user_creation_request import UserCreationRequest


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self.user_repository = user_repository

    async def execute(self, user_creation_request: UserCreationRequest) -> User:
        created = await self.user_repository.create(
            obj=UserWithPassword(
                name=user_creation_request.name,
                email=user_creation_request.email,
                password=user_creation_request.password,
                role=user_creation_request.role,
                graduating_year=user_creation_request.graduating_year,
                roll_number=user_creation_request.roll_number,
                user_metadata=user_creation_request.user_metadata,
            )
        )
        if not created:
            raise ValueError("error creating a user")

        return created
