from typing import Set

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infra.repositories.repository import Repository
from app.core.models.book_copy import BookCopyModel
from app.modules.books.domain.entities.book_copy import BookCopy
from app.modules.books.domain.repositories.book_copy_repository_interface import (
    BookCopyRepositoryInterface,
)


class BookCopyRepository(
    Repository[BookCopyModel, BookCopy], BookCopyRepositoryInterface
):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, BookCopyModel, BookCopy)

    async def get_all_unique_identifiers(self) -> Set[str]:
        query = select(self.model.unique_identifier).where(
            self.model.deleted == False, self.model.unique_identifier.is_not(None)
        )
        result = await self.db.execute(query)
        return set(result.scalars().all())
