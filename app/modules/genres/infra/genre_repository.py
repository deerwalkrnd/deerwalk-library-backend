from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infra.repositories.repository import Repository
from app.core.models.genre import GenreModel
from app.modules.genres.domain.entity.genre import Genre
from app.modules.genres.domain.repository.genre_repository_interface import (
    GenreRepositoryInterface,
)


class GenreRepository(Repository[GenreModel, Genre], GenreRepositoryInterface):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, model=GenreModel, entity=Genre)
