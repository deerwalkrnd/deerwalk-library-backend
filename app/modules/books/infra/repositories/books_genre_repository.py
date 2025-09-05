from sqlalchemy.ext.asyncio import AsyncSession
from app.core.infra.repositories.repository import Repository
from app.core.models.books_genre import BooksGenreModel
from app.modules.books.domain.entities.books_genre import BooksGenre
from app.modules.books.domain.repository.books_genre_repository_interface import (
    BooksGenreRepositoryInterface,
)


class BooksGenreRepository(
    Repository[BooksGenreModel, BooksGenre], BooksGenreRepositoryInterface
):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, BooksGenreModel, BooksGenre)
