from app.modules.genres.domain.entities.genre import Genre
from app.modules.genres.domain.repositories.genre_repository_interface import (
    GenreRepositoryInterface,
)


class CreateGenreUseCase:
    def __init__(self, genre_repository: GenreRepositoryInterface) -> None:
        self.genre_repository = genre_repository

    async def execute(self, title: str, image_url: str) -> Genre | None:
        already = await self.genre_repository.find_one(
            obj=Genre(title=title, image_url=image_url)
        )

        if already:
            raise ValueError("genre already exists.")

        return await self.genre_repository.create(
            obj=Genre(title=title, image_url=image_url)
        )
