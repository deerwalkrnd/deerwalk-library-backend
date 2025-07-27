
from app.core.domain.entities.user import UserWithPassword
from app.core.domain.repositories.user_repository_interface import UserRepositoryInterface


class UpdateUsersByUUIDUseCase:
    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self.user_repository = user_repository
    
    async def execute(self, conditions: UserWithPassword, new: UserWithPassword) -> None:
        await self.user_repository.update(
            conditions=conditions,
            obj=new
        )
    