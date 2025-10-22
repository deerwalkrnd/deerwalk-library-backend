from app.modules.reserves.domain.entities.reserve import Reserve
from app.modules.reserves.domain.repositories.reserves_repository_interface import (
    ReservesRepositoryInterface,
)


class GetReserveByIdUseCase:
    def __init__(self, reserve_repository: ReservesRepositoryInterface) -> None:
        self.reserve_repository = reserve_repository

    async def execute(self, reserve_id: int) -> Reserve | None:
        return await self.reserve_repository.find_one(obj=Reserve(id=reserve_id))
