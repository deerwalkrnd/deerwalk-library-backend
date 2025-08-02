from app.modules.genres.domain.entity.genre import Genre
from app.modules.genres.domain.repository.genre_repository_interface import (
    GenreRepositoryInterface,
)


class DeleteGenreByIdUseCase:
    def __init__(self, genre_repository: GenreRepositoryInterface) -> None:
        self.genre_repository = genre_repository

    async def execute(self, id: int) -> None:
        await self.genre_repository.hard_delete(conditions=Genre(id=id))
