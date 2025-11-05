from app.modules.reserves.domain.repositories.reserves_repository_interface import (
    ReservesRepositoryInterface,
)
from app.modules.reserves.domain.entities.reserve import Reserve
from app.core.models.reserve import BookReserveEnum


class GetTopIssuedBooksUseCase:
    def __init__(self, reserve_repository: ReservesRepositoryInterface):
        self.reserve_repository = reserve_repository

    async def execute(self, limit: int):
        return await self.reserve_repository.filter(
            limit=limit,
            offset=0,
            filter=Reserve(
                state=BookReserveEnum.RESERVED,
            ),
            sort_by="created_at",
            descending=False,
            start_date=None,
            end_date=None,
            searchable_key=None,
            searchable_value=None,
        )
