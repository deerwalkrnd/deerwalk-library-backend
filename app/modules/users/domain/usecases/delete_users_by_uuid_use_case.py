from app.core.domain.entities.user import UserWithPassword
from app.core.domain.repositories.user_repository_interface import \
    UserRepositoryInterface


class DeleteUsersByUUIDUseCase:
    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self.user_repository = user_repository

    async def execute(self, uuid: str):
        await self.user_repository.delete(conditions=UserWithPassword(uuid=uuid))
        return None
