from app.core.models.reserve import BookReserveEnum
from app.modules.reserves.domain.entities.reserve import Reserve
from app.modules.reserves.domain.repositories.reserves_repository_interface import (
    ReservesRepositoryInterface,
)


class UpdateReserveStateUseCase:
    def __init__(self, reserves_repository: ReservesRepositoryInterface) -> None:
        self.reserves_repository = reserves_repository

    async def execute(self, reserve_id: int, state: BookReserveEnum) -> int:
        return await self.reserves_repository.update(
            conditions=Reserve(id=reserve_id), obj=Reserve(state=state)
        )
