from app.modules.reserves.domain.entities.reserve import Reserve
from app.modules.reserves.domain.repositories.reserves_repository_interface import (
    ReservesRepositoryInterface,
)


class ReserveBookUseCase:
    def __init__(self, reserves_repository: ReservesRepositoryInterface) -> None:
        self.reserves_repository = reserves_repository

    async def execute(self, book_copy_id: int, user_id: str) -> Reserve | None:
        return await self.reserves_repository.find_one(
            obj=Reserve(book_copy_id=book_copy_id, user_id=user_id)
        )
