from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infra.repositories.repository import Repository
from app.core.models.books_genre import BooksGenreModel
from app.core.models.genre import GenreModel
from app.modules.books.domain.entities.books_genre import BooksGenre
from app.modules.books.domain.repositories.books_genre_repository_interface import (
    BooksGenreRepositoryInterface,
)
from app.modules.genres.domain.entities.genre import Genre


class BooksGenreRepository(
    Repository[BooksGenreModel, BooksGenre], BooksGenreRepositoryInterface
):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, BooksGenreModel, BooksGenre)

    async def get_genres_by_book_id(self, book_id: int) -> List[Genre]:
        query = (
            select(GenreModel)
            .join(BooksGenreModel, BooksGenreModel.genre_id == GenreModel.id)
            .where(BooksGenreModel.book_id == book_id)
        )
        result = await self.db.execute(query)
        data = result.scalars().unique().all()

        return [Genre.model_validate(obj=x) for x in data]
