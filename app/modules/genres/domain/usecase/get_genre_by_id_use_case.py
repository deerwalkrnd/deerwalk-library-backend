from app.modules.genres.domain.entity.genre import Genre
from app.modules.genres.domain.repository.genre_repository_interface import (
    GenreRepositoryInterface,
)


class GetGenreByIdUseCase:
    def __init__(self, genre_repository: GenreRepositoryInterface) -> None:
        self.genre_repository = genre_repository

    async def execute(self, id: int) -> Genre | None:
        return await self.genre_repository.find_one(obj=Genre(id=id))
