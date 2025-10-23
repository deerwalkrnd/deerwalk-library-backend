from app.modules.reserves.domain.entities.reserve import Reserve
from app.modules.reserves.domain.repositories.reserves_repository_interface import (
    ReservesRepositoryInterface,
)


class GetReserveByBookIdAndUserIdUseCase:
    def __init__(self, reserves_repository: ReservesRepositoryInterface) -> None:
        self.reserves_repository = reserves_repository

    async def execute(self, book_id: int, user_id: str) -> Reserve | None:
        return await self.reserves_repository.get_reserves_by_book(
            user_id=user_id, book_id=book_id
        )
