from app.modules.genres.domain.entity.genre import Genre
from app.modules.genres.domain.repository.genre_repository_interface import (
    GenreRepositoryInterface,
)


class UpdateGenreByIdUseCase:
    def __init__(self, genre_repostory: GenreRepositoryInterface) -> None:
        self.genre_repository = genre_repostory

    async def execute(self, conditions: Genre, new: Genre) -> None:
        await self.genre_repository.update(conditions=conditions, obj=new)
