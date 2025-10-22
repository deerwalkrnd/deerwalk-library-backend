from app.modules.reserves.domain.entities.reserve import Reserve
from app.modules.reserves.domain.repositories.reserves_repository_interface import (
    ReservesRepositoryInterface,
)


class RemoveReserveUseCase:
    def __init__(self, reserve_repository: ReservesRepositoryInterface) -> None:
        self.reserve_repository = reserve_repository

    async def execute(self, reserve_id: int):
        return await self.reserve_repository.delete(conditions=Reserve(id=reserve_id))
