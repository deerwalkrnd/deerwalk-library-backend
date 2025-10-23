from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.infra.repositories.repository import Repository
from app.core.models.book import BookModel
from app.core.models.book_copy import BookCopyModel
from app.core.models.reserve import BookReserveEnum, ReserveModel
from app.modules.reserves.domain.entities.reserve import Reserve
from app.modules.reserves.domain.repositories.reserves_repository_interface import (
    ReservesRepositoryInterface,
)


class ReservesRepository(
    Repository[ReserveModel, Reserve], ReservesRepositoryInterface
):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, ReserveModel, Reserve)

    async def get_reserves_by_book(self, user_id: str, book_id: int) -> Reserve | None:
        query = (
            select(ReserveModel)
            .join(BookModel, BookCopyModel.book_id == BookModel.id)
            .join(BookCopyModel, ReserveModel.book_copy_id == BookCopyModel.id)
            .where(ReserveModel.user_id == user_id)
            .where(ReserveModel.state == BookReserveEnum.RESERVED)
            .where(BookModel.id == book_id)
        )

        result = await self.db.execute(query)
        reserve = result.scalar()

        if not reserve:
            return None

        return Reserve.model_validate(reserve)
