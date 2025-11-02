from datetime import datetime
from typing import List

from app.core.models.reserve import BookReserveEnum
from app.modules.reserves.domain.entities.reserve import Reserve
from app.modules.reserves.domain.repositories.reserves_repository_interface import (
    ReservesRepositoryInterface,
)


class GetManyReservesUseCase:
    def __init__(self, reserves_repository: ReservesRepositoryInterface) -> None:
        self.reserves_repository = reserves_repository

    async def execute(
        self,
        page: int,
        limit: int,
        starts: datetime | None,
        ends: datetime | None,
        searchable_field: str | None,
        searchable_value: str | None,
        sort_by: str,
        is_descending: bool,
    ) -> List[Reserve]:
        offset = (page - 1) * limit

        reserves = await self.reserves_repository.filter(
            limit=limit,
            descending=is_descending,
            offset=offset,
            sort_by=sort_by,
            start_date=starts,
            end_date=ends,
            searchable_key=searchable_field,
            searchable_value=searchable_value,
            filter=Reserve(state=BookReserveEnum.RESERVED),
        )

        return reserves
