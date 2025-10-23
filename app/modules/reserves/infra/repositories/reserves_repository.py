from sqlalchemy.ext.asyncio import AsyncSession
from app.core.infra.repositories.repository import Repository
from app.core.models.reserve import ReserveModel
from app.modules.reserves.domain.entities.reserve import Reserve
from app.modules.reserves.domain.repositories.reserves_repository_interface import (
    ReservesRepositoryInterface,
)


class ReservesRepository(
    Repository[ReserveModel, Reserve], ReservesRepositoryInterface
):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, ReserveModel, Reserve)
