from app.core.models.reserve import BookReserveEnum
from app.modules.reserves.domain.entities.reserve import Reserve
from app.modules.reserves.domain.repositories.reserves_repository_interface import (
    ReservesRepositoryInterface,
)


class GetReserveByBookCopyIdandUserIdUseCase:
    def __init__(self, reserves_repository: ReservesRepositoryInterface) -> None:
        self.reserves_repository = reserves_repository

    async def execute(self, user_id: str, book_copy_id: int) -> Reserve | None:
        return await self.reserves_repository.find_one(
            obj=Reserve(book_copy_id=book_copy_id, user_id=user_id, state=BookReserveEnum.RESERVED)
        )
